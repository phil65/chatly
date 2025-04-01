"""Top-level package for DataCook QtCharts Plugin."""

from prettyqt import widgets

from chatly.core.translate import _
from chatly.gui import trees


class FileExplorerPage(widgets.Widget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.set_title(_("Files"))
        self.set_icon("mdi.file")
        self.set_layout("horizontal", margin=0)
        # filters = appmanager.instance.supported_filetypes()
        self.tree = trees.FileTree()  # filters=filters
        # self.tree.context_actions = [
        #     fileactions.ImportAction,
        #     fileactions.RecipesAction,
        #     fileactions.RemoveAction,
        # ]
        self.box.add(self.tree)
        self.restore_timer = self.start_callback_timer(
            self.restore_expanded_state, interval=1000, single_shot=True
        )
        widgets.Application.call_on_exit(self.save_expanded_state)

    def save_expanded_state(self):
        pass
        # config.filetree_state = self.tree.get_expanded_state()

    def restore_expanded_state(self):
        pass
        # self.tree.set_expanded_state(config.filetree_state)


if __name__ == "__main__":
    app = widgets.app()
    w = FileExplorerPage()
    w.show()
    app.main_loop()
