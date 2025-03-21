import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt


# === Define Views ===
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📊 Dashboard - Summary Info")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        self.setLayout(layout)


class ImportItemsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📥 Import - Items")
        layout.addWidget(title)
        self.setLayout(layout)


class ImportLocationsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📥 Import - Locations")
        layout.addWidget(title)
        self.setLayout(layout)


class ImportInventoryView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📥 Import - Inventory")
        layout.addWidget(title)
        self.setLayout(layout)


class ExportMMS200View(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📤 Export - MMS200_AddItmBasic")
        layout.addWidget(title)
        self.setLayout(layout)


class ExportMMS015View(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📤 Export - MMS015_add")
        layout.addWidget(title)
        self.setLayout(layout)


class ExportCRS099View(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📤 Export - CRS099_add")
        layout.addWidget(title)
        self.setLayout(layout)


class TestsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("✅ Tests")
        layout.addWidget(title)
        self.setLayout(layout)


class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("⚙️ Settings")
        layout.addWidget(title)
        self.setLayout(layout)


class SidebarButton(QPushButton):
    """Custom Sidebar Button"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
        self.setCheckable(True)  # Buttons should be checkable
        self.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                border: none;
                color: white;
                background-color: #34495E;
                text-align: left;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2C3E50;
            }
            QPushButton:checked {
                background-color: #1ABC9C;
            }
        """)


class CollapsibleMenu(QWidget):
    """Expandable Sidebar Section for Nested Menus."""

    def __init__(self, title, options, parent_window):
        super().__init__()
        layout = QVBoxLayout()
        self.toggle_button = SidebarButton(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_submenu)

        self.submenu = QWidget()
        submenu_layout = QVBoxLayout()
        submenu_layout.setContentsMargins(20, 0, 0, 0)  # Indent submenu options
        self.sub_buttons = []

        for opt_name, opt_view in options.items():
            btn = SidebarButton("   └ " + opt_name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, view=opt_view, button=btn: parent_window.switch_view(view, button))
            submenu_layout.addWidget(btn)
            self.sub_buttons.append(btn)
            parent_window.add_view(opt_view)  # Ensure view is registered before switching

        self.submenu.setLayout(submenu_layout)
        self.submenu.setVisible(False)

        layout.addWidget(self.toggle_button)
        layout.addWidget(self.submenu)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def toggle_submenu(self):
        """Show/Hide submenu items."""
        self.submenu.setVisible(self.toggle_button.isChecked())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ERP Data Migration Tool")
        self.setGeometry(200, 200, 1000, 600)

        # === Load Menu Config ===
        with open("menu_config.json", "r", encoding="utf-8") as f:
            self.menu_config = json.load(f)

        # === Main Layout ===
        main_layout = QHBoxLayout()

        # === Sidebar (Left) ===
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #2C3E50; border-right: 2px solid #1C2833;")
        sidebar_layout = QVBoxLayout()

        # === Header Bar ===
        header = QLabel("ERP Data Migration Tool")
        header.setStyleSheet(
            "font-size: 20px; font-weight: bold; padding: 10px; background-color: #1ABC9C; color: white;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === Content Area (Right) ===
        content_area = QVBoxLayout()
        content_area.addWidget(header)

        self.content_stack = QStackedWidget()
        self.views = {}
        self.active_button = None  # Track the currently active button

        # === Create Sidebar from Config ===
        self.buttons = []
        for menu_name, data in self.menu_config.items():
            if "submenu" in data:
                submenu = CollapsibleMenu(data["title"], {k: v["view"] for k, v in data["submenu"].items()}, self)
                sidebar_layout.addWidget(submenu)
            else:
                btn = SidebarButton(data["title"])
                btn.clicked.connect(lambda _, view=data["view"], button=btn: self.switch_view(view, button))
                sidebar_layout.addWidget(btn)
                self.buttons.append(btn)
                self.add_view(data["view"])  # Ensure the view is registered before use

        sidebar_layout.addStretch()
        self.sidebar.setLayout(sidebar_layout)

        content_area.addWidget(self.content_stack)

        # === Combine Layouts ===
        right_panel = QWidget()
        right_panel.setLayout(content_area)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(right_panel)

        # Main container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.switch_view("Dashboard", None)  # Default to dashboard

    def add_view(self, view_name):
        """Dynamically add views to stack."""
        if view_name not in self.views and hasattr(sys.modules[__name__], view_name):
            view = getattr(sys.modules[__name__], view_name)()
            self.views[view_name] = view
            self.content_stack.addWidget(view)

    def switch_view(self, view_name, button):
        """Switch view and reset button states."""
        if view_name in self.views:
            # Uncheck the previous button
            if self.active_button:
                self.active_button.setChecked(False)

            # Set the new active button
            self.active_button = button
            if self.active_button:
                self.active_button.setChecked(True)

            self.content_stack.setCurrentWidget(self.views[view_name])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

