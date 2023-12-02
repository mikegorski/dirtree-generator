from pathlib import Path
from typing import Callable, Optional, Tuple

from rich import print as rich_print
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree

from .base import BaseTreeGenerator
from .rich_styles import STYLES


class RichTreeGenerator(BaseTreeGenerator):
    def __init__(self, root: Path, style: str, verbose: bool, show_hidden: bool, *args, **kwargs) -> None:
        self.root = root
        self.tree: Optional[Tree] = None
        self.print_fn = rich_print
        self.style = STYLES[style]
        self.verbose = verbose
        self.show_hidden = show_hidden

    def build_tree(self) -> None:
        self._add_root()
        self._add_children(self.root, self.tree)

    def get_tree_repr(self) -> Tuple[Tree, Callable]:
        return self.tree, self.print_fn

    def _add_root(self) -> None:
        self.tree = Tree(
            f":open_file_folder: [link file://{self.root}]{self.root}",
            guide_style="bold bright_blue",
        )

    def _add_children(self, parent_dir: Path, parent_tree: Tree) -> None:
        locations = sorted(parent_dir.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
        for loc in locations:
            if loc.is_dir():
                self._add_directory(loc, parent_tree)
            else:
                self._add_file(loc, parent_tree)

    def _add_directory(self, directory: Path, parent_tree: Tree) -> None:
        style = "dim" if directory.name.startswith("__") else ""
        branch = parent_tree.add(
            f"[bold magenta]:open_file_folder: [link file://{directory}]{escape(directory.name)}",
            style=style,
            guide_style=style,
        )
        self._add_children(directory, branch)

    def _add_file(self, directory: Path, parent_tree: Tree) -> None:
        text_filename = Text(directory.name, "green")
        # text_filename.highlight_regex(r"\..*$", "bold red")
        # text_filename.stylize(f"link file://{directory}")
        if self.verbose:
            file_size = directory.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")
        icon = "🐍 " if directory.suffix.startswith(".py") else "📄 "
        parent_tree.add(Text(icon) + text_filename)
