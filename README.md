# payloadbox-ultra — XSS Payload List (Ultra Edition)

Projeto com foco em:
- Estrutura JSON rica (metadados, score, encodings)
- Exportadores: CSV, YAML, XML, Burp, ZAP, JSONL
- Gerador de variantes "AI-lite" (Markov + mutações fingerprint-aware)
- CLI empacotável (xssbox) para export, serve-docs, generate-variants
- Site estático (docs/) com busca Lunr + preview seguro
- Testes automatizados de sanitização e CI para validação + publish Pages

Uso responsável
- Use apenas em sistemas que você tem permissão de testar.
- Consulte SECURITY.md antes de divulgar PoCs.

Como começar (local)
1. Clone o repositório localmente.
2. Criar virtualenv e instalar deps:
   python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
3. Validar payloads:
   python tools/exporters.py --input payloads/payloads.json --formats csv,jsonl --outdir exports
4. Gerar variantes:
   python tools/variant_ai.py --input payloads/payloads.json --out exports/variants.jsonl
5. Servir docs localmente:
   python -m http.server 8000 --directory docs


