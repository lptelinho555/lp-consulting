# -*- coding: utf-8 -*-
"""Troca o dominio do site em todos os arquivos.

Uso:
    python scripts/set-domain.py meusite.com

Atualiza canonical, hreflang, Open Graph, sitemap.xml, robots.txt,
o redirect dos formularios e o arquivo CNAME do GitHub Pages.
"""
import pathlib
import re
import sys

PLACEHOLDER = "SEU-DOMINIO.com"
ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTS = {".html", ".xml", ".txt"}


def current_domain():
    """Descobre o dominio em uso (o CNAME manda; senao, o placeholder)."""
    cname = ROOT / "CNAME"
    if cname.exists():
        value = cname.read_text(encoding="utf-8").strip()
        if value:
            return value
    return PLACEHOLDER


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1

    new = sys.argv[1].strip().lower()
    new = re.sub(r"^https?://", "", new).rstrip("/")

    if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", new):
        print("Dominio invalido: %r  (esperado algo como meusite.com)" % new)
        return 1

    old = current_domain()
    if old == new:
        print("O dominio ja e %s — nada a fazer." % new)
        return 0

    changed = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in EXTS:
            continue
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if old not in text:
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")
        changed.append(str(path.relative_to(ROOT)))

    # CNAME: e o que diz ao GitHub Pages qual dominio servir
    (ROOT / "CNAME").write_text(new + "\n", encoding="utf-8")

    print("Dominio: %s  ->  %s" % (old, new))
    print("Arquivos atualizados: %d" % len(changed))
    print("CNAME gravado.")
    print("\nAgora: git add -A && git commit -m 'Define dominio %s' && git push" % new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
