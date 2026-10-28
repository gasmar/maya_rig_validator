from typing import Callable

from PySide6 import QtWidgets, QtGui, QtCore

from validation.validation import (
    ValidationResult,
    ValidationReport,
    ValidationState
)


class ValidationView(QtWidgets.QWidget):

    def __init__(
            self,
            run_validation: Callable[[], ValidationReport],
            select_object: Callable[[str], None],
            parent=None
    ) -> None:
        super().__init__(parent)
        self.run_validation = run_validation
        self.select_object = select_object

        self.setWindowTitle("Validator")
        self.resize(450, 500)

        self.main_layout = QtWidgets.QVBoxLayout()

        self.run_button = QtWidgets.QPushButton("Run Validation")
        self.run_button.clicked.connect(self.on_run_button_clicked)

        self.summary_label = QtWidgets.QLabel("No validation has been run.")

        self.results_list = QtWidgets.QListWidget()
        self.results_list.itemClicked.connect(self.on_result_clicked)

        self.details_label = QtWidgets.QLabel("Select a validation result to see details.")
        self.details_label.setWordWrap(True)

        self.failed_objects_list = QtWidgets.QListWidget()
        self.failed_objects_list.itemClicked.connect(self.on_failed_object_clicked)

        self.main_layout.addWidget(self.run_button)
        self.main_layout.addWidget(self.summary_label)
        self.main_layout.addWidget(self.results_list)
        self.main_layout.addWidget(self.details_label)
        self.main_layout.addWidget(self.failed_objects_list)

        self.setLayout(self.main_layout)

    def display_results(self, report: ValidationReport) -> None:
        self.results_list.clear()
        self.details_label.setText("Select a validation result to see details.")
        self.failed_objects_list.clear()

        if report.has_any_failures():
            status = "FAIL"
            self.summary_label.setStyleSheet("color: red")
        else:
            status = "PASS"
            self.summary_label.setStyleSheet("color: green")

        total_rules = len(report.results)
        self.summary_label.setText(f"{status} | {total_rules} rules")

        for result in report.results:
            item = QtWidgets.QListWidgetItem()

            if result.state == ValidationState.PASS:
                item.setText(f"[PASS] {result.name}")
                item.setForeground(QtGui.QColor("green"))
            else:
                item.setText(f"[FAIL] {result.name}")
                item.setForeground(QtGui.QColor("red"))

            item.setData(QtCore.Qt.UserRole, result)
            self.results_list.addItem(item)

    def display_result_details(self, result: ValidationResult) -> None:
        self.failed_objects_list.clear()
        self.details_label.setText(result.message)

        for node in result.failed_objects:
            self.failed_objects_list.addItem(node)

    def on_run_button_clicked(self) -> None:
        report = self.run_validation()
        self.display_results(report)

    def on_result_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        result = item.data(QtCore.Qt.UserRole)
        self.display_result_details(result)

    def on_failed_object_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        node = item.text()
        self.select_object(node)


