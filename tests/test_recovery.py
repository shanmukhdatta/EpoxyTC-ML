import base64
import json
from pathlib import Path
import importlib.util


def _load_recovery_script():
    path = Path(__file__).resolve().parents[1] / "scripts" / "recover_notebook_outputs.py"
    spec = importlib.util.spec_from_file_location("deepoxy_recover_outputs", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_recovers_genuine_png_html_and_stream_without_training(tmp_path):
    png = b"\x89PNG\r\n\x1a\n" + b"synthetic_fixture"
    notebook = {
        "cells": [{"cell_type": "code", "source": ["print(42)"], "execution_count": 2,
                   "outputs": [
                       {"output_type": "stream", "name": "stdout", "text": ["42\n"]},
                       {"output_type": "display_data", "data": {
                           "image/png": base64.b64encode(png).decode(),
                           "text/html": ["<table><tr><td>1</td></tr></table>"],
                       }}
                   ]}],
        "metadata": {}, "nbformat": 4, "nbformat_minor": 5,
    }
    source = tmp_path / "executed.ipynb"
    source.write_text(json.dumps(notebook), encoding="utf8")
    result = _load_recovery_script().recover_notebook_outputs(source, tmp_path / "recovered")
    assert result["png_figures"] == 1 and result["html_displays"] == 1
    assert result["stream_text_files"] == 1
    assert (tmp_path / "recovered" / "cell_000" / "output_02.png").read_bytes() == png
    assert len(result["files"]) == 3
