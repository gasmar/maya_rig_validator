from maya import cmds

from maya_validation.context import MayaValidationContext
from maya_validation.rules import (
    SceneHasJointsRule,
    UniqueJointNamesRule,
    JointNamingConventionRule,
    JointRotationRule,
    JointScaleRule,
    JointVisibilityRule,
)
from ui.view import ValidationView
from validation.validation import ValidationRunner, ValidationReport


def launch() -> ValidationView:
    rules = [
        SceneHasJointsRule(),
        UniqueJointNamesRule(),
        JointNamingConventionRule("_jnt"),
        JointRotationRule(),
        JointScaleRule(),
        JointVisibilityRule()
    ]
    runner = ValidationRunner(rules)

    def run_validation() -> ValidationReport:
        context = MayaValidationContext()
        results = runner.run(context)
        report = ValidationReport(results)
        return report

    def select_object(node: str) -> None:
        if cmds.objExists(node):
            cmds.select(node)

    view = ValidationView(run_validation, select_object)
    view.show()

    return view