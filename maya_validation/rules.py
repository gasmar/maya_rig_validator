from __future__ import annotations

from typing import TYPE_CHECKING

from validation.validation import ValidationResult, ValidationRule

if TYPE_CHECKING:
    from maya_validation.context import MayaValidationContext


class SceneHasJointsRule(ValidationRule):

    def validate(self, context: MayaValidationContext) -> ValidationResult:
        scene_joints = context.get_joints()
        scene_joints_result = bool(scene_joints)
        message = "Scene has joints."
        if not scene_joints:
            message = "No joints in scene."

        result = ValidationResult(
            "Joints in scene",
            scene_joints_result,
            [],
            message
        )
        return result


class UniqueJointNamesRule(ValidationRule):

    def validate(self, context: MayaValidationContext) -> ValidationResult:
        joint_names: dict[str, list[str]] = {}
        duplicate_joints = []
        scene_joints = context.get_joints()
        message = "No duplicate joints."

        for joint in scene_joints:
            joint_short_name = joint.split("|")[-1]

            if joint_short_name not in joint_names:
                joint_names[joint_short_name] = [joint]
            else:
                joint_names[joint_short_name].append(joint)

        for joints in joint_names.values():
            if len(joints) > 1:
                duplicate_joints.extend(joints)

        if duplicate_joints:
            message = "Some joint names are not unique."

        result = ValidationResult(
            "Unique Joint Names",
            not duplicate_joints,
            duplicate_joints,
            message
        )
        return result


class JointNamingConventionRule(ValidationRule):
    def __init__(
            self,
            joint_suffix: str
    ) -> None:
        self.joint_suffix = joint_suffix

    def validate(self, context: MayaValidationContext) -> ValidationResult:
        invalid_name_joints = []
        scene_joints = context.get_joints()
        message = "Valid joint naming convention."

        for joint in scene_joints:
            joint_short_name = joint.split("|")[-1]
            if not joint_short_name.endswith(self.joint_suffix):
                invalid_name_joints.append(joint)

        if invalid_name_joints:
            message = "Some joints do not follow the naming convention(s)."

        result = ValidationResult(
            "Joint Naming Convention",
            not invalid_name_joints,
            invalid_name_joints,
            message
        )
        return result


class JointRotationRule(ValidationRule):

    def validate(self, context: MayaValidationContext) -> ValidationResult:
        invalid_rotation_joints = []
        scene_joints = context.get_joints()
        message = "All joint rotations are zero."

        for joint in scene_joints:
            rx = context.get_attribute(joint, "rx")
            ry = context.get_attribute(joint, "ry")
            rz = context.get_attribute(joint, "rz")

            if rx or ry or rz:
                invalid_rotation_joints.append(joint)

        if invalid_rotation_joints:
            message = "Some joints have non-zero rotations."

        result = ValidationResult(
            "Joint Rotations",
            not invalid_rotation_joints,
            invalid_rotation_joints,
            message
        )
        return result


class JointScaleRule(ValidationRule):

    def validate(self, context: MayaValidationContext) -> ValidationResult:
        invalid_scale_joints = []
        scene_joints = context.get_joints()
        message = "All joint scales are 1."

        for joint in scene_joints:
            sx = context.get_attribute(joint, "sx")
            sy = context.get_attribute(joint, "sy")
            sz = context.get_attribute(joint, "sz")

            if sx != 1 or sy != 1 or sz != 1:
                invalid_scale_joints.append(joint)

        if invalid_scale_joints:
            message = "Some joints have invalid scale values."

        result = ValidationResult(
            "Joint Scales",
            not invalid_scale_joints,
            invalid_scale_joints,
            message
        )
        return result


class JointVisibilityRule(ValidationRule):

    def validate(self, context: MayaValidationContext) -> ValidationResult:
        invisible_joints = []
        scene_joints = context.get_joints()
        message = "All joints are visible."

        for joint in scene_joints:
            visibility = context.get_attribute(joint, "visibility")

            if not visibility:
                invisible_joints.append(joint)

        if invisible_joints:
            message = "Some joints are not visible."

        result = ValidationResult(
            "Visible Joints",
            not invisible_joints,
            invisible_joints,
            message
        )
        return result


