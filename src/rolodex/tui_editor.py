from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import TextArea, Markdown, Header, Footer

class MarkdownEditor(App):
    """TUI Markdown editor with live preview for your CRM."""

    CSS = """
    Screen { layout: vertical; }
    #body { height: 1fr; }
    TextArea { width: 1fr; }
    #preview { width: 1fr; padding: 1; border: solid green; }
    """
    # Save with Ctrl+S; Quit with Ctrl+Q (we implement our own quit)
    BINDINGS = [("ctrl+s", "save", "Save"), ("ctrl+q", "quit_editor", "Quit")]

    def __init__(self, initial_text: str = "", on_save=None):
        super().__init__()
        self.initial_text = initial_text
        self.on_save = on_save

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="body"):
            yield TextArea(placeholder="Type your Markdown...", id="editor")
            yield Markdown(id="preview")
        yield Footer()

    def on_mount(self) -> None:
        self.editor = self.query_one("#editor", TextArea)
        self.preview = self.query_one("#preview", Markdown)
        self.editor.text = self.initial_text
        self.preview.update(self.initial_text)

    # ← This replaces `self.editor.changed.connect(self.update_preview)`
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area.id == "editor":
            self.preview.update(self.editor.text)

    # Actions
    def action_save(self) -> None:
        if self.on_save:
            self.on_save(self.editor.text)
        self.notify("Notes saved")

    def action_quit_editor(self) -> None:
        # Auto-save on quit; remove these two lines if you prefer “prompt before quit”
        if self.on_save:
            self.on_save(self.editor.text)
        self.exit()
