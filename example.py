from maya import cmds

from maya_validation.rules import (
    SceneHasJointsRule,
    UniqueJointNamesRule,
    JointNamingConventionRule,
    JointRotationRule,
    JointScaleRule
)
from validation.runner import ValidationRunner


def main() -> None:
    scene_joints = cmds.ls(type="joint", long=True)

    rules = [
        SceneHasJointsRule(scene_joints),
        UniqueJointNamesRule(scene_joints),
        JointNamingConventionRule(scene_joints, "_jnt"),
        JointRotationRule(scene_joints),
        JointScaleRule(scene_joints),
    ]

    runner = ValidationRunner(rules)
    results = runner.run()

    for result in results:
        print(result.name)
        print(result.passed)
        print(result.failed_objects)
        print(result.message)
        print("---------------------")


if __name__ == "__main__":
    main()