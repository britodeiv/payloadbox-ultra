#!/usr/bin/env python3
"""cli/xssbox.py - ferramenta CLI mínima para export, serve-docs e generate-variants
Exemplos:
  python cli/xssbox.py export --formats csv,jsonl
  python cli/xssbox.py variants --max-per 50 --seed 42
  python cli/xssbox.py serve --port 8000
"""
import argparse, subprocess, sys
from pathlib import Path

def export_cmd(args):
    sys.argv = ["tools/exporters.py", "--input", "payloads/payloads.json", "--outdir", "exports", "--formats", args.formats]
    import tools.exporters as ex; ex.main()

def variants_cmd(args):
    sys.argv = ["tools/variant_ai.py", "--input", "payloads/payloads.json", "--out", "exports/variants.jsonl", "--max-per", str(args.max_per), "--seed", str(args.seed)]
    import tools.variant_ai as va; va.main()

def serve_cmd(args):
    docs = Path("docs")
    if not docs.exists():
        print("docs/ não existe. Gere o site em docs/ antes.")
        return
    print(f"Servindo docs/ em http://localhost:{args.port}")
    subprocess.run(["python3","-m","http.server", str(args.port)], cwd=str(docs))

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    e = sub.add_parser("export"); e.add_argument("--formats", default="csv,yaml,xml,burp,zap,jsonl")
    v = sub.add_parser("variants"); v.add_argument("--max-per", type=int, default=20); v.add_argument("--seed", type=int, default=0)
    s = sub.add_parser("serve"); s.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    if args.cmd == "export": export_cmd(args)
    elif args.cmd == "variants": variants_cmd(args)
    elif args.cmd == "serve": serve_cmd(args)
    else: ap.print_help()

if __name__ == "__main__":
    main()
