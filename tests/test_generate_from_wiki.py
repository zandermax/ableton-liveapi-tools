import json
import os
from pathlib import Path

import pytest

import scripts.generate_from_wiki as gen


def test_apply_writes_outputs(tmp_path):
    outdir = tmp_path / "mcp_tool_defs"
    manifest_path = tmp_path / "docs" / "tool_manifest.json"

    # Run generator in apply mode to create artifacts in a temporary dir
    gen.main(["--apply", "--output-dir", str(outdir), "--manifest", str(manifest_path)])

    full_path = outdir / "full.json"
    assert full_path.exists(), "full.json was not written"

    data = json.loads(full_path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) > 0

    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "tools" in manifest
    assert isinstance(manifest["tools"], list)
    assert manifest["tools"] == data


def test_check_ok_and_detects_mismatch(tmp_path):
    outdir = tmp_path / "mcp_tool_defs"
    manifest_path = tmp_path / "docs" / "tool_manifest.json"

    # Generate canonical outputs first
    gen.main(["--apply", "--output-dir", str(outdir), "--manifest", str(manifest_path)])

    # Check should pass against the generated artifacts
    gen.main(["--output-dir", str(outdir), "--manifest", str(manifest_path), "--check"])

    # Introduce a deliberate mismatch in the manifest
    manifest_json = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest_json.get("tools"):
        manifest_json["tools"][0]["name"] = manifest_json["tools"][0]["name"] + "_MOD"
    else:
        manifest_json["tools"] = [{"name": "__MISMATCH__"}]
    manifest_path.write_text(json.dumps(manifest_json, indent=2), encoding="utf-8")

    # Now check should fail (SystemExit with non-zero code)
    with pytest.raises(SystemExit) as exc:
        gen.main(["--output-dir", str(outdir), "--manifest", str(manifest_path), "--check"])
    assert exc.value.code != 0
