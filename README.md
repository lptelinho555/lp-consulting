# Luiz Paulo Consulting — site

Site institucional de consultoria remota em perfuração e desmonte de rochas.
HTML/CSS/JS estático, sem dependências externas, hospedado no GitHub Pages.

## Estrutura

```
index.html, services.html, ...   páginas em inglês (idioma padrão)
pt/  es/  zh/  ru/  ar/          traduções completas
blog/, pt/blog/, ...             3 artigos por idioma
css/style.css                    folha de estilo única
js/main.js                       menu mobile + ano do rodapé
404.html                         servido pelo GitHub Pages em qualquer nível
sitemap.xml, robots.txt          indexação
scripts/set-domain.py            troca o domínio em todo o site
```

62 páginas, 6 idiomas. O árabe usa `dir="rtl"`; o CSS usa propriedades
lógicas (`inset-inline-start`, `padding-inline-start`) para funcionar nos
dois sentidos de leitura.

## Rodar localmente

```bash
python -m http.server 8000
```

Abra <http://localhost:8000>. Ao editar o CSS, recarregue com `Ctrl+F5` —
o navegador guarda o `style.css` em cache de forma agressiva.

## Definir o domínio

O site é publicado com o marcador `SEU-DOMINIO.com`. Depois de registrar o
domínio real:

```bash
python scripts/set-domain.py meusite.com
```

Isso atualiza `canonical`, `hreflang`, Open Graph, `sitemap.xml`,
`robots.txt`, o redirecionamento dos formulários e grava o `CNAME` que o
GitHub Pages usa. Depois é só commitar e dar push.

No registrador do domínio, aponte o DNS para o GitHub Pages:

| Tipo | Nome | Valor |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `<usuário>.github.io` |

Em *Settings → Pages*, marque **Enforce HTTPS** assim que o certificado for
emitido (leva alguns minutos após o DNS propagar).

## Convenções

- **Links relativos**: páginas dentro de `pt/blog/` sobem **um** nível para
  chegar às páginas do próprio idioma (`../servicos.html`) e **dois** para
  chegar à raiz em inglês (`../../blog/post1.html`). Confundir isso já causou
  52 links quebrados uma vez.
- **Breakpoint do menu**: 1024px, definido em `css/style.css` e repetido em
  `js/main.js`. Alterar um exige alterar o outro.
- **Sem recursos externos**: nada de CDN, fontes ou scripts de terceiros — a
  CSP em cada página bloqueia. Ao adicionar algo externo, atualize a CSP.

## Formulário de contato

Usa [FormSubmit](https://formsubmit.co) (plano gratuito). O endpoint atual
expõe o e-mail no HTML; migrar para o endpoint com hash (`formsubmit.co/el/…`)
evita colheita por bots.
