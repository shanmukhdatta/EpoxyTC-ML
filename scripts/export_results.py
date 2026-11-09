#!/usr/bin/env python3
"""Checksum-verify and archive actual saved results; no computation is repeated."""
import argparse
import json
from deepoxy.reporting import export_verified_results


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--results-dir", default="results")
    p.add_argument("--zip", dest="destination", default="DEEPOXY_RESULTS_VERIFIED_FILES.zip")
    args = p.parse_args(argv)
    print(json.dumps(export_verified_results(args.results_dir, args.destination), indent=2))


if __name__ == "__main__":
    main()
