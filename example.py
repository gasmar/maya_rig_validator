from maya_validation.context import MayaValidationContext
from maya_validation.rules import (
    SceneHasJointsRule,
    UniqueJointNamesRule,
    JointNamingConventionRule,
    JointRotationRule,
    JointScaleRule,
    JointVisibilityRule
)
from validation.validation import (
    ValidationRunner,
    ValidationReport
)

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
        print(result.state)
        print(result.failed_objects)
        print(result.message)
        print("---------------------")

    print("-------REPORT-------")
    print(f"Has failures: {report.has_any_failures()}")
    

if __name__ == "__main__":
    main()