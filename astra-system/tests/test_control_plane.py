from astra.control_plane import get_system_identity


def test_control_plane_reports_foundation_identity_only() -> None:
    identity = get_system_identity()

    assert identity.name == "ASTRA", (
        "control_plane.py must expose ASTRA as the control-plane name"
    )
    assert identity.version == "0.1.0", (
        "control_plane.py must expose the current foundation version"
    )
    assert identity.status == "foundation", (
        "control_plane.py must report the foundation status"
    )
