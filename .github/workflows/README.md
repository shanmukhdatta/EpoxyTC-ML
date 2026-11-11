# Continuous integration

[tests.yml](tests.yml) executes on pushes to main and on pull requests for Python 3.11 and 3.12. It compiles Python, runs pytest, validates three committed public CSVs and replays archived physics calculations. Full Kaggle GPU reruns and laboratory experimental uncertainty are outside the CI scope.

[Documentation](../../docs/reproducibility.md).
