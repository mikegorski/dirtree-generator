from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Tuple


class BaseTreeGenerator(ABC):
    @abstractmethod
    def __init__(self, root: Path, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def build_tree(self) -> None:
        pass

    @abstractmethod
    def get_tree_repr(self) -> Tuple[Any, Callable]:
        pass
