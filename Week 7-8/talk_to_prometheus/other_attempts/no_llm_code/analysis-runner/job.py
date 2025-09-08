#!/usr/bin/env python3
# Small analysis job that computes descriptive stats for a data key.
import argparse, json, os
import numpy as np

def compute_summary(payload):
    out = {}
    series = payload.get("data", {}).get("result", [])
    for s in series:
        metric = s.get("metric", {})
        name = metric.get("__name__", "series")
        values = [float(v[1]) for v in s.get("values", [])] if s.get("values") else []
        if not values:
            continue
        arr = np.array(values)
        out[name] = {
            "min": float(arr.min()),
            "max": float(arr.max()),
            "mean": float(arr.mean()),
            "p50": float(np.percentile(arr, 50)),
            "p95": float(np.percentile(arr, 95)),
            "count": int(arr.size)
        }
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to data file (JSON)")
    parser.add_argument("--key", required=True, help="Data key to analyze")
    args = parser.parse_args()
    if not os.path.exists(args.file):
        print(json.dumps({"error": "file-not-found"}))
        return
    doc = json.load(open(args.file, "r"))
    payload = doc.get("data", {}).get(args.key)
    if not payload:
        print(json.dumps({"error": "key-not-found"}))
        return
    summary = compute_summary(payload.get("data", payload))
    print(json.dumps({"summary": summary}))

if __name__ == "__main__":
    main()
