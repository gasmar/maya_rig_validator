from PySide6 import QtWidgets, QtGui, QtCore

from validation.report import ValidationReport
from validation.result import ValidationResult


class ValidationView(QtWidgets.QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Maya Rig Validator")
        self.resize(450, 500)

        self.main_layout = QtWidgets.QVBoxLayout()

        self.run_button = QtWidgets.QPushButton("Run Validation")

        self.summary_label = QtWidgets.QLabel("No validation has been run.")

        self.results_list = QtWidgets.QListWidget()

        self.details_label = QtWidgets.QLabel("Select a validation result to see details.")
        self.details_label.setWordWrap(True)

        self.failed_objects_list = QtWidgets.QListWidget()

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

        total_rules = report.get_total_rules()
        passed_rules = report.get_passed_rules()
        failed_rules = report.get_failed_rules()

        is_valid = report.is_valid()
        if is_valid:
            status = "PASS"
            self.summary_label.setStyleSheet("color: green")
        else:
            status = "FAIL"
            self.summary_label.setStyleSheet("color: red")
        self.summary_label.setText(f"{status} {total_rules} rules | {passed_rules} passed | {failed_rules} failed")

        for result in report.results:
            item = QtWidgets.QListWidgetItem()

            if result.passed:
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