from maya import cmds

from validation.result import ValidationResult
from validation.rule import ValidationRule


class SceneHasJointsRule(ValidationRule):
    def __init__(self, scene_joints: list[str]) -> None:
        self.scene_joints = scene_joints

    def validate(self) -> ValidationResult:
        scene_joints_result = bool(self.scene_joints)

        result = ValidationResult(
            "Scene Has Joints",
            scene_joints_result,
            [],
            "Validation executed - Scene has joints."
        )
        return result


class UniqueJointNamesRule(ValidationRule):
    def __init__(self, scene_joints: list[str]) -> None:
        self.scene_joints = scene_joints

    def validate(self) -> ValidationResult:
        joint_names: dict[str, list[str]] = {}
        duplicate_joints = []

        for joint in self.scene_joints:
            joint_short_name = joint.split("|")[-1]

            if joint_short_name not in joint_names:
                joint_names[joint_short_name] = [joint]
            else:
                joint_names[joint_short_name].append(joint)

        for joints in joint_names.values():
            if len(joints) > 1:
                duplicate_joints.extend(joints)

        result = ValidationResult(
            "Unique Joint Names",
            not duplicate_joints,
            duplicate_joints,
            "Validation executed - Duplicate joints."
        )
        return result


class JointNamingConventionRule(ValidationRule):
    def __init__(
            self,
            scene_joints: list[str],
            joint_suffix: str
    ) -> None:
        self.scene_joints = scene_joints
        self.joint_suffix = joint_suffix

    def validate(self) -> ValidationResult:
        invalid_name_joints = []

        for joint in self.scene_joints:
            joint_short_name = joint.split("|")[-1]
            if not joint_short_name.endswith(self.joint_suffix):
                invalid_name_joints.append(joint)

        result = ValidationResult(
            "Joint Naming Convention",
            not invalid_name_joints,
            invalid_name_joints,
            "Validation executed - Invalid name joints."
        )
        return result


class JointRotationRule(ValidationRule):
    def __init__(self, scene_joints: list[str]) -> None:
        self.scene_joints = scene_joints

    def validate(self) -> ValidationResult:
        invalid_rotation_joints = []

        for joint in self.scene_joints:
            rx = cmds.getAttr(f"{joint}.rx")
            ry = cmds.getAttr(f"{joint}.ry")
            rz = cmds.getAttr(f"{joint}.rz")

            if rx or ry or rz:
                invalid_rotation_joints.append(joint)

        result = ValidationResult(
            "Joint Rotations",
            not invalid_rotation_joints,
            invalid_rotation_joints,
            "Validation executed - Joint Rotations."
        )
        return result


class JointScaleRule(ValidationRule):
    def __init__(self, scene_joints: list[str]) -> None:
        self.scene_joints = scene_joints

    def validate(self) -> ValidationResult:
        invalid_scale_joints = []

        for joint in self.scene_joints:
            sx = cmds.getAttr(f"{joint}.sx")
            sy = cmds.getAttr(f"{joint}.sy")
            sz = cmds.getAttr(f"{joint}.sz")

            if sx != 1 or sy != 1 or sz != 1:
                invalid_scale_joints.append(joint)

        result = ValidationResult(
            "Joint Scales",
            not invalid_scale_joints,
            invalid_scale_joints,
            "Validation executed - Joint Scales."
        )
        return result