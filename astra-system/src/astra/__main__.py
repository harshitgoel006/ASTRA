"""Command-line entry point for the ASTRA control plane."""

import argparse
import sys
from collections.abc import Sequence

from .control_plane import get_system_identity
from .model_gateway import ModelGatewayError
from .runtime import (
    DEFAULT_SYSTEM_PROMPT,
    DEFAULT_USER_PROMPT,
    DEFAULT_EVIDENCE_PATH,
    run_model_call,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m astra")
    subparsers = parser.add_subparsers(dest="command")
    model_call_parser = subparsers.add_parser(
        "model-call",
        help="run one bounded call through the configured local model gateway",
    )
    model_call_parser.add_argument("prompt", nargs="?", default=DEFAULT_USER_PROMPT)
    model_call_parser.add_argument(
        "--system-prompt",
        default=DEFAULT_SYSTEM_PROMPT,
    )

    args = parser.parse_args(argv)
    if args.command == "model-call":
        try:
            response = run_model_call(
                args.prompt,
                system_prompt=args.system_prompt,
            )
        except ModelGatewayError as exc:
            print(f"[ASTRA model runtime] error: {exc}", file=sys.stderr)
            return 1

        print(response.content)
        print(f"[ASTRA model runtime] evidence: {DEFAULT_EVIDENCE_PATH}")
        return 0

    identity = get_system_identity()
    print(f"[ASTRA control plane] identity: {identity.name} {identity.version}")
    print(f"[ASTRA control plane] status: {identity.status}")
    print("[ASTRA control plane] target repository access: not connected yet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
