#!/usr/bin/env python3
"""
tools/variant_ai.py
Gerador híbrido (Markov + mutações) para criar variantes originais.
Uso:
  python tools/variant_ai.py --input payloads/payloads.json --out exports/variants.jsonl --max-per 20 --seed 0
"""
import json, random, argparse, html, urllib.parse
from collections import defaultdict

def build_markov(corpus):
    M = defaultdict(list)
    for s in corpus:
        for i in range(len(s)-2):
            M[s[i:i+2]].append(s[i+2])
    return M

def markov_generate(M, length=40, seed=0):
    random.seed(seed)
    if not M:
        return ""
    k = random.choice(list(M.keys()))
    out = list(k)
    for _ in range(length):
        nxt = M.get("".join(out[-2:]), None)
        if not nxt: break
        out.append(random.choice(nxt))
    return "".join(out)

def mutate(payload, seed=0):
    random.seed(seed + (hash(payload) & 0xffffffff))
    ops = [
        lambda s: s.replace("<","&lt;"),
        lambda s: s.replace(">","&gt;"),
        lambda s: s.replace('"','\\"'),
        lambda s: s[::-1],
        lambda s: "".join(["\\u%04x"%ord(c) if ord(c)>127 else c for c in s]),
        lambda s: urllib.parse.quote_plus(s),
        lambda s: html.escape(s, quote=True)
    ]
    chosen = random.sample(ops, k=2)
    p = payload
    for op in chosen:
        p = op(p)
    p += random.choice(["","<!--@ultra-->","/*X*/",";!--"])
    return p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="exports/variants.jsonl")
    ap.add_argument("--max-per", type=int, default=20)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    data = json.load(open(args.input, encoding="utf-8"))
    corpus = [d["payload"] for d in data]
    M = build_markov(corpus)
    outp = open(args.out, "w", encoding="utf-8")
    for item in data:
        outp.write(json.dumps({"id": item["id"], "payload": item["payload"], "variant": item["payload"], "encoding": "none"}) + "\n")
        novel = markov_generate(M, length=min(60, max(20, len(item["payload"])*2)), seed=args.seed)
        outp.write(json.dumps({"id": item["id"], "payload": item["payload"], "variant": novel, "encoding": "markov"}) + "\n")
        for i in range(args.max_per):
            v = mutate(item["payload"], seed=args.seed + i)
            outp.write(json.dumps({"id": item["id"], "payload": item["payload"], "variant": v, "encoding": "mutate"}) + "\n")
    outp.close()
    print("Variants gerados em", args.out)

if __name__ == "__main__":
    main()
