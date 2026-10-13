"""Initial ASTRA control-plane identity.

The control plane will coordinate models, tools, permissions,
observations, verification and evidence in later milestones.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemIdentity:
    """Small deterministic description of the running ASTRA system."""

    name: str = "ASTRA"
    version: str = "0.1.0"
    status: str = "foundation"


def get_system_identity() -> SystemIdentity:
    """Return the current ASTRA control-plane identity."""

    return SystemIdentity()
