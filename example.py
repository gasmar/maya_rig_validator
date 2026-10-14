from maya_validation.context import MayaValidationContext
from maya_validation.rules import (
    SceneHasJointsRule,
    UniqueJointNamesRule,
    JointNamingConventionRule,
    JointRotationRule,
    JointScaleRule
)
from validation.runner import ValidationRunner


def main() -> None:
    context = MayaValidationContext()
    rules = [
        SceneHasJointsRule(),
        UniqueJointNamesRule(),
        JointNamingConventionRule("_jnt"),
        JointRotationRule(),
        JointScaleRule(),
    ]

    runner = ValidationRunner(rules)
    results = runner.run(context)

    for result in results:
        print(result.name)
        print(result.passed)
        print(result.failed_objects)
        print(result.message)
        print("---------------------")


if __name__ == "__main__":
    main()