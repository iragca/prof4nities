import json
from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path
from typing import Any, Literal, Union

from ..config import Directories
from ..utils import check_types


class Cache(ABC):
    """
    Abstract base class for simple persistent caches backed by a filesystem path.

    Subclasses must implement the load and save methods to define how data is
    serialized to and deserialized from the file at `filepath`. This class only
    stores the path to the cache location and documents the expected behavior of
    implementations.

    Parameters
    ----------
    filepath : pathlib.Path
        Filesystem path where the cache is stored. Implementations may assume the
        parent directory exists or create it as needed.

    Methods to implement
    --------------------
    load() -> Any
        Read and return the cached data from `filepath`. Implementations should:
        - Return the original object previously passed to `save`.
        - Raise FileNotFoundError if the cache file does not exist (or return a
          sentinel/None only if that behavior is documented by the subclass).
        - Raise a descriptive exception if the file exists but cannot be parsed.

    save(data: Any) -> None
        Persist `data` to `filepath`. Implementations should:
        - Ensure atomicity where possible (e.g., write to a temp file and rename).
        - Create parent directories if necessary, or document that callers must
          create them.
        - Raise an exception if the data cannot be serialized or written.

    Notes
    -----
    This is an abstract helper intended to centralize the cache file location and
    to enforce a consistent interface for different serialization strategies
    (e.g., JSON, pickle, YAML). Subclasses are responsible for thread/process
    safety and for choosing a serialization format appropriate for the stored
    objects.

    Example
    -------
    A JSON-backed implementation might implement `load` to open `filepath`,
    parse JSON and return the resulting object, and implement `save` to serialize
    the object to JSON with an atomic write.
    """

    @check_types
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @property
    def exists(self) -> bool:
        """Check if the cache file exists on disk."""
        return self.filepath.exists()

    @abstractmethod
    def load(self) -> Any:
        pass

    @abstractmethod
    def save(self, data: Any) -> None:
        pass


class JSONCache(Cache):
    """
    A simple JSON-backed cache that reads from and writes to a file referenced by
    self.filepath.

    The cache stores arbitrary JSON-serializable data and exposes two primary
    operations: load() to read and deserialize JSON content from the backing file,
    and save(data) to serialize and persist a Python dict or list to that file.

    Notes
    -----
    - The implementation expects self.filepath to be a pathlib.Path-like object
        supporting the .open(...) method.
    - No special concurrency guarantees are provided; concurrent readers/writers may
        result in race conditions or corrupted files.

    Attributes
    ----------
    filepath : pathlib.Path-like
        Path-like object pointing to the JSON file used for persistence. The object
        must support the .open(mode, encoding=...) method.

    Methods
    -------
    load()
        Open the file at self.filepath for reading (UTF-8) and return the
        deserialized JSON content (a dict or a list).
    save(data)
        Persist `data` to self.filepath as JSON using UTF-8 encoding. Writes with
        ensure_ascii=False and an indent of 4 for human-readable formatting. This
        method accepts only a dict or a list.

    -------
    load : dict | list
        The Python object deserialized from the JSON file. The exact type depends
        on the stored JSON (typically a dict or a list).
    save : None
        No return value.

    Parameters (for save)
    ---------------------
    data : dict | list
        The JSON-serializable object to persist. Only dicts and lists are accepted
        by this implementation.

    Raises
    ------
    ValueError
        If save() is called with a value that is not a dict or list.
    FileNotFoundError, PermissionError, json.JSONDecodeError, OSError
        I/O and JSON-related exceptions raised by pathlib.Path.open, json.load or
        json.dump are propagated to the caller.

    -----
    - save() may be decorated with runtime type-checking utilities (e.g., @check_types)
      in the surrounding codebase; behavior depends on that decorator.
    - No special concurrency guarantees are provided. Concurrent readers/writers
      may result in race conditions or corrupted files; external synchronization is
      recommended for concurrent access.
    - The implementation expects a pathlib.Path-like object that implements .open().

    Examples
    --------
    Typical usage:

        cache = JSONCache(...)         # filepath assigned on initialization
        data = cache.load()           # returns dict or list loaded from file
        cache.save({"key": "value"})  # writes JSON to the backing file
    """

    def load(self) -> Union[dict[str, Any], list[Any]]:
        with self.filepath.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: Union[dict, list[Any]]) -> None:
        if not isinstance(data, (dict, list)):
            raise ValueError("JSONCache can only save dict or list data.")

        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


class TXTCache(Cache):
    """
    A simple disk-backed cache that stores and retrieves a list of strings as a UTF-8
    text file with one item per line.

    Methods
    -------
    load() -> list[str]
        Open the file at self.filepath for reading (UTF-8) and return a list of lines
        with newline characters removed.
    save(data: list[Any]) -> None
        Write the provided list to self.filepath using UTF-8 encoding. Elements are
        joined with a single newline between items.

    Parameters
    ----------
    None

    Raises
    ------
    ValueError
        If save() is called with a non-list argument.
    TypeError
        If non-string elements are present and joining them into text fails.
    OSError, IOError
        On filesystem read/write failures.
    """

    def load(self) -> list[str]:
        with self.filepath.open("r", encoding="utf-8") as f:
            return f.read().splitlines()

    def save(self, data: list[Any]) -> None:
        if not isinstance(data, list):
            raise ValueError("TXTCache can only save list data.")

        with self.filepath.open("w", encoding="utf-8") as f:
            f.write("\n".join(data))


class CacheManager(Cache):
    """
    Manage on-disk cache files for simple JSON or text-backed caches.

    This class centralizes creation and access to a small cache directory and
    provides convenience methods for obtaining a cache file path, loading cache
    contents, and saving data. When instantiated, it ensures the cache directory
    exists.

    Parameters
    ----------
    filename : str
        Base name of the cache file (without extension).
    ext : {'json', 'txt'}, optional
        File extension/type of the cache. Supported values are `'json'` and `'txt'`.
        Default is `'txt'`.
    directory : Path, optional
        Parent directory in which a hidden `.cache` folder will be created.
        Default is ``Directories.CACHE_DIR.value``.

    Attributes
    ----------
    cache_dir : Path
        Full path to the directory used to store cache files
        (i.e., ``directory``). This directory is created on
        initialization if it does not already exist.
    filename : str
        The provided cache filename base.
    ext : str
        The chosen cache file extension/type.

    Methods
    -------
    get_cache_file()
        Return the full path to the cache file (``cache_dir / f"{filename}.{ext}"``).
    _cache : Cache
        Dynamically construct and return the appropriate cache backend
        instance (e.g., `JSONCache` or `TXTCache`) for the current `ext`.
    load()
        Load and return the cache contents using the selected backend's `load` method.
    save(data)
        Persist `data` using the selected backend's `save` method.

    Raises
    ------
    ValueError
        If an unsupported `ext` value is provided when accessing the `cache` property.

    Notes
    -----
    This class delegates actual serialization/deserialization to backend
    implementations (`JSONCache`, `TXTCache`) and only manages location and
    selection of the appropriate backend.

    A `check_types` decorator is used on the initializer and `save` method
    in the original implementation to validate input types at runtime.
    """

    def __init__(
        self,
        filename: str,
        ext: Literal["json", "txt"] = "txt",
        directory: Path = Directories.CACHE_DIR.value,
    ) -> None:
        self.cache_dir = directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.filename = filename
        self.ext = ext

    @cached_property
    def cache_filepath(self) -> Path:
        """Get the full path to the cache file."""
        return self.cache_dir / f"{self.filename}.{self.ext}"

    @cached_property
    def _cache(self) -> Cache:
        if self.ext == "json":
            return JSONCache(self.cache_filepath)
        elif self.ext == "txt":
            return TXTCache(self.cache_filepath)
        else:
            raise ValueError(f"Unsupported cache file extension: {self.ext}")

    @property
    def exists(self) -> bool:
        """Check if the cache file exists on disk."""
        return self.cache_filepath.exists()

    def load(self) -> Any:
        """
        Load and return the cached value from the underlying cache backend.

        This method delegates to self.cache.load() and returns whatever the backend provides
        (typically a deserialized object, or None if no value is cached). The exact return
        type depends on the cache implementation and stored payload.

        Returns
        -------
        Any
            The object returned by the underlying cache's load method. This could be a dict,
            list, or other type depending on the cache implementation.

        Notes
        -----
            - This method performs a read-only operation and does not modify the cache.
            - Thread-safety and atomicity depend on the underlying cache implementation.
            - Callers should validate the returned value and handle any propagated exceptions.
        """
        return self._cache.load()

    def save(self, data: Any) -> None:
        """
        Persist the given data using the manager's configured cache backend.

        This method delegates the actual storage operation to self.cache.save(data).
        The exact persistence semantics (serialization format, storage medium,
        expiration, keying) are determined by the concrete cache implementation
        attached to this manager.

        Parameters
        ----------
        data : Any
            The object to save into the cache. Ensure the object is compatible with
            the configured cache backend (for example, serializable if required).

        Returns
        -------
        None
        """
        self._cache.save(data)
