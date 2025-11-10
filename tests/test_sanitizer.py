import json
from sanitizer.escape import simple_escape
def test_escape_removes_script_tag():
    payload = "\"><script>alert(1)</script>"
    escaped = simple_escape(payload, "html")
    assert "<script>" not in escaped
def test_all_payloads_escaped_no_script():
    data = json.load(open("payloads/payloads.json", encoding="utf-8"))
    for p in data:
        e = simple_escape(p["payload"], "html")
        assert "<script>" not in e
