import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTreeWidget, QTreeWidgetItem, QStackedWidget, QFrame
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

        # === Sidebar (Left) using QTreeWidget ===
        self.sidebar = QTreeWidget()
        self.sidebar.setHeaderHidden(True)  # Hide the column header
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("""
            QTreeWidget {
                background-color: #2C3E50;
                color: white;
                
            }
        #    QTreeWidget::item {
        #        padding: 8px;
        #    }
        #    QTreeWidget::item:selected {
        #        background-color: #fABC9C;
        #    }
        """)

        self.content_stack = QStackedWidget()
        self.views = {}

        # === Populate Sidebar from Config ===
        self.tree_items = {}  # Store references to tree items

        for menu_name, data in self.menu_config.items():
            parent_item = QTreeWidgetItem([data["title"]])

            # If the menu has sub-items, add them under the parent
            if "submenu" in data:
                for sub_name, sub_data in data["submenu"].items():
                    sub_item = QTreeWidgetItem(parent_item, [sub_name])
                    self.tree_items[sub_name] = sub_data["view"]
                    self.add_view(sub_data["view"])

            # If the menu item is standalone, store it for direct selection
            if "view" in data:
                self.tree_items[data["title"]] = data["view"]
                self.add_view(data["view"])

            self.sidebar.addTopLevelItem(parent_item)

        self.sidebar.itemClicked.connect(self.handle_menu_click)

        # === Header Bar ===
        #header = QLabel("ERP Data Migration Tool")
        #header.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px; background-color: #1ABC9C; color: white;")
        #header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === Content Area (Right) ===
        content_area = QVBoxLayout()
        #content_area.addWidget(header)
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

        self.switch_view("Dashboard")  # Default to dashboard

    def add_view(self, view_name):
        """Dynamically add views to stack."""
        if view_name not in self.views and hasattr(sys.modules[__name__], view_name):
            view = getattr(sys.modules[__name__], view_name)()
            self.views[view_name] = view
            self.content_stack.addWidget(view)

    def handle_menu_click(self, item):
        """Handles sidebar item selection."""
        menu_text = item.text(0)

        # Check if this is a top-level item with a direct view
        if item.parent() is None and menu_text in self.tree_items:
            self.switch_view(self.tree_items[menu_text])

        # If it's a submenu, switch to its view
        elif menu_text in self.tree_items:
            self.switch_view(self.tree_items[menu_text])

    def switch_view(self, view_name):
        """Switch content area."""
        if view_name in self.views:
            self.content_stack.setCurrentWidget(self.views[view_name])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

