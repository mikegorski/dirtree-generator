from .base import BaseTreeGenerator
from .plain import PlainTreeGenerator
from .rich import RichTreeGenerator
from .rich_styles import STYLES

GEN_MAPPING = {"plain": PlainTreeGenerator, "rich": RichTreeGenerator}

__all__ = ["BaseTreeGenerator", "PlainTreeGenerator", "RichTreeGenerator", "STYLES", "GEN_MAPPING"]
