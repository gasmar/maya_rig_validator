from maya import cmds


def get_scene_joints():
    joints = cmds.ls(type="joint", long=True)

    return joints


def get_joint_rotations(joints):
    joints_with_rotations = []

    for joint in joints:
        rx = cmds.getAttr(f"{joint}.rx")
        ry = cmds.getAttr(f"{joint}.ry")
        rz = cmds.getAttr(f"{joint}.rz")

        if rx or ry or rz:
            joints_with_rotations.append(joint)
    return joints_with_rotations


def validate_joints():
    scene_joints = get_scene_joints()
    joints_with_rotations = get_joint_rotations(scene_joints)

    if scene_joints and not joints_with_rotations:
        return True

    return False