from maya import cmds


def get_scene_joints() -> list[str]:
    joints = cmds.ls(type="joint", long=True)
    return joints


def scene_has_joints(scene_joints: list[str]) -> bool:
    if scene_joints:
        return True
    return False


def get_joints_with_duplicate_names(scene_joints: list[str]) -> list[str]:
    joint_names = {}
    duplicate_joints = []

    for joint in scene_joints:
        joint_short_name = joint.split("|")[-1]

        if joint_short_name not in joint_names:
            joint_names[joint_short_name] = [joint]
        else:
            joint_names[joint_short_name].append(joint)

    for joint_name, joints in joint_names.items():
        if len(joints) > 1:
            duplicate_joints.extend(joints)

    return duplicate_joints


def get_joints_with_invalid_names(
        scene_joints: list[str],
        joint_suffix: str
) -> list[str]:

    invalid_name_joints = []

    for joint in scene_joints:
        joint_short_name = joint.split("|")[-1]
        if not joint_short_name.endswith(joint_suffix):
            invalid_name_joints.append(joint)

    return invalid_name_joints


def get_joints_with_invalid_rotations(joints: list[str]) -> list[str]:
    invalid_rotation_joints = []

    for joint in joints:
        rx = cmds.getAttr(f"{joint}.rx")
        ry = cmds.getAttr(f"{joint}.ry")
        rz = cmds.getAttr(f"{joint}.rz")

        if rx or ry or rz:
            invalid_rotation_joints.append(joint)
    return invalid_rotation_joints


def get_joints_with_invalid_scales(joints: list[str]) -> list[str]:
    invalid_scale_joints = []

    for joint in joints:
        sx = cmds.getAttr(f"{joint}.sx")
        sy = cmds.getAttr(f"{joint}.sy")
        sz = cmds.getAttr(f"{joint}.sz")

        if sx != 1 or sy != 1 or sz != 1:
            invalid_scale_joints.append(joint)
    return invalid_scale_joints


def validate_joints() -> dict[str, bool | list[str]]:
    scene_joints = get_scene_joints()
    scene_has_joints_result = scene_has_joints(scene_joints)

    joint_suffix = "_jnt"
    duplicate_joints = get_joints_with_duplicate_names(scene_joints)
    invalid_name_joints = get_joints_with_invalid_names(scene_joints, joint_suffix)
    invalid_rotation_joints = get_joints_with_invalid_rotations(scene_joints)
    invalid_scale_joints = get_joints_with_invalid_scales(scene_joints)

    validation = {
        "validate": scene_has_joints_result
                    and not duplicate_joints
                    and not invalid_name_joints
                    and not invalid_rotation_joints
                    and not invalid_scale_joints,

        "scene_has_joints": scene_has_joints_result,

        "joint_names_are_unique": not duplicate_joints,
        "duplicate_joints": duplicate_joints,

        "joint_names_are_valid": not invalid_name_joints,
        "invalid_name_joints": invalid_name_joints,

        "joint_rotations_are_valid": not invalid_rotation_joints,
        "invalid_rotation_joints": invalid_rotation_joints,

        "joint_scales_are_valid": not invalid_scale_joints,
        "invalid_scale_joints": invalid_scale_joints,
    }
    return validation


