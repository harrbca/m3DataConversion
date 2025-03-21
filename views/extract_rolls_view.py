from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from view_registry import registered_views, register_view


@register_view("Export", "MMS015_add", section_order=3, title_order=1)
class ExportMMS015View(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📤 Export - MMS015_add")
        layout.addWidget(title)
        self.setLayout(layout)