/* Portfolio 2026: fondo animado de la portada.
   Una red de nodos con forma de cerebro en la que cinco agentes se pasan mensajes
   (pulsos que viajan por las conexiones). Canvas 2D, sin dependencias.
   - Respeta prefers-reduced-motion (dibuja un fotograma fijo).
   - Se pausa cuando la portada no está en pantalla o la pestaña está oculta. */
(function () {
	var canvas = document.querySelector("#intro .neuro-bg");
	if (!canvas || !canvas.getContext) return;
	var ctx = canvas.getContext("2d");

	var BG = "#16191f", LINE = "rgba(110,118,134,0.28)", GRID = "rgba(255,255,255,0.035)";
	var PAL = ["#e88296", "#b29ce6", "#6ec4b4", "#e4b068", "#78aae6"];
	var LABELS = {
		es: ["PLANIFICA", "INVESTIGA", "RECUERDA", "REVISA", "RESPONDE"],
		en: ["PLANS", "RESEARCHES", "REMEMBERS", "REVIEWS", "ANSWERS"]
	};
	var AG = [[-0.55, -0.45], [0.15, -0.70], [0.62, -0.18], [-0.30, 0.25], [0.40, 0.40]];
	var ROUTES = [[0, 1], [1, 2], [2, 4], [3, 0], [4, 3], [1, 3], [2, 0]];
	var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

	// generador pseudoaleatorio con semilla: la red es siempre la misma
	var seed = 7;
	function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }

	// forma de cerebro (vista lateral) en coordenadas normalizadas u,v
	function inside(u, v) {
		var cereb = u * u + Math.pow((v + 0.08) / 0.82, 2) < 1 && !(u > 0.25 && v > 0.45);
		var cerebelo = Math.pow((u - 0.48) / 0.34, 2) + Math.pow((v - 0.62) / 0.24, 2) < 1;
		return cereb || cerebelo;
	}
	var nodes = [], tries = 0;
	while (nodes.length < 200 && tries < 60000) {
		tries++;
		var u = rnd() * 2.1 - 1.05, v = rnd() * 2.1 - 1.05;
		if (!inside(u, v)) continue;
		var ok = true;
		for (var i = 0; i < nodes.length; i++) {
			var du = (nodes[i].u - u) * 300, dv = (nodes[i].v - v) * 200;
			if (du * du + dv * dv < 22 * 22) { ok = false; break; }
		}
		if (ok) nodes.push({ u: u, v: v, c: PAL[Math.floor(((Math.atan2(v, u) + Math.PI) / (2 * Math.PI)) * 5) % 5] });
	}
	// conexiones: 3 vecinos más cercanos
	var edges = [], adj = nodes.map(function () { return []; }), seen = {};
	nodes.forEach(function (a, i) {
		var d = nodes.map(function (b, j) {
			var x = (a.u - b.u) * 300, y = (a.v - b.v) * 200;
			return [Math.sqrt(x * x + y * y), j];
		}).sort(function (p, q) { return p[0] - q[0]; });
		for (var k = 1; k <= 3; k++) {
			var j = d[k][1], key = Math.min(i, j) + "-" + Math.max(i, j);
			if (d[k][0] < 85 && !seen[key]) { seen[key] = 1; edges.push([i, j]); adj[i].push(j); adj[j].push(i); }
		}
	});
	function nearest(u, v) {
		var best = 0, bd = 1e9;
		nodes.forEach(function (n, i) { var d = Math.pow(n.u - u, 2) + Math.pow(n.v - v, 2); if (d < bd) { bd = d; best = i; } });
		return best;
	}
	var agents = AG.map(function (p, k) { return { i: nearest(p[0], p[1]), c: PAL[k] }; });
	function bfs(a, b) {
		var prev = {}; prev[a] = -1; var q = [a];
		for (var h = 0; h < q.length; h++) {
			var n = q[h]; if (n === b) break;
			adj[n].forEach(function (m) { if (!(m in prev)) { prev[m] = n; q.push(m); } });
		}
		var out = [b]; while (prev[out[out.length - 1]] !== -1 && prev[out[out.length - 1]] !== undefined) out.push(prev[out[out.length - 1]]);
		return out.reverse();
	}
	var paths = ROUTES.map(function (r) { return bfs(agents[r[0]].i, agents[r[1]].i); });

	var W, H, dpr, cx, cy, sx, sy;
	function resize() {
		dpr = Math.min(window.devicePixelRatio || 1, 2);
		W = canvas.clientWidth; H = canvas.clientHeight;
		canvas.width = W * dpr; canvas.height = H * dpr;
		ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
		var s = Math.min(W / 760, H / 700, 1.1);        // cabe en la parte alta, sin tapar el nombre
		sx = 300 * s; sy = 200 * s; cx = W / 2; cy = H * 0.33;
	}
	function P(i) { return [cx + nodes[i].u * sx, cy + nodes[i].v * sy]; }
	function along(path, t) {
		var pts = path.map(P), L = 0, segs = [];
		for (var i = 0; i < pts.length - 1; i++) { var d = Math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]); segs.push(d); L += d; }
		var x = L * t;
		for (i = 0; i < segs.length; i++) {
			if (x <= segs[i]) { var f = segs[i] ? x / segs[i] : 0; return [pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f]; }
			x -= segs[i];
		}
		return pts[pts.length - 1];
	}

	function draw(time) {
		var ph = (time / 8000) % 1;
		ctx.fillStyle = BG; ctx.fillRect(0, 0, W, H);
		ctx.fillStyle = GRID;
		for (var gx = 0; gx < W; gx += 24) for (var gy = 0; gy < H; gy += 24) ctx.fillRect(gx, gy, 1, 1);
		ctx.strokeStyle = LINE; ctx.lineWidth = 1; ctx.beginPath();
		edges.forEach(function (e) { var a = P(e[0]), b = P(e[1]); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); });
		ctx.stroke();
		// rutas entre agentes (discontinuas, como las relaciones de Writers)
		ctx.setLineDash([4, 5]);
		paths.forEach(function (p, k) {
			ctx.strokeStyle = agents[ROUTES[k][0]].c; ctx.globalAlpha = 0.35; ctx.beginPath();
			p.forEach(function (i, n) { var q = P(i); n ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); });
			ctx.stroke();
		});
		ctx.setLineDash([]); ctx.globalAlpha = 1;
		nodes.forEach(function (n, i) { var q = P(i); ctx.globalAlpha = 0.5; ctx.fillStyle = n.c; ctx.beginPath(); ctx.arc(q[0], q[1], 2, 0, 7); ctx.fill(); });
		ctx.globalAlpha = 1;
		// pulsos (mensajes entre agentes)
		paths.forEach(function (p, k) {
			var t = reduce ? (0.35 + k * 0.13) % 1 : (ph * (1 + k % 2) + k * 0.17) % 1, q = along(p, t), c = agents[ROUTES[k][0]].c;
			var g = ctx.createRadialGradient(q[0], q[1], 0, q[0], q[1], 16);
			g.addColorStop(0, c); g.addColorStop(1, "rgba(22,25,31,0)");
			ctx.fillStyle = g; ctx.globalAlpha = 0.9; ctx.beginPath(); ctx.arc(q[0], q[1], 16, 0, 7); ctx.fill();
			ctx.globalAlpha = 1; ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(q[0], q[1], 2.2, 0, 7); ctx.fill();
		});
		// agentes con su ficha
		var lang = document.documentElement.getAttribute("data-lang") === "en" ? "en" : "es";
		ctx.font = "600 11px Inter, 'Source Sans Pro', Helvetica, sans-serif"; ctx.textBaseline = "middle";
		agents.forEach(function (a, k) {
			var q = P(a.i), pulse = reduce ? 0.6 : 0.5 + 0.5 * Math.sin(2 * Math.PI * (ph * 2 + k / 5)), r = 9 + 3 * pulse;
			ctx.strokeStyle = a.c; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(q[0], q[1], r, 0, 7); ctx.stroke();
			ctx.fillStyle = a.c; ctx.beginPath(); ctx.arc(q[0], q[1], 4.5, 0, 7); ctx.fill();
			if (W < 520) return;                              // en móvil, sin etiquetas
			var lab = LABELS[lang][k], tw = ctx.measureText(lab).width, bx = q[0] + 16, by = q[1] - 11;
			ctx.fillStyle = "#1e222a"; ctx.strokeStyle = "#3a404c";
			ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(bx, by, tw + 26, 22, 5); else ctx.rect(bx, by, tw + 26, 22); ctx.fill(); ctx.stroke();
			ctx.fillStyle = a.c; ctx.beginPath(); ctx.arc(bx + 11, by + 11, 3, 0, 7); ctx.fill();
			ctx.fillStyle = "#c4c8d0"; ctx.fillText(lab, bx + 19, by + 11.5);
		});
	}

	var running = false, visible = true;
	function loop(t) { if (!running) return; draw(t); requestAnimationFrame(loop); }
	function start() { if (reduce) { draw(0); return; } if (!running && visible && !document.hidden) { running = true; requestAnimationFrame(loop); } }
	function stop() { running = false; }

	resize(); draw(0);
	window.addEventListener("resize", function () { resize(); draw(performance.now()); });
	document.addEventListener("visibilitychange", function () { document.hidden ? stop() : start(); });
	if ("IntersectionObserver" in window) {
		new IntersectionObserver(function (en) { visible = en[0].isIntersecting; visible ? start() : stop(); }).observe(canvas);
	}
	start();
})();
