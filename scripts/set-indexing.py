# -*- coding: utf-8 -*-
"""Liga ou desliga a indexacao do site pelos buscadores.

    python scripts/set-indexing.py off    # esconde do Google (endereco provisorio)
    python scripts/set-indexing.py on     # libera (usar so com o dominio definitivo)

Mexe na meta robots de todas as paginas e no robots.txt.
A pagina 404 fica sempre fora do indice, em qualquer modo.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = "<!-- indexing:off -->"
BLOCK = '    %s\n    <meta name="robots" content="noindex, nofollow">\n' % MARK
BLOCK_RE = re.compile(re.escape(MARK) + r'\n\s*<meta name="robots"[^>]*>\n', re.MULTILINE)
ANY_ROBOTS = re.compile(r'[ \t]*<meta name="robots"[^>]*>\n')

ROBOTS_OFF = """User-agent: *
Disallow: /
"""
ROBOTS_ON = """User-agent: *
Allow: /
Sitemap: https://SEU-DOMINIO.com/sitemap.xml
"""


def pages():
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" not in path.parts:
            yield path


def turn_off():
    changed = 0
    for path in pages():
        text = path.read_text(encoding="utf-8")
        if MARK in text:
            continue
        # tira qualquer meta robots existente para nao brigar com a nova
        text = ANY_ROBOTS.sub("", text)
        text, n = re.subn(r'(<meta name="viewport"[^>]*>\n)',
                          lambda m: m.group(1) + BLOCK, text, count=1)
        if n:
            path.write_text(text, encoding="utf-8")
            changed += 1
    (ROOT / "robots.txt").write_text(ROBOTS_OFF, encoding="utf-8")
    return changed


def turn_on():
    changed = 0
    for path in pages():
        text = path.read_text(encoding="utf-8")
        if MARK not in text:
            continue
        if path.name == "404.html":
            # a 404 nunca deve ser indexada; so troca o marcador
            text = text.replace(BLOCK.strip() + "\n",
                                '    <meta name="robots" content="noindex, follow">\n')
        else:
            text = BLOCK_RE.sub("", text)
        path.write_text(text, encoding="utf-8")
        changed += 1
    (ROOT / "robots.txt").write_text(ROBOTS_ON, encoding="utf-8")
    return changed


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("on", "off"):
        print(__doc__)
        return 1
    if sys.argv[1] == "off":
        n = turn_off()
        print("Indexacao DESLIGADA em %d paginas." % n)
        print("robots.txt agora bloqueia todos os buscadores.")
    else:
        n = turn_on()
        print("Indexacao LIGADA (%d paginas liberadas)." % n)
        print("Confirme que o dominio ja esta correto antes de publicar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
