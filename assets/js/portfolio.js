/* Portfolio 2026: selector de idioma ES/EN. */
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
})();
