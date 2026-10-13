"""Deterministic permission checks for ASTRA's first prototype.

This module decides whether an action is allowed. It does not execute commands
or modify files. Execution will be added only after these decisions are tested.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class PermissionDecision:
    """The result of one permission check."""

    allowed: bool
    reason: str


class PermissionPolicy:
    """The locked M0 permission boundary for a local target repository."""

    _ALLOWED_TEST_COMMAND = ("npm.cmd", "test")
    _ALLOWED_GIT_OPERATIONS = frozenset({"status", "history", "diff"})

    def __init__(self, target_root: Path, evidence_root: Path) -> None:
        self.target_root = target_root.resolve()
        self.evidence_root = evidence_root.resolve()

    def check_read(self, path: Path) -> PermissionDecision:
        """Allow reads only for paths inside the approved target repository."""

        if self._is_inside(path, self.target_root):
            return self._allow("read is inside the approved target repository")

        return self._deny("read is outside the approved target repository")

    def check_git_read(self, operation: str) -> PermissionDecision:
        """Allow only read-only Git observations defined by the M0 contract."""

        if operation in self._ALLOWED_GIT_OPERATIONS:
            return self._allow(f"git {operation} is an approved read-only operation")

        return self._deny(f"git {operation} is not an approved read-only operation")

    def check_test_command(
        self, command: Sequence[str], cwd: Path
    ) -> PermissionDecision:
        """Allow only the exact target test command from the target root."""

        resolved_cwd = cwd.resolve()
        normalized_command = tuple(command)

        if resolved_cwd != self.target_root:
            return self._deny("test command must run from the approved target root")

        if normalized_command != self._ALLOWED_TEST_COMMAND:
            return self._deny("only npm.cmd test is allowlisted for the prototype")

        return self._allow("npm.cmd test is allowlisted for the target root")

    def check_write(
        self,
        path: Path,
        approved_paths: Iterable[Path],
        human_approved: bool,
    ) -> PermissionDecision:
        """Allow writes only after approval and only to planned target files."""

        if not human_approved:
            return self._deny("human approval is required before writing target files")

        resolved_path = path.resolve()
        if not self._is_inside(resolved_path, self.target_root):
            return self._deny("write is outside the approved target repository")

        resolved_approved_paths = {
            approved_path.resolve() for approved_path in approved_paths
        }
        if resolved_path not in resolved_approved_paths:
            return self._deny("target file is not included in the approved plan")

        return self._allow("write is approved for a planned target file")

    def check_evidence_write(self, path: Path) -> PermissionDecision:
        """Allow evidence writes only inside ASTRA's run directory."""

        if self._is_inside(path, self.evidence_root):
            return self._allow("evidence write is inside astra-system/runs")

        return self._deny("evidence write is outside astra-system/runs")

    def check_denied_action(self, action: str) -> PermissionDecision:
        """Reject actions that are outside the M0 prototype boundary."""

        return self._deny(f"{action} is blocked by the M0 permission boundary")

    @staticmethod
    def _is_inside(path: Path, root: Path) -> bool:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
        return True

    @staticmethod
    def _allow(reason: str) -> PermissionDecision:
        return PermissionDecision(allowed=True, reason=reason)

    @staticmethod
    def _deny(reason: str) -> PermissionDecision:
        return PermissionDecision(allowed=False, reason=reason)
