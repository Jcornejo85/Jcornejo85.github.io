# -*- coding: utf-8 -*-
"""Genera index.html, generic.html y una página por proyecto a partir de tools/content.py.

Uso:  python3 tools/build.py
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from content import PROJECTS, PREVIOUS  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LINKEDIN = "https://www.linkedin.com/in/juanmanuelcornejociruelo/"
GITHUB = "https://github.com/Jcornejo85"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"


def L(es, en, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag} data-l="es"{c}>{es}</{tag}><{tag} data-l="en"{c}>{en}</{tag}>'


def head(title_es, title_en, mermaid=False):
    m = f'\n\t\t<script src="{MERMAID}" defer></script>' if mermaid else ""
    return f"""<!DOCTYPE HTML>
<!--
	Massively by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
	Generado con tools/build.py — editar tools/content.py, no este archivo.
-->
<html lang="es" data-lang="es">
	<head>
		<title data-es="{html.escape(title_es)}" data-en="{html.escape(title_en)}">{html.escape(title_es)}</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<link rel="stylesheet" href="assets/css/main.css" />
		<link rel="stylesheet" href="assets/css/portfolio.css" />
		<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>{m}
		<script src="assets/js/portfolio.js" defer></script>
	</head>
	<body class="is-preload">
		<div id="wrapper"{' class="fade-in"' if title_es.startswith('Juan') else ''}>
"""


def nav(active):
    def li(key, href, es, en):
        a = ' class="active"' if key == active else ""
        return f'<li{a}><a href="{href}">{L(es, en)}</a></li>'

    return f"""
				<header id="header">
					<a href="index.html" class="logo">Juan Manuel Cornejo</a>
				</header>
				<nav id="nav">
					<ul class="links">
						{li('projects', 'index.html', 'Proyectos', 'Projects')}
						{li('about', 'generic.html', 'Sobre mí', 'About me')}
					</ul>
					<ul class="icons">
						<li><a href="{LINKEDIN}" class="icon brands fa-linkedin"><span class="label">LinkedIn</span></a></li>
						<li><a href="{GITHUB}" class="icon brands fa-github"><span class="label">GitHub</span></a></li>
						<li class="lang-switch"><a href="#" class="lang-btn" role="button">EN</a></li>
					</ul>
				</nav>
"""


FOOT = f"""
				<footer id="footer">
					<section class="split contact">
						<section class="alt">
							<h3>{L('Ubicación', 'Location')}</h3>
							<p>Madrid, {L('España', 'Spain')}</p>
						</section>
						<section>
							<h3>{L('Teléfono', 'Phone')}</h3>
							<p><a href="tel:+34600325300">(+34) 600325300</a></p>
						</section>
						<section>
							<h3>Email</h3>
							<p><a href="mailto:juanm.cornejoc@gmail.com">juanm.cornejoc@gmail.com</a></p>
						</section>
						<section>
							<h3>{L('Redes', 'Social')}</h3>
							<ul class="icons alt">
								<li><a href="{LINKEDIN}" class="icon brands alt fa-linkedin"><span class="label">LinkedIn</span></a></li>
								<li><a href="{GITHUB}" class="icon brands alt fa-github"><span class="label">GitHub</span></a></li>
							</ul>
						</section>
					</section>
				</footer>
				<div id="copyright">
					<ul><li>&copy; Juan Manuel Cornejo</li><li>Design: <a href="https://html5up.net">HTML5 UP</a></li></ul>
				</div>
			</div>
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/browser.min.js"></script>
			<script src="assets/js/breakpoints.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>
	</body>
</html>
"""


def chips(items):
    return '<ul class="chips">' + "".join(f"<li>{html.escape(c)}</li>" for c in items) + "</ul>"


def media(p, n=""):
    v = p["video"]
    if v:
        note = L(
            "Recorrido real por la app. El repositorio es privado: abajo se explica cómo funciona por dentro.",
            "Real walkthrough of the app. The repository is private: how it works inside is explained below.",
            "p", "demo-note")
        return (f'<div class="demo-video"><video controls playsinline preload="metadata" poster="{v["poster"]}">'
                f'<source src="{v["src"]}" type="video/mp4" /></video></div>\n{note}')
    ill = p.get("illustration")
    if ill:
        alt = html.escape(p["name"])
        return (f'<figure class="demo-illustration">'
                f'<img data-l="es" src="{ill["es"]}" alt="{alt}" /><img data-l="en" src="{ill["en"]}" alt="{alt}" /></figure>')
    return (f'<div class="demo-pending"><img src="{p["cover"]}" alt="{html.escape(p["name"])}" />'
            f'{L("Demo en vídeo próximamente.", "Video demo coming soon.", "p")}</div>')


def project_page(p):
    s = p["slug"]
    tag_es, tag_en = p["tagline"]
    facts = "".join(f"<div><b>{v}</b>{L(es, en)}</div>" for v, es, en in p["facts"])
    what_es = "".join(f"<p>{x}</p>" for x in p["what"][0])
    what_en = "".join(f"<p>{x}</p>" for x in p["what"][1])
    decisions = "".join(
        f"<li>{L(f'<strong>{tes}.</strong> {bes}', f'<strong>{ten}.</strong> {ben}')}</li>"
        for tes, bes, ten, ben in p["decisions"]
    )
    flow_es, flow_en = p["flow"]
    arch_es, arch_en = p["arch"]
    live = ""
    if p["link"]:
        live = (f'<li><a href="{p["link"]}" class="button primary large" target="_blank" rel="noopener">'
                f'{L("Abrir la app", "Open the app")}</a></li>')
    actions = f"""<ul class="actions special">{live}<li><a href="index.html#projects" class="button large">{L('Ver todos los proyectos', 'All projects')}</a></li></ul>"""

    body = f"""
				<div id="main">
					<section class="post">
						<header class="major">
							<h1>{html.escape(p['name'])}</h1>
							<p class="project-tagline">{L(tag_es, tag_en)}</p>
							<p><span class="badge-private">{L('Repositorio privado', 'Private repository')}</span></p>
						</header>
						{chips(p['chips'])}
						{media(p)}
						<div class="project-facts">{facts}</div>

						<h2>{L('Qué es', 'What it is')}</h2>
						<div data-l="es">{what_es}</div>
						<div data-l="en">{what_en}</div>

						<h2>{L('Cómo funciona', 'How it works')}</h2>
						<div class="diagram"><div id="flow-es" data-l="es"><p class="diagram-loading">Cargando diagrama…</p></div><div id="flow-en" data-l="en"><p class="diagram-loading">Loading diagram…</p></div></div>
						<script type="text/x-mermaid" data-target="flow-es">
{flow_es}</script>
						<script type="text/x-mermaid" data-target="flow-en">
{flow_en}</script>

						<details class="arch">
							<summary>{L('Arquitectura técnica', 'Technical architecture')}</summary>
							<div class="diagram"><div id="arch-es" data-l="es"></div><div id="arch-en" data-l="en"></div></div>
						</details>
						<script type="text/x-mermaid" data-target="arch-es">
{arch_es}</script>
						<script type="text/x-mermaid" data-target="arch-en">
{arch_en}</script>

						<h2>{L('Decisiones técnicas', 'Technical decisions')}</h2>
						<ul class="decisions">{decisions}</ul>

						{actions}
					</section>
				</div>
"""
    out = head(f"{p['name']} · Juan Manuel Cornejo", f"{p['name']} · Juan Manuel Cornejo", mermaid=True) + nav(None) + body + FOOT
    with open(os.path.join(ROOT, f"{s}.html"), "w", encoding="utf-8") as f:
        f.write(out)


def index_page():
    posts = []
    for p in PROJECTS:
        es, en = p["card"]
        posts.append(f"""
							<article>
								<header>
									<h2><a href="{p['slug']}.html">{html.escape(p['name'])}</a></h2>
								</header>
								<a href="{p['slug']}.html" class="image fit"><img src="{p['cover']}" alt="{html.escape(p['name'])}" loading="lazy" /></a>
								{chips(p['chips'][:5])}
								{L(es, en, 'p')}
								<ul class="actions special">
									<li><a href="{p['slug']}.html" class="button">{L('Ver proyecto', 'View project')}</a></li>
								</ul>
							</article>""")
    prev = []
    for q in PREVIOUS:
        nes, nen = q["name"]
        des, den = q["desc"]
        ext = q["href"].startswith("http")
        tgt = ' target="_blank" rel="noopener"' if ext else ""
        prev.append(f"""
							<article>
								<header><h2><a href="{q['href']}"{tgt}>{L(nes, nen)}</a></h2></header>
								<a href="{q['href']}" class="image fit"{tgt}><img src="{q['img']}" alt="" loading="lazy" /></a>
								{L(des, den, 'p')}
								<ul class="actions special"><li><a href="{q['href']}" class="button small"{tgt}>{L('Ver', 'View')}</a></li></ul>
							</article>""")

    body = f"""
				<div id="intro">
					<h1>Juan Manuel Cornejo</h1>
					<p>{L('Data Scientist especializado en <strong>IA generativa</strong>: sistemas con LLM, RAG y agentes, del prototipo a producción.',
                          'Data Scientist specialised in <strong>generative AI</strong>: LLM systems, RAG and agents, from prototype to production.')}</p>
					<ul class="actions">
						<li><a href="#header" class="button icon solid solo fa-arrow-down scrolly">{L('Continuar', 'Continue')}</a></li>
					</ul>
				</div>
{nav('projects')}
				<div id="main">
					<article class="post featured" id="projects">
						<header class="major">
							<h2>{L('Proyectos recientes', 'Recent projects')}</h2>
							<p>{L('Cuatro aplicaciones completas diseñadas y desarrolladas por mí en 2026. Los repositorios son privados, así que cada proyecto tiene una demo y una explicación de cómo funciona por dentro.',
                                  'Four complete applications I designed and built in 2026. The repositories are private, so each project comes with a demo and an explanation of how it works inside.')}</p>
						</header>
					</article>
					<section class="posts">{''.join(posts)}
					</section>

					<article class="post featured" id="previous">
						<header class="major">
							<h2>{L('Proyectos anteriores', 'Previous projects')}</h2>
							<p>{L('Machine learning y análisis de datos (2021–2022).', 'Machine learning and data analysis (2021–2022).')}</p>
						</header>
					</article>
					<section class="posts previous">{''.join(prev)}
					</section>
				</div>
"""
    out = head("Juan Manuel Cornejo · Portfolio", "Juan Manuel Cornejo · Portfolio") + body + FOOT
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)


def about_page():
    es = """
						<p>Soy <strong>Data Scientist Expert en Verisure</strong>, dentro del AI Center of Excellence, donde lidero proyectos internacionales de IA generativa: análisis de imágenes con LLM, speech analytics y un chatbot RAG con capacidades agénticas para un servicio interno.</p>
						<p>Antes trabajé como Data Analyst en Cobee (hoy parte de Pluxee) y, durante más de seis años, en el sector financiero. Me reconvertí a la tecnología en el campus 42 Madrid, con especialización en Data Science.</p>
						<p>Fuera del trabajo construyo mis propias aplicaciones de principio a fin —producto, arquitectura, IA y despliegue—, que son las que encontrarás en este portfolio. Me interesa especialmente que la IA sea fiable: medir antes de cambiar, controlar el coste y diseñar para que el modelo no invente.</p>
"""
    en = """
						<p>I'm a <strong>Data Scientist Expert at Verisure</strong>, in the AI Center of Excellence, where I lead international generative-AI projects: LLM-based image analysis, speech analytics and a RAG chatbot with agentic capabilities for an internal service.</p>
						<p>Before that I worked as a Data Analyst at Cobee (now part of Pluxee) and spent more than six years in the financial sector. I moved into tech through the 42 Madrid campus, specialising in Data Science.</p>
						<p>Outside work I build my own applications end to end —product, architecture, AI and deployment—, which are the ones you'll find in this portfolio. I care most about reliable AI: measuring before changing, keeping costs under control and designing so the model doesn't make things up.</p>
"""
    body = f"""
				<div id="main">
					<section class="post">
						<header class="major">
							<h1>{L('Sobre mí', 'About me')}</h1>
						</header>
						<div class="image main"><img src="images/ABOUTME.jpg" alt="" /></div>
						<div data-l="es">{es}</div>
						<div data-l="en">{en}</div>
						<ul class="actions special">
							<li><a href="{LINKEDIN}" class="button large">LinkedIn</a></li>
							<li><a href="index.html#projects" class="button large">{L('Ver proyectos', 'View projects')}</a></li>
						</ul>
					</section>
				</div>
"""
    out = head("Sobre mí · Juan Manuel Cornejo", "About me · Juan Manuel Cornejo") + nav("about") + body + FOOT
    with open(os.path.join(ROOT, "generic.html"), "w", encoding="utf-8") as f:
        f.write(out)


if __name__ == "__main__":
    for p in PROJECTS:
        project_page(p)
    index_page()
    about_page()
    print("OK:", ", ".join(p["slug"] + ".html" for p in PROJECTS), "+ index.html + generic.html")
