# Contribuindo

Obrigado por contribuir! Siga estas diretrizes:

- Adicione payloads em payloads/payloads.json seguindo payloads/payloads.schema.json.
- Execute validação local antes de PR:
  - pip install -r requirements.txt
  - python -c "from jsonschema import validate; import json; validate(json.load(open('payloads/payloads.json')), json.load(open('payloads/payloads.schema.json')))"
  - pytest
- Para adicionar novos recursos: crie branches pequenos e focados.
- Inclua referência/origem em cada payload quando aplicável.

Aviso: não inclua PoCs que você não tem permissão de divulgar.
