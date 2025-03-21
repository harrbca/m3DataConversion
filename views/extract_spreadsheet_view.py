import pandas as pd
import pyodbc
import pymssql
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit,
    QProgressBar, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from config_reader import ConfigReader
import config_keys
from path_manager import PathManager
from view_registry import register_view

# === Fetch Database Config ===
config = ConfigReader.get_instance()
path_manager = PathManager()

db_type = config.get("CONNECTION", "DB_TYPE").lower()  # 'as400' or 'mssql'
excel_path = path_manager.get_path("PATHS", config_keys.CONFIG_ACTIVE_ITEM_PATH)
query_path = config.get("QUERIES", config_keys.CONFIG_ACTIVE_ITEM_SQL_QUERY_PATH)

# Load SQL query
with open(query_path) as file:
    select_query = file.read()


def connect_as400():
    """Establish a connection to the AS400 DB2 database."""
    conn_str = (
        f"DRIVER={{iSeries Access ODBC Driver}};"
        f"SYSTEM={config.get_connection('AS400_HOST')};"
        f"UID={config.get_connection('AS400_USERNAME')};"
        f"PWD={config.get_connection('AS400_PASSWORD')};"
        f"naming=1;"
        f"READONLY=1;"
    )
    return pyodbc.connect(conn_str)


def connect_mssql():
    """Establish a connection to the MSSQL database."""
    return pymssql.connect(
        server=config.get_connection('DB_SERVER'),
        user=config.get_connection('DB_USERNAME'),
        password=config.get_connection('DB_PASSWORD'),
        database=config.get_connection('DB_DATABASE')
    )


class DataExtractionThread(QThread):
    """Background thread to fetch and save data."""
    progress = pyqtSignal(int)  # Emits progress updates
    status_update = pyqtSignal(str)  # Emits status messages
    finished_signal = pyqtSignal(bool)  # Emits when task is finished

    def run(self):
        """Runs the database extraction in a background thread."""
        conn = None
        try:
            self.status_update.emit("Initializing data extraction...")

            # Connect to database
            if db_type == 'as400':
                self.status_update.emit("🔌 Connecting to AS400 DB2...")
                conn = connect_as400()
            elif db_type == 'mssql':
                self.status_update.emit("🔌 Connecting to MSSQL...")
                conn = connect_mssql()
            else:
                self.status_update.emit("❌ Invalid database type! Exiting.")
                self.finished_signal.emit(False)
                return

            self.status_update.emit("✅ Connection successful! Running query...")
            cursor = conn.cursor()

            if db_type == 'as400':
                cursor.execute(select_query)
                columns = [column[0] for column in cursor.description]  # Column names
                data = cursor.fetchall()
                df = pd.DataFrame([list(row) for row in data], columns=columns)
            else:  # MSSQL
                cursor = conn.cursor(as_dict=True)
                cursor.execute(select_query)
                data = cursor.fetchall()
                df = pd.DataFrame(data)

            if df.empty:
                self.status_update.emit("⚠️ No data retrieved!")
                self.finished_signal.emit(False)
                return

            self.status_update.emit(f"📊 Retrieved {len(df)} records. Saving to Excel...")

            # Save to Excel
            df.to_excel(excel_path, index=False)
            self.status_update.emit(f"✅ Data successfully saved to {excel_path}")
            self.progress.emit(100)  # Set progress bar to 100%
            self.finished_signal.emit(True)

        except Exception as e:
            self.status_update.emit(f"❌ Error: {e}")
            self.finished_signal.emit(False)

@register_view("Extraction", "Active Items", section_order=10, title_order=0)
class ExtractSpreadsheetView(QWidget):
    """GUI for Extracting and Saving Active Spreadsheet Data."""
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()

        self.title = QLabel("📊 Build Active Spreadsheet")
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title)

        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.status_output.setStyleSheet("background-color: #F5F5F5;")
        layout.addWidget(self.status_output)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_bar)

        self.extract_button = QPushButton("🔄 Start Extraction")
        self.extract_button.clicked.connect(self.start_extraction)
        layout.addWidget(self.extract_button)

        self.setLayout(layout)

    def start_extraction(self):
        """Starts the data extraction process."""
        self.status_output.append("🛠 Starting data extraction process...")
        self.extract_button.setEnabled(False)  # Disable button while running

        self.worker = DataExtractionThread()
        self.worker.status_update.connect(self.update_status)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished_signal.connect(self.extraction_finished)
        self.worker.start()

    def update_status(self, message):
        """Update the status message area."""
        self.status_output.append(message)
        self.status_output.ensureCursorVisible()

    def extraction_finished(self, success):
        """Handles cleanup after extraction is complete."""
        if success:
            QMessageBox.information(self, "Success", "✅ Data extraction completed successfully!")
        else:
            QMessageBox.warning(self, "Error", "❌ Data extraction failed. See log for details.")

        self.extract_button.setEnabled(True)
        self.progress_bar.setValue(0)
