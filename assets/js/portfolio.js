/* Portfolio 2026: selector de idioma ES/EN y renderizado de diagramas Mermaid. */
(function () {
	var KEY = "portfolio-lang";
	var root = document.documentElement;

	function initialLang() {
		var q = new URLSearchParams(window.location.search).get("lang");
		if (q === "es" || q === "en") return q;
		try {
			var saved = localStorage.getItem(KEY);
			if (saved === "es" || saved === "en") return saved;
		} catch (e) { /* almacenamiento no disponible */ }
		return (navigator.language || "es").toLowerCase().indexOf("es") === 0 ? "es" : "en";
	}

	function setLang(lang) {
		root.setAttribute("data-lang", lang);
		root.setAttribute("lang", lang);
		try { localStorage.setItem(KEY, lang); } catch (e) { /* ignorar */ }
		var btns = document.querySelectorAll(".lang-btn");
		for (var i = 0; i < btns.length; i++) {
			btns[i].textContent = lang === "es" ? "EN" : "ES";
			btns[i].setAttribute("aria-label", lang === "es" ? "Switch to English" : "Cambiar a español");
		}
		var t = document.querySelector("title[data-es]");
		if (t) document.title = t.getAttribute("data-" + lang);
	}

	setLang(initialLang());

	// Listener directo en cada botón: el panel móvil de Massively corta la propagación de los clics.
	function bindToggle() {
		var btns = document.querySelectorAll(".lang-btn");
		for (var i = 0; i < btns.length; i++) {
			btns[i].addEventListener("click", function (ev) {
				ev.preventDefault();
				setLang(root.getAttribute("data-lang") === "es" ? "en" : "es");
			});
		}
		setLang(root.getAttribute("data-lang"));
	}
	if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bindToggle);
	else bindToggle();

	// ---------- Mermaid ----------
	// Cada diagrama vive en <script type="text/x-mermaid" data-target="id">; se renderiza en el div #id.
	function renderDiagrams() {
		var sources = document.querySelectorAll('script[type="text/x-mermaid"]');
		if (!sources.length || !window.mermaid) return;
		window.mermaid.initialize({
			startOnLoad: false,
			securityLevel: "strict",
			theme: "base",
			flowchart: { htmlLabels: true, curve: "basis", useMaxWidth: true },
			themeVariables: {
				fontFamily: "Source Sans Pro, Helvetica, Arial, sans-serif",
				fontSize: "15px",
				primaryColor: "#ffffff",
				primaryBorderColor: "#18bfef",
				primaryTextColor: "#212931",
				lineColor: "#7f8a96",
				secondaryColor: "#eaf8fd",
				tertiaryColor: "#f4f5f6",
				clusterBkg: "#f4f7f9",
				clusterBorder: "#c8cccf",
				edgeLabelBackground: "#ffffff"
			}
		});
		// mermaid.render() mide en un contenedor temporal propio, así que el diagrama del idioma oculto
		// se dibuja bien aunque su destino esté en display:none.
		var jobs = [];
		for (var i = 0; i < sources.length; i++) {
			(function (src, n) {
				var target = document.getElementById(src.getAttribute("data-target"));
				if (!target) return;
				jobs.push(
					window.mermaid.render("mmd-" + n, src.textContent.trim()).then(function (out) {
						target.innerHTML = out.svg;
					}).catch(function () {
						target.innerHTML = '<p class="diagram-loading">—</p>';
					})
				);
			})(sources[i], i);
		}
		return Promise.all(jobs);
	}

	if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", renderDiagrams);
	else renderDiagrams();
})();
