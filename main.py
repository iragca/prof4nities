from typer import Typer

from src.config import DirectoryPaths as dir
from src.utils import ensure_file, ensure_path, greetings

app = Typer()


@app.command()
def main():
    greetings(dir.PROJECT_ROOT.value.name)


@app.command()
def init_dirs():
    ensure_file(dir.ENV_FILE.value)
    ensure_path(dir.DATA.value)
    ensure_path(dir.EXTERNAL_DATA.value)


if __name__ == "__main__":
    app()
