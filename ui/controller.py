from PySide6 import QtWidgets, QtCore
from maya import cmds

from maya_validation.context import MayaValidationContext
from ui.model import ValidationModel
from ui.view import ValidationView
from validation.report import ValidationReport
from validation.runner import ValidationRunner


class ValidationController:

    def __init__(
            self,
            model: ValidationModel,
            runner: ValidationRunner,
            view: ValidationView,
    ) -> None:
        self.model = model
        self.runner = runner
        self.view = view

        self.view.run_button.clicked.connect(self.on_run_clicked)
        self.view.results_list.itemClicked.connect(self.on_result_clicked)
        self.view.failed_objects_list.itemClicked.connect(self.on_failed_object_clicked)

    def run_validation(self, context) -> None:
        results = self.runner.run(context)
        report = ValidationReport(results)
        self.model.set_report(report)
        self.view.display_results(report)

    def on_run_clicked(self) -> None:
        context = MayaValidationContext()
        self.run_validation(context)

    def on_result_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        result = item.data(QtCore.Qt.UserRole)
        self.view.display_result_details(result)

    def on_failed_object_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        node = item.text()
        if cmds.objExists(node):
            cmds.select(node)
        else:
            print(f"Node {node} longer exists or has been fixed and passed validation.")