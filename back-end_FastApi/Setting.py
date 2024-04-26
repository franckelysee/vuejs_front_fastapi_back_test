import pathlib

from starlette.config import Config

ROOT = pathlib.Path(__file__).resolve()
BASE_DIR = ROOT.parent

config = Config(BASE_DIR / ".env")

