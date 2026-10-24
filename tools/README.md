# Cómo actualizar el portfolio

Las páginas `index.html`, `proyectos.html`, `generic.html` y las de cada proyecto (`careercraft.html`, `writers.html`, `kocinai.html`, `economia-familiar.html`) **se generan**; no las edites a mano.

1. Edita textos o vídeos en `tools/content.py`.
2. Regenera: `python3 tools/build.py`
3. Commit y push.

## Añadir el vídeo de un proyecto

1. Graba la demo (30–90 s, 1280 px de ancho es suficiente) y comprímela:
   `ffmpeg -i demo.mov -vf "scale=1280:-2,fps=30,format=yuv420p" -c:v libx264 -crf 27 -preset slow -movflags +faststart -an assets/video/<slug>-demo.mp4`
   Mantén cada vídeo por debajo de ~10 MB (GitHub rechaza archivos de más de 100 MB).
2. Saca un póster: `ffmpeg -ss 5 -i assets/video/<slug>-demo.mp4 -frames:v 1 -q:v 3 images/projects/<slug>-poster.jpg`
3. En `content.py`, rellena `"video": {"src": "assets/video/<slug>-demo.mp4", "poster": "images/projects/<slug>-poster.jpg"}` (y, si quieres, cambia `"cover"` por el póster).
4. `python3 tools/build.py`

Alternativa para vídeos largos: subirlo a YouTube como «no listado» y sustituir el bloque `<video>` por un `<iframe>`.

## Diagramas

Cada proyecto embebe dos diagramas interactivos en modo oscuro: «Cómo funciona» (`diagramas/<slug>-flujo-es.html` / `-en.html`) y «Arquitectura» (`diagramas/<slug>-es.html` / `-en.html`), generados con [Archify](https://github.com/tt-a1i/archify). Son HTML autónomos (sin peticiones de red): para actualizar uno, regenéralo con Archify y sustituye el archivo. Son versiones públicas: sin enlaces al código privado ni detalles internos de seguridad.

## Idiomas

Todo texto va en pareja ES/EN (`data-l="es"` / `data-l="en"`). El selector del menú cambia el idioma y lo recuerda; `?lang=en` fuerza inglés en un enlace.

## Portada inmersiva

`index.html` es la red neuronal que se recorre con el scroll; la genera `tools/red.py` con los mismos datos de `content.py` (vídeo, tagline, cifras y stack de cada proyecto). La animación está en `assets/js/red.js` (Three.js + GSAP ScrollTrigger + Lenis, por CDN) y los estilos en `assets/css/red.css`.

- «Cómo funciona por dentro» abre, encima de la red, el contenido de la página del proyecto (`<slug>.html`), así que no hay nada duplicado.
- `index.html#<slug>` lleva directamente a la neurona de ese proyecto.
- Sin WebGL, o con «reducir movimiento», la portada se adapta (lista legible o vistas fijas). `proyectos.html` es la lista clásica.
- El color de cada neurona está en `COLORS` de `tools/red.py`.
