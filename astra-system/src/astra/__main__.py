from .control_plane import get_system_identity


def main() -> None:
    identity = get_system_identity()
    print(f"[ASTRA control plane] identity: {identity.name} {identity.version}")
    print(f"[ASTRA control plane] status: {identity.status}")
    print("[ASTRA control plane] target repository access: not connected yet")


if __name__ == "__main__":
    main()
