import unittest

from maya_validation.rules import (
    SceneHasJointsRule,
    UniqueJointNamesRule,
    JointNamingConventionRule,
    JointRotationRule,
    JointScaleRule
)


class FakeMayaContext:

    def __init__(
            self,
            joints: list[str],
            attribute_values: dict[str, float] | None = None
    ) -> None:
        self.joints = joints
        self.attribute_values = attribute_values or {}

    def get_joints(self) -> list[str]:
        return self.joints

    def get_attribute(self, joint: str, attribute_name: str):
        return self.attribute_values[f"{joint}.{attribute_name}"]


class TestSceneHasJointsRule(unittest.TestCase):

    def test_scene_with_joints(self):
        joints = ["|root_jnt", "|root_jnt|spine_jnt"]
        context = FakeMayaContext(joints)
        rule = SceneHasJointsRule()
        result = rule.validate(context)

        self.assertTrue(result.passed)

    def test_scene_without_joints(self):
        context = FakeMayaContext([])
        rule = SceneHasJointsRule()
        result = rule.validate(context)

        self.assertFalse(result.passed)


class TestUniqueJointsRule(unittest.TestCase):

    def test_unique_joints(self):
        joints = [
            "|root_jnt",
            "|root_jnt|spine_jnt"
        ]
        context = FakeMayaContext(joints)
        rule = UniqueJointNamesRule()
        result = rule.validate(context)

        self.assertTrue(result.passed)

    def test_duplicate_joints(self):
        joints = [
            "|characterA|spine_jnt",
            "|characterB|spine_jnt",
        ]
        context = FakeMayaContext(joints)
        rule = UniqueJointNamesRule()
        result = rule.validate(context)

        self.assertFalse(result.passed)
        self.assertEqual(result.failed_objects, joints)


class TestJointNamingConventionRule(unittest.TestCase):

    def test_valid_joint_names(self):
        joints = [
            "|root_jnt",
            "|root_jnt|spine_jnt",
            "|root_jnt|spine_jnt|head_jnt",
        ]
        context = FakeMayaContext(joints)
        rule = JointNamingConventionRule("_jnt")
        result = rule.validate(context)

        self.assertTrue(result.passed)
        self.assertEqual(result.failed_objects, [])

    def test_invalid_joint_names(self):
        joints = [
            "|root_jnt",
            "|root_jnt|spine",
            "|root_jnt|spine|head_jnt",
        ]
        context = FakeMayaContext(joints)
        rule = JointNamingConventionRule("_jnt")
        result = rule.validate(context)

        self.assertFalse(result.passed)
        self.assertEqual(result.failed_objects, ["|root_jnt|spine"])


class TestJointRotationRule(unittest.TestCase):

    def test_joints_with_zero_rotations(self):
        joints = [
            "|characterA|spine_jnt",
            "|characterB|spine_jnt",
        ]
        attribute_values = {
            "|characterA|spine_jnt.rx": 0,
            "|characterA|spine_jnt.ry": 0,
            "|characterA|spine_jnt.rz": 0,
            "|characterB|spine_jnt.rx": 0,
            "|characterB|spine_jnt.ry": 0,
            "|characterB|spine_jnt.rz": 0,
        }
        context = FakeMayaContext(joints, attribute_values)
        rule = JointRotationRule()
        result = rule.validate(context)

        self.assertTrue(result.passed)
        self.assertEqual(result.failed_objects, [])

    def test_joint_with_nonzero_rotation(self):
        joints = [
            "|root_jnt",
            "|root_jnt|spine_jnt",
        ]
        attribute_values = {
            "|root_jnt.rx": 0,
            "|root_jnt.ry": 0,
            "|root_jnt.rz": 0,
            "|root_jnt|spine_jnt.rx": 45,
            "|root_jnt|spine_jnt.ry": 0,
            "|root_jnt|spine_jnt.rz": 0,
        }
        context = FakeMayaContext(joints, attribute_values)
        rule = JointRotationRule()
        result = rule.validate(context)

        self.assertFalse(result.passed)
        self.assertEqual(result.failed_objects, ["|root_jnt|spine_jnt"])


class TestJointScaleRule(unittest.TestCase):

    def test_joints_with_valid_scales(self):
        joints = [
            "|characterA|spine_jnt",
            "|characterB|spine_jnt",
        ]
        attribute_values = {
            "|characterA|spine_jnt.sx": 1,
            "|characterA|spine_jnt.sy": 1,
            "|characterA|spine_jnt.sz": 1,
            "|characterB|spine_jnt.sx": 1,
            "|characterB|spine_jnt.sy": 1,
            "|characterB|spine_jnt.sz": 1,
        }
        context = FakeMayaContext(joints, attribute_values)
        rule = JointScaleRule()
        result = rule.validate(context)

        self.assertTrue(result.passed)
        self.assertEqual(result.failed_objects, [])

    def test_joints_with_invalid_scales(self):
        joints = [
            "|root_jnt",
            "|root_jnt|spine_jnt",
        ]
        attribute_values = {
            "|root_jnt.sx": 1,
            "|root_jnt.sy": 1,
            "|root_jnt.sz": 1,
            "|root_jnt|spine_jnt.sx": 5,
            "|root_jnt|spine_jnt.sy": 0,
            "|root_jnt|spine_jnt.sz": 1,
        }
        context = FakeMayaContext(joints, attribute_values)
        rule = JointScaleRule()
        result = rule.validate(context)

        self.assertFalse(result.passed)
        self.assertEqual(result.failed_objects, ["|root_jnt|spine_jnt"])