from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from view_registry import register_view


@register_view("Settings", None, section_order=9999, title_order=1)
class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("⚙️ Settings")
        layout.addWidget(title)
        self.setLayout(layout)