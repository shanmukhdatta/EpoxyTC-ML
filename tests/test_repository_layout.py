"""Verify the user-requested flat repository structure remains importable."""
from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parents[1]
MODULES = [
    "data", "eda", "preprocessing", "models", "training",
    "augmentation", "evaluation", "physics", "diagnostics", "reporting"
]
FIGURES = [
    "augmentation_selected_delta_mae.svg",
    "cryogenic_gradientboosting_permutation_importance.svg",
    "cryogenic_nine_model_mean_fold_mae.svg",
    "cryogenic_ood_mae.svg",
    "high_temperature_exploratory_mae.svg",
    "record_counts_by_regime.svg",
    "room_nine_model_mean_fold_mae.svg",
]


def test_flat_src_package_and_module_imports():
    assert (ROOT / "src" / "__init__.py").is_file()
    assert (ROOT / "src" / "README.md").is_file()
    assert not (ROOT / "src" / "deepoxy").exists()
    for module in MODULES:
        assert (ROOT / "src" / f"{module}.py").is_file()
        assert importlib.import_module(f"src.{module}") is not None


def test_flat_figures_and_readme():
    assert (ROOT / "figures" / "README.md").is_file()
    assert not (ROOT / "figures" / "recovered").exists()
    for name in FIGURES:
        assert (ROOT / "figures" / name).is_file()
        assert f"]({name})" in (ROOT / "figures" / "README.md").read_text()
