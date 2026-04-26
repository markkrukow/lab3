from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "openapi" / "social_network_api.yaml"
SDK_DIR = ROOT / "sdk"
SDK_OUT = SDK_DIR / "social_network_client"


def run() -> int:
    if not SPEC_PATH.exists():
        print(f"[error] OpenAPI file not found: {SPEC_PATH}")
        return 1

    if shutil.which("openapi-python-client") is None:
        print("[error] 'openapi-python-client' is not installed.")
        print("Install it with: python -m pip install openapi-python-client")
        return 1

    SDK_DIR.mkdir(parents=True, exist_ok=True)
    if SDK_OUT.exists():
        shutil.rmtree(SDK_OUT)

    cmd = [
        "openapi-python-client",
        "generate",
        "--path",
        str(SPEC_PATH),
        "--output-path",
        str(SDK_OUT),
        "--meta",
        "none",
    ]
    print("[info] Running:", " ".join(cmd))
    completed = subprocess.run(cmd, cwd=ROOT)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(run())
