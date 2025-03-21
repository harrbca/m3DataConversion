import os
import shutil
import sys

from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTreeWidget, QTreeWidgetItem, QStackedWidget, QMessageBox, QFileDialog
)

from view_registry import registered_views, discover_views



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ERP Data Migration Tool")
        self.setGeometry(200, 200, 1000, 600)

        discover_views()

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



        self.build_sidebar()
        self.sidebar.itemClicked.connect(self.handle_menu_click)

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

    def get_sorted_sections(self):
        sections = {v["section"] for v in registered_views.values()}
        return sorted(
            sections,
            key=lambda sec: min(
                v["section_order"]
                for k, v in registered_views.items()
                if v["section"] == sec
            )
        )

    def get_sorted_titles_for_section(self, section):
        """Return full keys for views in a section (excluding section-only), sorted by title_order."""
        return sorted(
            [k for k, v in registered_views.items() if v["section"] == section and v["title"]],
            key=lambda k: registered_views[k]["title_order"]
        )


    def build_sidebar(self):

        for section in self.get_sorted_sections():
            section_item = QTreeWidgetItem([section])
            section_item.setData(0, Qt.ItemDataRole.TextAlignmentRole, Qt.AlignmentFlag.AlignLeft)
            self.sidebar.addTopLevelItem(section_item)

            section_view_key = section
            has_section_view = section_view_key in registered_views

            if has_section_view and registered_views[section_view_key]["title"] is None:
                section_item.setData(0, Qt.ItemDataRole.UserRole, section_view_key)

            for key in self.get_sorted_titles_for_section(section):
                title = registered_views[key]["title"]
                item = QTreeWidgetItem(section_item, [title])
                item.setData(0, Qt.ItemDataRole.TextAlignmentRole, Qt.AlignmentFlag.AlignLeft)
                item.setData(0, Qt.ItemDataRole.UserRole, key)


    def handle_menu_click(self, item):
        """Handles sidebar item selection."""
        view_key = item.data(0, Qt.ItemDataRole.UserRole)
        if view_key and view_key in registered_views:
            self.switch_view(view_key)

    def switch_view(self, view_key):
        """Dynamically create the view if not already added."""
        if view_key in self.views:
            self.content_stack.setCurrentWidget(self.views[view_key])
        else:
            new_view = registered_views[view_key]["class"]()  # Instantiate class
            self.views[view_key] = new_view
            self.content_stack.addWidget(new_view)
            self.content_stack.setCurrentWidget(new_view)


def ensure_data_dir_with_prompt(parent_widget=None):
    """
    Ensure the data directory exists. If not, prompt the user to either
    create the default directory or select a custom directory. Returns the
    final chosen directory path or None if the user cancels entirely.
    """
    # You could load a user preference from QSettings or a config file here.
    # For illustration, we'll just define a default:
    default_dir = r"C:\infor_migration"

    # Let's pretend we read from QSettings:
    settings = QSettings("Bravo", "m3DataConversion")
    data_dir = settings.value("data_dir", default_dir)

    # If it doesn't exist, ask user
    if not os.path.exists(data_dir):
        msg = (f"The directory:\n\n"
               f"{data_dir}\n\n"
               "does not exist. Do you want to create it now?\n"
               "Click 'Yes' to create, or 'No' to pick a different directory.")
        answer = QMessageBox.question(
            parent_widget,
            "Create Data Directory?",
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )
        if answer == QMessageBox.StandardButton.Yes:
            # Create the default directory
            os.makedirs(data_dir, exist_ok=True)

        elif answer == QMessageBox.StandardButton.No:
            # Let user pick a different directory
            chosen_dir = QFileDialog.getExistingDirectory(
                parent_widget,
                "Select Data Directory",
                os.path.dirname(data_dir) or "C:\\"
            )
            if chosen_dir:
                data_dir = chosen_dir
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir, exist_ok=True)
            else:
                # User canceled the directory selection
                return None

        else:
            # User hit 'Cancel' on the message box
            return None

        # Optionally copy a default config file into the newly created directory
        copy_default_config(data_dir)

        # Save the final chosen directory back to QSettings
        settings.setValue("data_dir", data_dir)

    # If it exists already, we can still optionally copy config if not present
    else:
        # Example: check if the config is missing, then copy
        config_path = os.path.join(data_dir, "default_config.yaml")
        if not os.path.isfile(config_path):
            copy_default_config(data_dir)

    return data_dir


def copy_default_config(target_dir):
    """
    Copies default_config.yaml from your script/config folder into target_dir,
    if it exists.
    """
    default_config_source = "config/config.ini.example"
    if os.path.isfile(default_config_source):
        dest_config_path = os.path.join(target_dir, os.path.basename(default_config_source))
        shutil.copyfile(default_config_source, dest_config_path)
    else:
        print("Warning: No default config found at", default_config_source)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    final_dir = ensure_data_dir_with_prompt()
    if not final_dir:
        print("User canceled. Exiting application.")
        sys.exit(0)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

