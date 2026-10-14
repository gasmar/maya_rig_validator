from maya import cmds


class MayaValidationContext:
    def __init__(self) -> None:
        self._joints: list[str] | None = None

    def get_joints(self) -> list[str]:
        if self._joints is None:
            self._joints = cmds.ls(type="joint", long=True)

        joints = self._joints
        assert joints is not None

        return joints