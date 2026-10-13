from pathlib import Path

from astra.permissions import PermissionPolicy


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TARGET_ROOT = PROJECT_ROOT / "test-repo"
EVIDENCE_ROOT = PROJECT_ROOT / "astra-system" / "runs"


def make_policy() -> PermissionPolicy:
    return PermissionPolicy(TARGET_ROOT, EVIDENCE_ROOT)


def test_read_inside_target_repository_is_allowed() -> None:
    decision = make_policy().check_read(TARGET_ROOT / "server" / "models" / "task.js")

    assert decision.allowed is True
    assert "approved target repository" in decision.reason


def test_read_outside_target_repository_is_denied() -> None:
    decision = make_policy().check_read(PROJECT_ROOT / "README.md")

    assert decision.allowed is False
    assert "outside" in decision.reason


def test_only_read_only_git_operations_are_allowed() -> None:
    policy = make_policy()

    assert policy.check_git_read("status").allowed is True
    assert policy.check_git_read("history").allowed is True
    assert policy.check_git_read("diff").allowed is True
    assert policy.check_git_read("push").allowed is False


def test_exact_target_test_command_is_allowed() -> None:
    decision = make_policy().check_test_command(
        ("npm.cmd", "test"),
        TARGET_ROOT,
    )

    assert decision.allowed is True


def test_test_command_is_denied_from_wrong_directory() -> None:
    decision = make_policy().check_test_command(
        ("npm.cmd", "test"),
        PROJECT_ROOT,
    )

    assert decision.allowed is False
    assert "target root" in decision.reason


def test_unallowlisted_test_command_is_denied() -> None:
    decision = make_policy().check_test_command(
        ("npm.cmd", "install"),
        TARGET_ROOT,
    )

    assert decision.allowed is False
    assert "allowlisted" in decision.reason


def test_write_requires_human_approval_and_approved_path() -> None:
    policy = make_policy()
    target_file = TARGET_ROOT / "server" / "services" / "taskService.js"

    assert policy.check_write(target_file, [target_file], False).allowed is False
    assert policy.check_write(target_file, [target_file], True).allowed is True
    assert policy.check_write(
        TARGET_ROOT / "server" / "models" / "task.js",
        [target_file],
        True,
    ).allowed is False


def test_evidence_write_is_limited_to_astra_runs() -> None:
    policy = make_policy()

    assert policy.check_evidence_write(EVIDENCE_ROOT / "run.json").allowed is True
    assert policy.check_evidence_write(TARGET_ROOT / "run.json").allowed is False


def test_blocked_actions_are_denied_with_a_reason() -> None:
    decision = make_policy().check_denied_action("network access")

    assert decision.allowed is False
    assert "blocked" in decision.reason
