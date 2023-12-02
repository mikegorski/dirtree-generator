import os
from pathlib import Path
from typing import Callable, Tuple

from .base import BaseTreeGenerator

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class PlainTreeGenerator(BaseTreeGenerator):
    def __init__(self, root: Path, verbose: bool, show_hidden: bool, *args, **kwargs) -> None:
        self.root = root
        self.structure: list[str] = []
        self.print_fn = print
        self.verbose = verbose
        self.show_hidden = show_hidden

    def build_tree(self) -> None:
        self._add_root()
        self._add_children(self.root)

    def get_tree_repr(self) -> Tuple[str, Callable]:
        return "".join(self.structure), self.print_fn

    def _add_root(self) -> None:
        self.structure.append(f"{self.root.name}{os.sep}\n")

    def _add_children(self, parent: Path, prefix: str = "") -> None:
        children = sorted(parent.iterdir(), key=lambda x: x.is_file())
        count = len(children)
        for index, child in enumerate(children):
            connector = ELBOW if index == count - 1 else TEE
            if child.is_dir():
                self._add_directory(child, index, count, prefix, connector)
            else:
                self._add_file(child, prefix, connector)

    def _add_directory(self, directory: Path, index: int, count: int, prefix: str, connector: str) -> None:
        self.structure.append(f"{prefix}{connector} {directory.name}{os.sep}\n")
        prefix += PIPE_PREFIX if index != count - 1 else SPACE_PREFIX
        self._add_children(directory, prefix)

    def _add_file(self, file: Path, prefix: str, connector: str) -> None:
        self.structure.append(f"{prefix}{connector} {file.name}\n")
