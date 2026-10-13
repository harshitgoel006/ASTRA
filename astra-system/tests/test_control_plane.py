from astra.control_plane import get_system_identity


def test_control_plane_has_foundation_identity() -> None:
    identity = get_system_identity()

    assert identity.name == "ASTRA"
    assert identity.version == "0.1.0"
    assert identity.status == "foundation"
