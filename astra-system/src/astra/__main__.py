from .control_plane import get_system_identity


def main() -> None:
    identity = get_system_identity()
    print(f"{identity.name} {identity.version} - {identity.status}")


if __name__ == "__main__":
    main()
