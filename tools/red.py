# -*- coding: utf-8 -*-
"""Portada inmersiva (index.html): la red neuronal que se recorre con el scroll.

La genera tools/build.py con los mismos datos de tools/content.py. El HTML lleva todo el contenido
escrito, así que sin WebGL o sin scripts la página se lee igual (modo «static» de assets/css/red.css).
La animación está en assets/js/red.js y los estilos en assets/css/red.css.
"""
import html
import os
import re

# Color de la neurona de cada proyecto, en el orden de PROJECTS (paleta violeta)
COLORS = ["#a98bff", "#cf6bff", "#ff7ad9", "#7d8cff", "#b77bff", "#e2d6ff"]

LIBS = """\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
\t\t<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
\t\t<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>
\t\t<script type="importmap">
\t\t{ "imports": {
\t\t\t"three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
\t\t\t"three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
\t\t} }
\t\t</script>
\t\t<script type="module" src="assets/js/red.js"></script>"""


def red_index(root, projects, previous, L, head, linkedin, github, desc):
    esc = html.escape

    def scene(i, p):
        s, color = p["slug"], COLORS[i % len(COLORS)]
        tag_es, tag_en = p["tagline"]
        facts = "".join(f"<div><dt>{v}</dt><dd>{L(es, en)}</dd></div>" for v, es, en in p["facts"][:4])
        chips = "".join(f"<li>{esc(c)}</li>" for c in p["chips"][:5])
        app = ""
        if p["link"]:
            app = f'<a class="btn btn-ghost" href="{p["link"]}" target="_blank" rel="noopener">{L("Abrir la app", "Open the app")}</a>'
        video = ""
        v = p.get("video")
        if v:
            video = f"""
						<figure class="scene-video">
							<button type="button" data-open="{s}" aria-label="{esc(p['name'])}: ver la demo y cómo funciona">
								<video muted loop playsinline preload="none" poster="{v['poster']}" data-src="{v['src']}"></video>
								<span class="vbadge"><svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3.5v9l7.5-4.5z" fill="currentColor"/></svg>{L('Ver demo y detalle', 'Watch demo and details')}</span>
							</button>
							<figcaption>{L('Demo real de la app', 'Real app demo')}</figcaption>
						</figure>"""
        return f"""
				<section class="scene" id="{s}" style="--ch:{color}" aria-label="{esc(p['name'])}">
					<div class="scene-text">
						<h2>{esc(p['name'])}</h2>
						<p class="tagline">{L(tag_es, tag_en)}</p>
						<dl class="facts">{facts}</dl>
						<ul class="chips">{chips}</ul>
						<div class="actions">
							<a class="btn btn-main" href="{s}.html" data-open="{s}">{L('Cómo funciona por dentro', 'How it works inside')}</a>
							{app}
						</div>
					</div>{video}
				</section>"""

    old = []
    for i, q in enumerate(previous):
        nes, nen = q["name"]
        des, den = q["desc"]
        tgt = ' target="_blank" rel="noopener"' if q["href"].startswith("http") else ""
        gh = q["href"].startswith("https://github.com")
        go = L("Ver en GitHub", "View on GitHub") if gh else L("Ver proyecto", "View project")
        old.append(f'<li><a href="{q["href"]}"{tgt}>'
                   f'<b>{L(nes, nen)}</b><small>{L(des, den)}</small><span class="open">{go}<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3h7v7M13 3 4 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span></a></li>')

    stops = ([("Inicio", "Start"), ("2021–2022", "2021–2022")] + [(p["name"], p["name"]) for p in projects]
             + [("Contacto", "Contact")])
    dots = "".join(f'<button type="button" aria-label="{esc(es)}" title="{esc(es)}"></button>' for es, _ in stops)

    body = f"""
		<canvas id="gl" aria-hidden="true"></canvas>
		<div class="veil" id="veil"></div>
		<nav class="top" aria-label="{esc('Opciones')}">
			<a href="proyectos.html">{L('Ver en lista', 'List view')}</a>
			<a href="#" class="lang-btn" role="button">EN</a>
		</nav>
		<main id="hud">
			<section class="intro shadow" id="intro">
				<h1>Juan Manuel Cornejo</h1>
				<p>{L('Data Scientist especializado en <strong>IA generativa</strong>: sistemas con LLM, RAG y agentes, del prototipo a producción.',
                      'Data Scientist specialised in <strong>generative AI</strong>: LLM systems, RAG and agents, from prototype to production.')}</p>
				<div class="hint"><i></i>{L('Desliza para entrar en la red', 'Scroll to enter the network')}</div>
			</section>

			<div class="year fx shadow" id="y2021" aria-hidden="true">2021<small>{L('Primeros modelos', 'First models')}</small></div>
			<section id="previous" aria-label="{esc('Proyectos anteriores')}">
				<h2 class="sr">{L('Proyectos anteriores (2021–2022)', 'Previous projects (2021–2022)')}</h2>
				<ol class="old">{''.join(old)}</ol>
			</section>
			<div class="year fx shadow" id="y2026" aria-hidden="true">2026<small>{L('IA generativa', 'Generative AI')}</small></div>
			<div id="labels"></div>
{''.join(scene(i, p) for i, p in enumerate(projects))}

			<section class="outro fx shadow" id="contacto">
				<h2>{L('Toda la red, encendida', 'The whole network, lit up')}</h2>
				<p>{L('¿Hablamos de IA generativa, RAG o agentes? Madrid, España.', 'Shall we talk about generative AI, RAG or agents? Madrid, Spain.')}</p>
				<ul class="links">
					<li><a href="{linkedin}" target="_blank" rel="noopener">LinkedIn</a></li>
					<li><a href="{github}" target="_blank" rel="noopener">GitHub</a></li>
					<li><a href="generic.html">{L('Sobre mí', 'About me')}</a></li>
					<li><a href="proyectos.html">{L('Todos los proyectos', 'All projects')}</a></li>
				</ul>
				<div class="mail"><span id="mailTxt">juanm.cornejoc@gmail.com</span><button type="button" id="copyMail">{L('Copiar email', 'Copy email')}</button></div>
			</section>

			<nav class="progress" id="progress" aria-label="{esc('Recorrido')}"><span class="fill" id="fill"></span>{dots}</nav>
		</main>

		<div class="sheet" id="sheet" hidden role="dialog" aria-modal="true" aria-label="{esc('Detalle del proyecto')}">
			<div class="sheet-bar">
				<a id="sheet-page" href="#">{L('Abrir como página', 'Open as a page')}</a>
				<button type="button" class="sheet-close">{L('Volver a la red', 'Back to the network')}</button>
			</div>
			<div class="sheet-body" id="sheet-body"></div>
		</div>
		<div id="track"></div>
		<noscript><style>#hud{{position:relative}}</style><p style="padding:20px"><a href="proyectos.html">Ver los proyectos en lista</a></p></noscript>

		<script>
			// Modo lista: sin WebGL, o si en 8 s la escena no ha arrancado. Los vídeos pasan a cargarse con controles.
			window.__static = function () {{
				document.documentElement.classList.add('static');
				document.querySelectorAll('video[data-src]').forEach(function (v) {{ if (!v.src) v.src = v.dataset.src; v.controls = true; v.preload = 'metadata'; }});
			}};
			setTimeout(function () {{ if (!window.__booted) window.__static(); }}, 8000);
			document.getElementById('copyMail').addEventListener('click', function () {{
				var t = document.getElementById('mailTxt'), b = this;
				function sel() {{ var r = document.createRange(); r.selectNodeContents(t); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }}
				try {{ navigator.clipboard.writeText(t.textContent).then(function () {{ b.classList.add('done'); }}, sel); }} catch (e) {{ sel(); }}
			}});
		</script>
{LIBS}
	</body>
</html>
"""
    # Cabecera: la de build.py (metadatos para compartir) pero sin los estilos de Massively
    top = head("Juan Manuel Cornejo · Portfolio", "Juan Manuel Cornejo · Portfolio", desc)
    top = re.sub(r'\s*<link rel="stylesheet" href="assets/css/main.css" />', "", top)
    top = re.sub(r'\s*<link rel="stylesheet" href="assets/css/portfolio.css" />', "", top)
    top = re.sub(r'\s*<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>', "", top)
    top = top.replace("Massively by HTML5 UP\n\thtml5up.net | @ajlkn\n\tFree for personal and commercial use under the CCA 3.0 license (html5up.net/license)\n\t", "")
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com" />\n'
             '\t\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
             '\t\t<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1'
             '&amp;family=Hanken+Grotesk:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400&amp;display=swap" />\n'
             '\t\t<link rel="stylesheet" href="assets/css/red.css" />\n'
             '\t\t<meta name="theme-color" content="#000000" />\n'
             '\t\t<script src="assets/js/portfolio.js" defer></script>')
    top = top.replace('<script src="assets/js/portfolio.js" defer></script>', fonts, 1)
    top = re.sub(r'<body class="is-preload">\s*<div id="wrapper"[^>]*>\s*', '<body class="red">', top)
    with open(os.path.join(root, "index.html"), "w", encoding="utf-8") as f:
        f.write(top + body)
