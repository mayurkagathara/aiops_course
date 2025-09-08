#!/usr/bin/env python3
# simple CLI runner for the teaching skeleton
import argparse
import json
from tasks import run_pipeline

def main():
    parser = argparse.ArgumentParser(prog="talk-to-prometheus")
    sub = parser.add_subparsers(dest="cmd")
    p1 = sub.add_parser("query", help="Run question end-to-end")
    p1.add_argument("question", type=str, help="Natural language question")
    p1.add_argument("--dry-run", action="store_true", help="Only produce plan, do not execute")
    args = parser.parse_args()
    if args.cmd == "query":
        analysis = run_pipeline(args.question, dry_run=args.dry_run)
        print(json.dumps(analysis, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
