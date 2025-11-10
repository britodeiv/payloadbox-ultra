#!/usr/bin/env python3
"""
tools/exporters.py
Exporta payloads para CSV, YAML, XML, Burp, ZAP e JSONL.
Uso:
  python tools/exporters.py --input payloads/payloads.json --outdir exports --formats csv,yaml,xml,burp,zap,jsonl
"""
import argparse, json, csv
from pathlib import Path
import yaml
import xml.etree.ElementTree as ET

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def to_csv(data, path):
    keys = ["id","payload","context","vector","tags","severity","score","source","created_at","version"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for item in data:
            row = []
            for k in keys:
                v = item.get(k, "")
                if isinstance(v, list): v = " | ".join(v)
                row.append(v)
            writer.writerow(row)

def to_yaml(data, path):
    Path(path).write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")

def to_xml(data, path):
    root = ET.Element("payloads")
    for item in data:
        p = ET.SubElement(root, "payload", attrib={"id": item.get("id","")})
        for k,v in item.items():
            if isinstance(v, list):
                sub = ET.SubElement(p, k)
                for val in v:
                    it = ET.SubElement(sub, "item"); it.text = str(val)
            else:
                el = ET.SubElement(p, k); el.text = str(v)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

def to_burp(data, path):
    Path(path).write_text("\n".join([p["payload"] for p in data]), encoding="utf-8")

def to_zap(data, path):
    zap = [{"name": p["id"], "payload": p["payload"], "description": p.get("notes","")} for p in data]
    Path(path).write_text(json.dumps(zap, ensure_ascii=False, indent=2), encoding="utf-8")

def to_jsonl(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--outdir", default="exports")
    ap.add_argument("--formats", default="csv,yaml,xml")
    args = ap.parse_args()
    data = load(args.input)
    out = Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    fmts = args.formats.split(",")
    if "csv" in fmts: to_csv(data, out/"payloads.csv")
    if "yaml" in fmts: to_yaml(data, out/"payloads.yaml")
    if "xml" in fmts: to_xml(data, out/"payloads.xml")
    if "burp" in fmts: to_burp(data, out/"payloads-burp.txt")
    if "zap" in fmts: to_zap(data, out/"payloads-zap.json")
    if "jsonl" in fmts: to_jsonl(data, out/"payloads.jsonl")
    print("Export concluído em", str(out))

if __name__ == "__main__":
    main()
