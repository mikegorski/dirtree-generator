from .generators import BaseTreeGenerator


class TreePresenter:
    def __init__(self, generator: BaseTreeGenerator):
        self.generator = generator

    def display(self) -> None:
        tree, print_fn = self.generator.get_tree_repr()
        print_fn(tree)
