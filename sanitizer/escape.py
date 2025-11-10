"""
sanitizer/escape.py
Funções de escape simples usadas nos testes automatizados.
"""
import html
def simple_escape(s: str, context: str = "html") -> str:
    if context == "html":
        return html.escape(s, quote=True)
    elif context == "attr":
        return html.escape(s, quote=True).replace('"', "&quot;")
    elif context == "url":
        from urllib.parse import quote_plus
        return quote_plus(s)
    else:
        return s
