from maya_validation.context import MayaValidationContext
from maya_validation.rules import (
    SceneHasJointsRule,
    UniqueJointNamesRule,
    JointNamingConventionRule,
    JointRotationRule,
    JointScaleRule, JointVisibilityRule
)
from validation.report import ValidationReport
from validation.runner import ValidationRunner


def main() -> None:
    context = MayaValidationContext()
    rules = [
        SceneHasJointsRule(),
        UniqueJointNamesRule(),
        JointNamingConventionRule("_jnt"),
        JointRotationRule(),
        JointScaleRule(),
        JointVisibilityRule()
    ]

    runner = ValidationRunner(rules)
    results = runner.run(context)
    report = ValidationReport(results)

    for result in results:
        print(result.name)
        print(result.passed)
        print(result.failed_objects)
        print(result.message)
        print("---------------------")

    print("-------REPORT-------")
    print(f"total rules: {report.get_total_rules()}")
    print(f"passed rules: {report.get_passed_rules()}")
    print(f"failed rules: {report.get_failed_rules()}")
    print(f"overall valid: {report.is_valid()}")
    

if __name__ == "__main__":
    main()