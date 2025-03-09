import sys
from gui.uom_test_gui import Ui_MainWindow
from PyQt6 import QtWidgets

from dancik.dancik_uom import UOMService
from dancik.dancik_rolls import DancikRollsService

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.rolls = None
        self.uomService = None
        self.setupUi(self)

        self.loadItemButton.clicked.connect(self.on_load_item)
        self.itemNumberField.textChanged.connect(self.force_uppercase)
        self.uomComboBox.currentIndexChanged.connect(self.create_rolls_table)

        self.dancikRollsService = DancikRollsService()

    def on_load_item(self):
        self.uomService = UOMService(self.itemNumberField.text())
        self.uomComboBox.blockSignals(True)
        self.uomComboBox.clear()
        self.uomComboBox.addItems(self.uomService.graph.keys())
        self.uomComboBox.blockSignals(False)
        self.rolls = self.dancikRollsService.load_rolls(self.itemNumberField.text())
        self.create_rolls_table()
        print(self.rolls)
        print("Item loaded")

    def force_uppercase(self):
        self.itemNumberField.setText(self.itemNumberField.text().upper())

    def create_rolls_table(self):
        # Define the columns you need
        selected_columns = ["RWARE#", "RROLL#", "RLOC1", "RONHAN", "RUM"]

        # Cache the target UOM once
        target_uom = self.uomComboBox.currentText()

        # Create a copy of the selected columns from the original DataFrame
        df = self.rolls[selected_columns].copy()

        # Compute the converted on-hand values.
        # Here we assume self.uomService.convert is not vectorized.
        # You can use .apply() to compute the new column for each row.
        df["CONHAND"] = df.apply(
            lambda row: self.uomService.convert(row["RONHAN"], row["RUM"], target_uom), axis=1
        )

        # Set up the table dimensions and headers based on the new DataFrame
        self.rollsTable.setRowCount(len(df))
        self.rollsTable.setColumnCount(len(df.columns))
        self.rollsTable.setHorizontalHeaderLabels(df.columns.tolist())

        # Populate the QTableWidget with the DataFrame values
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                self.rollsTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()