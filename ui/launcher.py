from maya_validation.rules import (
    SceneHasJointsRule,
    UniqueJointNamesRule,
    JointNamingConventionRule,
    JointRotationRule,
    JointScaleRule,
)
from ui.controller import ValidationController
from ui.model import ValidationModel
from ui.view import ValidationView
from validation.runner import ValidationRunner


def launch() -> ValidationView:
    rules = [
        SceneHasJointsRule(),
        UniqueJointNamesRule(),
        JointNamingConventionRule("_jnt"),
        JointRotationRule(),
        JointScaleRule()
    ]
    runner = ValidationRunner(rules)
    model = ValidationModel()
    view = ValidationView()
    controller = ValidationController(model, runner, view)
    view.controller = controller

    view.show()

    return view