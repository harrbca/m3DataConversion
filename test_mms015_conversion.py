import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QGroupBox, QHBoxLayout
)
from PyQt6.QtGui import QFont
from database import Database
from plugin_manager import load_transformer
from config_reader import ConfigReader

QUERY = "SELECT * FROM ITEMS where itemNumber = ?"

class ItemLookupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.config = ConfigReader.get_instance()
        self.transformer = load_transformer("mms015", self.config.get("TRANSFORMER", "mms015_transformer"))

    def init_ui(self):
        layout = QVBoxLayout()

        # Input Section
        input_layout = QHBoxLayout()
        self.label = QLabel("Enter an item number:")
        self.input_field = QLineEdit()
        self.lookup_button = QPushButton("Lookup Item")

        input_layout.addWidget(self.label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.lookup_button)

        # Table for Item Details
        self.item_details_group = QGroupBox("Item Details")
        details_layout = QVBoxLayout()
        self.item_details_table = QTableWidget(1, 5)
        self.item_details_table.setHorizontalHeaderLabels(["Item Number", "Pick UOM", "Price UOM", "Cost UOM", "Component"])
        self.item_details_table.setFont(QFont("Courier New", 10))
        details_layout.addWidget(self.item_details_table)
        self.item_details_group.setLayout(details_layout)

        # Table for MMS015 Data
        self.mms015_group = QGroupBox("MMS015 Data")
        mms015_layout = QVBoxLayout()
        self.mms015_table = QTableWidget(0, 12)
        self.mms015_table.setHorizontalHeaderLabels([
            "ITNO", "AUTP", "ALUN", "DCCD", "COFA", "DMCF", "PCOF", "AUS1", "AUS2", "AUS6", "UNMU", "AUSB"
        ])
        self.mms015_table.setFont(QFont("Courier New", 10))
        mms015_layout.addWidget(self.mms015_table)
        self.mms015_group.setLayout(mms015_layout)

        # Table for Unit Conversion Data
        self.unit_conversion_group = QGroupBox("Unit Conversion Table")
        unit_conversion_layout = QVBoxLayout()
        self.unit_conversion_table = QTableWidget(0, 3)
        self.unit_conversion_table.setHorizontalHeaderLabels(["From Unit", "To Unit", "Conversion Factor"])
        self.unit_conversion_table.setFont(QFont("Courier New", 10))
        unit_conversion_layout.addWidget(self.unit_conversion_table)
        self.unit_conversion_group.setLayout(unit_conversion_layout)

        # Add widgets to the main layout
        layout.addLayout(input_layout)
        layout.addWidget(self.lookup_button)
        layout.addWidget(self.item_details_group)
        layout.addWidget(self.mms015_group)
        layout.addWidget(self.unit_conversion_group)

        self.setLayout(layout)
        self.setWindowTitle("Item Lookup")
        self.lookup_button.clicked.connect(self.lookup_item)

    def _fetch_item_data(self, item_number):
        with Database() as db:
            result = db.fetch_dataframe(QUERY, (item_number,))
            return result.itertuples(index=False, name="Item").__next__() if not result.empty else None

    def update_item_details_table(self, item_data):
        values = [
            getattr(item_data, "itemNumber", ""),
            getattr(item_data, "IUM2", ""),
            getattr(item_data, "IUNITS", ""),
            getattr(item_data, "iunitc", ""),
            getattr(item_data, "ICOMPO", "")
        ]
        for col_idx, value in enumerate(values):
            self.item_details_table.setItem(0, col_idx, QTableWidgetItem(str(value)))

    def update_mms015_table(self, mms015_data):
        self.mms015_table.setRowCount(len(mms015_data))

        for row_idx, entry in enumerate(mms015_data):
            for col_idx, key in enumerate(["ITNO", "AUTP", "ALUN", "DCCD", "COFA", "DMCF", "PCOF", "AUS1", "AUS2", "AUS6", "UNMU", "AUSB"]):
                self.mms015_table.setItem(row_idx, col_idx, QTableWidgetItem(str(entry.get(key, ""))))

    def update_unit_conversion_table(self, graph_data):
        self.unit_conversion_table.setRowCount(sum(len(v) for v in graph_data.values()))
        row_idx = 0

        for source_unit, conversions in graph_data.items():
            for target_unit, value in conversions.items():
                self.unit_conversion_table.setItem(row_idx, 0, QTableWidgetItem(str(source_unit)))
                self.unit_conversion_table.setItem(row_idx, 1, QTableWidgetItem(str(target_unit)))
                self.unit_conversion_table.setItem(row_idx, 2, QTableWidgetItem(f"{value:.6f}"))
                row_idx += 1

    def lookup_item(self):
        item_number = self.input_field.text().strip()
        if not item_number:
            return

        item_data = self._fetch_item_data(item_number)
        if not item_data:
            return

        self.update_item_details_table(item_data)
        mms015_data = self.transformer.transform(item_data)
        self.update_mms015_table(mms015_data)

        # Placeholder for unit conversion data (Replace with actual retrieval logic)
        graph_data = {
            'SF': {'CT': 0.019481},
            'CT': {'SF': 51.33, 'LB': 35.28, 'PA': 0.016667},
            'LB': {'CT': 0.028345},
            'PA': {'CT': 60.0}
        }
        self.update_unit_conversion_table(graph_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemLookupApp()
    window.show()
    sys.exit(app.exec())

