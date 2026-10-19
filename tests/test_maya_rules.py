import sys
import types
import unittest
from unittest.mock import patch

fake_maya = types.ModuleType("maya")
fake_cmds = types.ModuleType("maya.cmds")

fake_maya.cmds = fake_cmds
fake_cmds.getAttr = lambda attribute: None

with patch.dict(sys.modules, {
    "maya": fake_maya,
    "maya.cmds": fake_cmds,
}):

    from maya_validation.rules import (
        SceneHasJointsRule,
        UniqueJointNamesRule,
        JointNamingConventionRule,
        JointRotationRule,
        JointScaleRule
    )


class FakeMayaContext:

    def __init__(self, joints: list[str]) -> None:
        self.joints = joints

    def get_joints(self) -> list[str]:
        return self.joints


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
        with patch.object(fake_cmds, "getAttr", return_value=0):
            joints = [
                "|characterA|spine_jnt",
                "|characterB|spine_jnt",
            ]
            context = FakeMayaContext(joints)
            rule = JointRotationRule()
            result = rule.validate(context)

            self.assertTrue(result.passed)
            self.assertEqual(result.failed_objects, [])

    def test_joint_with_nonzero_rotation(self):
        rotation_values = {
            "|root_jnt.rx": 0,
            "|root_jnt.ry": 0,
            "|root_jnt.rz": 0,
            "|root_jnt|spine_jnt.rx": 45,
            "|root_jnt|spine_jnt.ry": 0,
            "|root_jnt|spine_jnt.rz": 0,
        }
        with patch.object(fake_cmds, "getAttr", side_effect=rotation_values.get):
            joints = [
                "|root_jnt",
                "|root_jnt|spine_jnt",
            ]

            context = FakeMayaContext(joints)
            rule = JointRotationRule()
            result = rule.validate(context)

            self.assertFalse(result.passed)
            self.assertEqual(result.failed_objects, ["|root_jnt|spine_jnt"])


class TestJointScaleRule(unittest.TestCase):

    def test_joints_with_valid_scales(self):
        with patch.object(fake_cmds, "getAttr", return_value=1):
            joints = [
                "|characterA|spine_jnt",
                "|characterB|spine_jnt",
            ]
            context = FakeMayaContext(joints)
            rule = JointScaleRule()
            result = rule.validate(context)

            self.assertTrue(result.passed)
            self.assertEqual(result.failed_objects, [])

    def test_joints_with_invalid_scales(self):
        scale_values = {
            "|root_jnt.sx": 1,
            "|root_jnt.sy": 1,
            "|root_jnt.sz": 1,
            "|root_jnt|spine_jnt.sx": 5,
            "|root_jnt|spine_jnt.sy": 0,
            "|root_jnt|spine_jnt.sz": 1,
        }
        with patch.object(fake_cmds, "getAttr", side_effect=scale_values.get):
            joints = [
                "|root_jnt",
                "|root_jnt|spine_jnt",
            ]
            context = FakeMayaContext(joints)
            rule = JointScaleRule()
            result = rule.validate(context)

            self.assertFalse(result.passed)
            self.assertEqual(result.failed_objects, ["|root_jnt|spine_jnt"])

