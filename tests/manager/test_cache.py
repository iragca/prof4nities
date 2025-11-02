import pytest

from prof4nities.manager import CacheManager, JSONCache, TXTCache


def test_cache_manager_initialization(tmp_path):
    cache_manager = CacheManager(filename="test_cache", ext="json", directory=tmp_path)
    assert cache_manager.filename == "test_cache"
    assert cache_manager.ext == "json"
    assert cache_manager.cache_dir == tmp_path
    assert cache_manager.cache_dir.exists()


def test_get_cache_file(tmp_path):
    cache_manager = CacheManager(filename="test_cache", ext="txt", directory=tmp_path)
    expected_path = tmp_path / "test_cache.txt"
    assert cache_manager.cache_filepath == expected_path


def test_cache_property_json(tmp_path):
    cache_manager = CacheManager(filename="test_cache", ext="json", directory=tmp_path)
    cache = cache_manager._cache
    assert isinstance(cache, JSONCache)
    assert cache.filepath == tmp_path / "test_cache.json"


def test_cache_property_txt(tmp_path):
    cache_manager = CacheManager(filename="test_cache", ext="txt", directory=tmp_path)
    cache = cache_manager._cache
    assert isinstance(cache, TXTCache)
    assert cache.filepath == tmp_path / "test_cache.txt"


def test_cache_property_unsupported_extension(tmp_path):
    cache_manager = CacheManager(filename="test_cache", ext="xml", directory=tmp_path)
    with pytest.raises(ValueError, match="Unsupported cache file extension: xml"):
        _ = cache_manager._cache


def test_save_and_load_cache_json(tmp_path):
    cache_manager = CacheManager(filename="test_cache", ext="json", directory=tmp_path)
    data_to_save = {"key": "value"}
    cache_manager.save(data_to_save)

    loaded_data = cache_manager.load()
    assert loaded_data == data_to_save

    data_to_save = {"another_key": [1, 2, 3]}
    cache_manager.save(data_to_save)
    loaded_data = cache_manager.load()
    assert loaded_data == data_to_save

    data_to_save = [1, 2, 3, 4, 5]
    cache_manager.save(data_to_save)
    loaded_data = cache_manager.load()
    assert loaded_data == data_to_save


def test_save_and_load_cache_txt(tmp_path):
    cache_manager = CacheManager(filename="test_cache", ext="txt", directory=tmp_path)
    data_to_save = ["line1", "line2", "line3"]
    cache_manager.save(data_to_save)

    loaded_data = cache_manager.load()
    assert loaded_data == data_to_save

    data_to_save = ["another line", "yet another line"]
    cache_manager.save(data_to_save)
    loaded_data = cache_manager.load()
    assert loaded_data == data_to_save
