#!/usr/bin/env python3
"""Recover saved outputs (not experiment execution) from an executed .ipynb.

The generated image/HTML/text files are historical notebook display artifacts.
A displayed/truncated HTML table is NOT a complete original Kaggle CSV export.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path


def _text(value):
    return "".join(value) if isinstance(value, list) else str(value)


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def recover_notebook_outputs(notebook_path, output_dir):
    source = Path(notebook_path)
    raw = source.read_bytes()
    notebook = json.loads(raw)
    if not isinstance(notebook.get("cells"), list):
        raise ValueError("Notebook JSON must contain a cells list")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source_notebook": source.name,
        "source_sha256": _sha256(raw),
        "source_size_bytes": len(raw),
        "method": "Saved Jupyter output extraction; no model fitting or rerunning",
        "scientific_validation": "UNVERIFIED_HISTORICAL_NOTEBOOK_DISPLAYS",
        "files": [],
        "errors": [],
        "code_cells": 0,
        "png_figures": 0,
        "html_displays": 0,
        "stream_text_files": 0,
    }

    def save(relative, payload, *, cell, output, mimetype):
        dest = out / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(payload)
        manifest["files"].append({
            "path": relative.as_posix(),
            "cell_index_zero_based": cell,
            "cell_number_one_based": cell + 1,
            "output_index_one_based": output + 1,
            "media_type": mimetype,
            "bytes": len(payload),
            "sha256": _sha256(payload),
        })

    for i, cell in enumerate(notebook["cells"]):
        if cell.get("cell_type") != "code":
            continue
        manifest["code_cells"] += 1
        for j, record in enumerate(cell.get("outputs", [])):
            base = Path(f"cell_{i:03d}") / f"output_{j+1:02d}"
            kind = record.get("output_type")
            if kind == "stream":
                save(base.with_suffix(".txt"), _text(record.get("text", "")).encode("utf8"),
                     cell=i, output=j, mimetype="text/plain")
                manifest["stream_text_files"] += 1
            elif kind == "error":
                error = "\n".join(_text(line) for line in record.get("traceback", []))
                save(base.with_name(base.name + "_error.txt"), error.encode("utf8"),
                     cell=i, output=j, mimetype="text/plain+traceback")
                manifest["errors"].append({
                    "cell_index_zero_based": i, "ename": record.get("ename"),
                    "evalue": record.get("evalue"),
                })
            data = record.get("data") or {}
            if "image/png" in data:
                encoded = _text(data["image/png"]).replace("\n", "")
                png = base64.b64decode(encoded, validate=True)
                if not png.startswith(b"\x89PNG\r\n\x1a\n"):
                    raise ValueError(f"Invalid image/png signature in cell {i}, output {j}")
                save(base.with_suffix(".png"), png, cell=i, output=j, mimetype="image/png")
                manifest["png_figures"] += 1
            for mime, suffix in (
                ("image/svg+xml", ".svg"),
                ("text/html", ".html"),
                ("text/plain", "_display.txt"),
            ):
                if mime not in data:
                    continue
                relative = base.with_suffix(suffix) if suffix.startswith(".") else base.with_name(base.name + suffix)
                save(relative, _text(data[mime]).encode("utf8"),
                     cell=i, output=j, mimetype=mime)
                if mime == "text/html":
                    manifest["html_displays"] += 1

    (out / "RECOVERY_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf8"
    )
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", required=True, help="Original executed .ipynb path")
    parser.add_argument("--output-dir", default="results/notebook_recovered/raw_outputs")
    parser.add_argument("--expected-png", type=int)
    parser.add_argument("--expected-html", type=int)
    args = parser.parse_args(argv)
    manifest = recover_notebook_outputs(args.notebook, args.output_dir)
    if args.expected_png is not None and manifest["png_figures"] != args.expected_png:
        parser.error(f"Expected {args.expected_png} PNGs, found {manifest['png_figures']}")
    if args.expected_html is not None and manifest["html_displays"] != args.expected_html:
        parser.error(f"Expected {args.expected_html} HTML displays, found {manifest['html_displays']}")
    print(json.dumps({k: manifest[k] for k in ("source_sha256", "code_cells", "png_figures",
                                               "html_displays", "stream_text_files", "errors")}, indent=2))


if __name__ == "__main__":
    main()
