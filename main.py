import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt


class SidebarButton(QPushButton):
    """Custom Sidebar Button"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(50)
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


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📊 Dashboard - Summary Info")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        self.setLayout(layout)


class ImportView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📥 Import Data")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        self.setLayout(layout)


class ExportView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("📤 Export Data")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        self.setLayout(layout)


class TestsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("✅ Run Tests")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        self.setLayout(layout)


class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("⚙️ Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ERP Data Migration Tool")
        self.setGeometry(200, 200, 1000, 600)

        # === Main Layout ===
        main_layout = QHBoxLayout()

        # === Sidebar (Left) ===
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #2C3E50; border-right: 2px solid #1C2833;")
        sidebar_layout = QVBoxLayout()

        self.sidebar_buttons = []
        pages = ["🏠 Dashboard", "📥 Import", "📤 Export", "✅ Tests", "⚙️ Settings"]
        for i, page in enumerate(pages):
            btn = SidebarButton(page)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=i: self.switch_view(idx))
            sidebar_layout.addWidget(btn)
            self.sidebar_buttons.append(btn)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        # === Header Bar ===
        header = QLabel("ERP Data Migration Tool")
        header.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px; background-color: #1ABC9C; color: white;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === Content Area (Right) ===
        content_area = QVBoxLayout()
        content_area.addWidget(header)

        self.content_stack = QStackedWidget()
        self.dashboard = Dashboard()
        self.import_view = ImportView()
        self.export_view = ExportView()
        self.tests_view = TestsView()
        self.settings_view = SettingsView()

        self.content_stack.addWidget(self.dashboard)  # Index 0
        self.content_stack.addWidget(self.import_view)  # Index 1
        self.content_stack.addWidget(self.export_view)  # Index 2
        self.content_stack.addWidget(self.tests_view)  # Index 3
        self.content_stack.addWidget(self.settings_view)  # Index 4

        content_area.addWidget(self.content_stack)

        # === Combine Layouts ===
        right_panel = QWidget()
        right_panel.setLayout(content_area)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(right_panel)

        # Main container widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Default to dashboard
        self.sidebar_buttons[0].setChecked(True)
        self.content_stack.setCurrentIndex(0)

    def switch_view(self, index):
        """Switch content area and update button states."""
        for btn in self.sidebar_buttons:
            btn.setChecked(False)
        self.sidebar_buttons[index].setChecked(True)
        self.content_stack.setCurrentIndex(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
