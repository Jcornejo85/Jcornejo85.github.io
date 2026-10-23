# -*- coding: utf-8 -*-
"""Contenido bilingüe (ES/EN) de los proyectos del portfolio.

Editar aquí y regenerar con:  python3 tools/build.py
"""

PROJECTS = [
    # ------------------------------------------------------------------ CareerCraft
    {
        "slug": "careercraft",
        "name": "CareerCraft",
        "cover": "images/projects/careercraft-poster.jpg",
        "video": {"src": "assets/video/careercraft-demo.mp4", "poster": "images/projects/careercraft-poster.jpg"},
        "link": None,
        "tagline": (
            "Asistente de carrera con IA: construye un perfil profesional verificado y genera CVs adaptados a cada oferta <strong>sin inventar nada</strong>.",
            "AI career assistant: it builds a verified professional profile and generates CVs tailored to each job offer <strong>without making anything up</strong>.",
        ),
        "card": (
            "Asistente de carrera con IA que construye tu perfil, analiza cada oferta y genera un CV adaptado que pasa una auditoría de veracidad antes de exportarse. Incluye simulador de entrevistas con feedback STAR.",
            "AI career assistant that builds your profile, analyses each job offer and generates a tailored CV that must pass a truthfulness audit before export. Includes an interview simulator with STAR feedback.",
        ),
        "chips": ["Python", "FastAPI", "React + TypeScript", "Claude (Sonnet / Haiku)", "PostgreSQL + pgvector", "SQLite", "WeasyPrint", "Tauri 2", "Docker"],
        "facts": [
            ("~$0.10", "coste real por CV generado", "real cost per generated CV"),
            ("20/20", "exageraciones detectadas en el banco de evaluación", "exaggerations caught in the eval set"),
            ("~850", "tests automáticos", "automated tests"),
            ("10", "plantillas PDF legibles por ATS", "ATS-readable PDF templates"),
        ],
        "what": (
            [
                "Escribir un CV distinto para cada oferta es lento, y los generadores con IA tienden a <em>adornar</em> la experiencia. CareerCraft parte de la idea contraria: primero construye una <strong>base de hechos verificada</strong> sobre ti y después redacta a partir de ella con el enfoque más favorable, siempre que siga siendo defendible.",
                "Puedes empezar subiendo tu CV o tu PDF de LinkedIn, o con una entrevista conversacional que solo pregunta por lo que falta. Al pegar una oferta, la app cruza cada requisito con tu perfil (cubierto, implícito con evidencia o ausente), genera el CV en el idioma de la oferta y lo somete a una auditoría antes de dejarte exportarlo.",
                "Funciona de dos maneras con el mismo código: como <strong>aplicación web</strong> con cuentas de usuario, o como <strong>app de escritorio para macOS</strong> en la que tus datos no salen del ordenador.",
            ],
            [
                "Writing a different CV for every job offer is slow, and AI generators tend to <em>embellish</em> experience. CareerCraft takes the opposite approach: it first builds a <strong>verified fact base</strong> about you and then writes from it with the most favourable framing that is still defensible.",
                "You can start by uploading your CV or LinkedIn PDF, or through a conversational interview that only asks about what is missing. When you paste a job offer, the app matches each requirement against your profile (covered, implied with evidence, or missing), generates the CV in the offer's language and audits it before letting you export it.",
                "The same code runs in two ways: as a <strong>web application</strong> with user accounts, or as a <strong>macOS desktop app</strong> where your data never leaves your computer.",
            ],
        ),
        "arch_intro": (
            [
                "Un único backend FastAPI concentra toda la lógica: perfil, generación del CV, entrevistas y créditos. La interfaz es una SPA en React que habla con él por REST. Los servicios de dominio son los únicos que tocan la base de datos, el render de PDF y la capa de IA, que elige el proveedor según el modelo: Claude para redactar y auditar, y OpenAI solo para embeddings.",
                "El mismo backend se empaqueta de dos formas. En la versión web corre en un contenedor Docker con PostgreSQL + pgvector y login con JWT. En la app de escritorio, una shell Tauri 2 lanza el backend como proceso local con SQLite y guarda la credencial de IA en el llavero de macOS.",
            ],
            [
                "A single FastAPI backend holds all the logic: profile, CV generation, interviews and credits. The UI is a React SPA that talks to it over REST. Only the domain services touch the database, the PDF renderer and the AI layer, which picks the provider by model: Claude to write and audit, and OpenAI for embeddings only.",
                "The same backend ships in two forms. The web version runs in a Docker container with PostgreSQL + pgvector and JWT login. In the desktop app, a Tauri 2 shell launches the backend as a local process with SQLite and keeps the AI credential in the macOS keychain.",
            ],
        ),
        "decisions": [
            ("Un backend, dos productos",
             "En lugar de mantener una app web y otra de escritorio, el mismo backend se empaqueta como contenedor o como proceso local de Tauri. Cambian la base de datos (PostgreSQL o SQLite) y la autenticación; la lógica de dominio y sus tests son los mismos.",
             "One backend, two products",
             "Instead of maintaining separate web and desktop apps, the same backend ships either as a container or as a local Tauri process. Only the database (PostgreSQL or SQLite) and authentication change; the domain logic and its tests are shared."),
            ("Antialucinación por capas",
             "Los datos factuales (empresa, puesto, fechas, skills) se copian tal cual; el modelo solo redacta resumen y bullets. Después, un gate audita cada dimensión: los años y el nivel se comprueban con código determinista (los LLM fallaban la aritmética) y la invención o el seniority inflado los revisan jueces LLM con responsabilidades separadas.",
             "Layered anti-hallucination",
             "Factual data (company, role, dates, skills) is copied verbatim; the model only writes the summary and bullets. A gate then audits each dimension: years and level are checked with deterministic code (LLMs got the arithmetic wrong) while invention or inflated seniority are reviewed by LLM judges with separate responsibilities."),
            ("Ni inflar ni quedarse corto",
             "El corrector funciona en las dos direcciones: si un arreglo elimina una exageración pero deja el logro por debajo de lo real, no se acepta. El objetivo es el «punto medio honesto».",
             "Neither inflate nor undersell",
             "The corrector works both ways: if a fix removes an exaggeration but undersells the real achievement, it is rejected. The goal is the “honest middle”."),
            ("Requisitos con evidencia obligatoria",
             "Un requisito solo cuenta como «implícito» si cita un hecho del perfil; si no, pasa a «ausente». La cobertura y el score ATS son deterministas, no una opinión del modelo.",
             "Requirements need evidence",
             "A requirement only counts as “implied” if it cites a fact from the profile; otherwise it becomes “missing”. Coverage and the ATS score are deterministic, not the model's opinion."),
            ("Coste bajo control",
             "Cada tarea usa el modelo que necesita (Haiku para extraer, Sonnet para redactar), con prompt caching y un ledger de créditos atómico. Coste real: unos 10 céntimos de dólar por CV (≈4 céntimos en el banco de evaluación).",
             "Cost under control",
             "Each task uses the model it needs (Haiku to extract, Sonnet to write), with prompt caching and an atomic credit ledger. Real cost: about 10 US cents per CV (≈4 cents on the evaluation set)."),
            ("Medir antes que intuir",
             "Desarrollo guiado por specs y ADRs, con un banco de evaluación fijo y una rúbrica de calidad 0–100 que actúa como prueba de regresión antes de cada cambio de prompt o modelo.",
             "Measure, don't guess",
             "Spec-driven development with ADRs, a fixed evaluation set and a 0–100 quality rubric that acts as a regression test before every prompt or model change."),
        ],
    },
    # ------------------------------------------------------------------ Writers
    {
        "slug": "writers",
        "name": "Writers",
        "cover": "images/projects/writers-poster.jpg",
        "video": {"src": "assets/video/writers-demo.mp4", "poster": "images/projects/writers-poster.jpg"},
        "link": None,
        "tagline": (
            "App de escritorio para escribir novelas de ciencia ficción y fantasía: escuela de oficio, taller de mundos y manuscrito, con una IA que <strong>revisa, no escribe por ti</strong>.",
            "Desktop app for writing science-fiction and fantasy novels: a craft school, a world-building workshop and a manuscript editor, with an AI that <strong>reviews instead of writing for you</strong>.",
        ),
        "card": (
            "App de escritorio local-first para escribir novelas: lecciones de oficio cuyos ejercicios crean fichas reales, lienzo infinito para construir el mundo, cronología, relaciones, hilos de trama y manuscrito, con un asistente Claude que hace de editor.",
            "Local-first desktop app for novelists: craft lessons whose exercises create real story entities, an infinite canvas for world-building, timeline, relationships, plot threads and manuscript, with a Claude assistant acting as an editor.",
        ),
        "chips": ["TypeScript", "React 19", "Tauri 2 (Rust)", "SQLite + FTS5 (WASM)", "Claude API", "Ollama", "OpenAI Images", "Playwright"],
        "facts": [
            ("~40", "lecciones de oficio en español", "craft lessons in Spanish"),
            ("3–15 MB", "instalador (Tauri en vez de Electron)", "installer (Tauri instead of Electron)"),
            ("0", "claves de API expuestas al frontend", "API keys exposed to the frontend"),
            ("Win · Mac", "escritorio multiplataforma", "cross-platform desktop"),
        ],
        "what": (
            [
                "Las herramientas para escritores separan tres cosas que en la práctica van juntas: <strong>aprender el oficio</strong>, <strong>construir el mundo</strong> y <strong>escribir el libro</strong>. Writers las une en una sola app de escritorio.",
                "La <em>Escuela</em> tiene lecciones de oficio cuyos ejercicios crean o enriquecen fichas reales del libro. Esas fichas (personajes, lugares, facciones, sistemas de magia…) viven en un lienzo infinito y alimentan vistas derivadas: cronología con calendarios inventados, grafo de relaciones, hilos de trama y estructuras. El <em>Manuscrito</em> se escribe por escenas, con menciones a las fichas y un corrector que aprende los nombres de tu mundo.",
                "La IA está planteada como un editor: revisa continuidad, detecta huecos y hace preguntas, pero no escribe la prosa. El contexto que se le envía es visible y editable antes de cada petición, y se muestra el coste real de cada respuesta.",
            ],
            [
                "Writing tools tend to separate three things that in practice go together: <strong>learning the craft</strong>, <strong>building the world</strong> and <strong>writing the book</strong>. Writers brings them together in a single desktop app.",
                "The <em>School</em> has craft lessons whose exercises create or enrich real entities of the book. Those entities (characters, places, factions, magic systems…) live on an infinite canvas and feed derived views: a timeline with invented calendars, a relationship graph, plot threads and story structures. The <em>Manuscript</em> is written scene by scene, with mentions of entities and a spell checker that learns your world's names.",
                "AI is designed as an editor: it checks continuity, spots gaps and asks questions, but it doesn't write the prose. The context sent to it is visible and editable before each request, and the real cost of every answer is shown.",
            ],
        ),
        "arch_intro": (
            [
                "La app es local-first. La interfaz en React y el núcleo en TypeScript puro corren dentro del webview de Tauri, y el núcleo no sabe en qué plataforma está: pide disco o IA a una capa de plataforma, que en escritorio delega en el proceso nativo en Rust.",
                "Ese proceso nativo es la única salida al exterior: lee y escribe la carpeta del proyecto y los ajustes de la app, consulta el llavero del sistema y hace las peticiones a los proveedores de IA (Claude, OpenAI u Ollama en local). El índice SQLite con búsqueda de texto completo vive en memoria y se reconstruye a partir de los archivos.",
            ],
            [
                "The app is local-first. The React UI and the pure-TypeScript core run inside Tauri's webview, and the core doesn't know which platform it runs on: it asks a platform layer for disk or AI access, which on desktop delegates to the native Rust process.",
                "That native process is the only way out: it reads and writes the project folder and the app settings, uses the OS keychain and makes the requests to AI providers (Claude, OpenAI or local Ollama). The SQLite full-text index lives in memory and is rebuilt from the files.",
            ],
        ),
        "decisions": [
            ("Archivos como fuente de verdad",
             "Todo se guarda en Markdown con YAML y JSON Canvas legibles y versionables con git. La base SQLite + FTS5 (en WebAssembly) es solo un índice derivado que se puede reconstruir en cualquier momento.",
             "Files as the source of truth",
             "Everything is stored as readable, git-friendly Markdown with YAML and JSON Canvas. The SQLite + FTS5 database (in WebAssembly) is only a derived index that can be rebuilt at any time."),
            ("Tauri en lugar de Electron",
             "Instalador de 3–15 MB y menos memoria. La lógica vive en TypeScript y Rust queda solo para lo nativo. Un test impide que el núcleo importe React o Tauri.",
             "Tauri instead of Electron",
             "A 3–15 MB installer and lower memory use. Logic lives in TypeScript; Rust is kept for native concerns only. A test prevents the core from importing React or Tauri."),
            ("IA segura por diseño",
             "Las claves de API se guardan en el llavero del sistema, no en la interfaz, y la red solo se usa desde el proceso nativo para hablar con los proveedores de IA.",
             "Secure-by-design AI",
             "API keys are kept in the OS keychain, not in the UI, and the network is only used from the native process to talk to AI providers."),
            ("IA transparente",
             "El contexto que se envía se ve como chips editables, la «biblia» del libro se cachea con prompt caching y cada respuesta muestra su coste real. Hay alternativa local con Ollama.",
             "Transparent AI",
             "The context being sent is shown as editable chips, the book's “bible” is cached with prompt caching and every answer shows its real cost. A local alternative with Ollama is available."),
            ("Privacidad y trabajo offline",
             "Corrector ortográfico local, fuentes servidas sin CDN y eliminación de metadatos (EXIF/GPS) en las imágenes que se suben.",
             "Privacy and offline work",
             "Local spell checker, fonts served without a CDN and metadata (EXIF/GPS) stripped from uploaded images."),
        ],
    },
    # ------------------------------------------------------------------ KocinAI
    {
        "slug": "kocinai",
        "name": "KocinAI",
        "cover": "images/projects/kocinai-poster.jpg",
        "video": {"src": "assets/video/kocinai-demo.mp4", "poster": "images/projects/kocinai-poster.jpg"},
        "link": "https://kocin-ai.app",
        "tagline": (
            "PWA para organizar la cocina de una familia: recetario, planificador semanal, despensa y lista de la compra, con IA que <strong>planifica, importa recetas y lee tickets</strong>.",
            "PWA that organises a family's kitchen: recipe book, weekly planner, pantry and shopping list, with AI that <strong>plans, imports recipes and reads receipts</strong>.",
        ),
        "card": (
            "PWA en producción que junta recetario, menú semanal, despensa y lista de la compra. La IA crea o importa recetas, lee tickets del súper con visión y planifica la semana teniendo en cuenta las alergias de la familia.",
            "Production PWA bringing together recipe book, weekly menu, pantry and shopping list. AI creates or imports recipes, reads supermarket receipts with vision and plans the week around the family's allergies.",
        ),
        "chips": ["TypeScript", "Next.js 16", "React 19", "tRPC", "Supabase (Postgres · Auth · Realtime)", "Drizzle", "Claude Sonnet / Haiku", "Vision", "Vercel"],
        "facts": [
            ("~2¢", "por planificación semanal con IA", "per AI weekly plan"),
            ("4", "funciones de IA (recetas, importar, tickets, menú)", "AI features (recipes, import, receipts, menu)"),
            ("~280", "tests automáticos", "automated tests"),
            ("PWA", "instalable en el móvil", "installable on mobile"),
        ],
        "what": (
            [
                "Decidir qué se come cada día, saber qué hay en casa y no olvidar nada en el súper son tres problemas que suelen vivir en apps distintas. KocinAI los junta en una PWA pensada para el móvil y compartida entre los miembros del hogar.",
                "La lista de la compra se calcula sola: <strong>menú de la semana menos lo que ya hay en la despensa</strong>, agrupada por pasillos y sincronizada en tiempo real entre la familia. La IA se encarga de lo pesado: crea recetas a partir de una frase, las importa desde una web, lee el ticket del supermercado (foto o PDF) para rellenar la despensa y propone el menú de la semana a partir de una petición libre, siempre respetando las alergias del hogar.",
            ],
            [
                "Deciding what to eat each day, knowing what's at home and not forgetting anything at the supermarket are three problems that usually live in separate apps. KocinAI brings them together in a mobile-first PWA shared by everyone in the household.",
                "The shopping list computes itself: <strong>this week's menu minus what is already in the pantry</strong>, grouped by aisle and synced in real time across the family. AI handles the heavy lifting: it creates recipes from a sentence, imports them from a website, reads the supermarket receipt (photo or PDF) to fill the pantry and proposes the week's menu from a free-text request, always respecting the household's allergies.",
            ],
        ),
        "arch_intro": (
            [
                "Es un monolito Next.js 16 desplegado en Vercel. Las páginas del App Router hablan con el servidor por un único endpoint tRPC, donde los routers de cada dominio (recetas, menú, despensa, compra…) trabajan siempre en el contexto del hogar del usuario y acceden a Postgres con Drizzle.",
                "Supabase pone el resto de piezas: autenticación, base de datos, almacenamiento de fotos y Realtime, que empuja los cambios de la lista de la compra a todos los móviles del hogar. Las funciones de IA pasan por una capa común que aplica los cupos de uso, prepara los prompts y llama a Claude; para importar una receta, además, lee la web de origen.",
            ],
            [
                "It is a Next.js 16 monolith deployed on Vercel. App Router pages talk to the server through a single tRPC endpoint, where each domain's routers (recipes, menu, pantry, shopping…) always work in the context of the user's household and reach Postgres through Drizzle.",
                "Supabase provides the rest: authentication, database, photo storage and Realtime, which pushes shopping-list changes to every phone in the household. AI features go through a shared layer that applies usage quotas, builds the prompts and calls Claude; to import a recipe it also reads the source website.",
            ],
        ),
        "decisions": [
            ("IA contenida por estructura",
             "Todas las llamadas usan tool-use forzado y validación con Zod, el resultado se reconcilia contra el catálogo de ingredientes y nada se guarda sin revisión humana. Encima hay un filtro de intención (cada función solo acepta lo suyo) y el contenido externo se delimita como datos, no como instrucciones.",
             "AI contained by structure",
             "Every call uses forced tool-use and Zod validation, the output is reconciled against the ingredient catalogue and nothing is saved without human review. On top of that there is an intent filter (each feature only accepts its own task) and external content is fenced as data, not instructions."),
            ("Primero filtrar, después generar",
             "El planificador se rediseñó tras un 502 en producción: Haiku interpreta la petición, un filtro determinista reduce las recetas candidatas y solo entonces Sonnet compone. El prompt ya no crece con el recetario.",
             "Filter first, then generate",
             "The planner was redesigned after a 502 in production: Haiku interprets the request, a deterministic filter narrows the candidate recipes and only then does Sonnet compose. The prompt no longer grows with the recipe book."),
            ("Cada modelo para lo suyo",
             "Haiku para extracciones y clasificación por lotes (78 recetas por unos 2,5 céntimos), Sonnet para calidad y visión. El modelo de cada tarea se cambia por variable de entorno.",
             "The right model for each job",
             "Haiku for extraction and batch classification (78 recipes for about 2.5 cents), Sonnet for quality and vision. Each task's model is configurable through an environment variable."),
            ("Coste bajo control",
             "Ledger de tokens y coste por llamada, cupo diario por hogar, rate limiting atómico en Postgres y planes free / premium / prueba con caducidad sin necesidad de cron.",
             "Cost under control",
             "Per-call token and cost ledger, a daily quota per household, atomic rate limiting in Postgres and free / premium / trial plans with expiry and no cron jobs."),
            ("Un hogar, un espacio de datos",
             "Cada endpoint resuelve primero el hogar del usuario y solo trabaja con sus datos. La lista de la compra se comparte por Supabase Realtime en un componente aislado, y las recetas que alguien decide publicar se sirven desde un catálogo público separado.",
             "One household, one data space",
             "Every endpoint first resolves the user's household and only works with its data. The shopping list is shared via Supabase Realtime in an isolated component, and recipes someone chooses to publish are served from a separate public catalogue."),
        ],
    },
    # ------------------------------------------------------------------ Economía Familiar
    {
        "slug": "economia-familiar",
        "name": "Economía Familiar",
        "cover": "images/projects/economia-familiar-poster.jpg",
        "video": {
            "src": "assets/video/economia-familiar-demo.mp4",
            "poster": "images/projects/economia-familiar-poster.jpg",
            "note": (
                "Recorrido por las siete pantallas de la app, en modo claro y oscuro. Los datos son <strong>ficticios</strong>: los de la familia nunca salen de casa.",
                "A walkthrough of the app's seven screens, in light and dark mode. The data is <strong>fictitious</strong>: the family's real data never leaves home.",
            ),
        },
        "illustration": None,
        "link": None,
        "tagline": (
            "App de escritorio para las finanzas de casa: importa el extracto del banco, categoriza los gastos con el criterio histórico de la familia y avisa cuando una partida se pasa de su límite. <strong>Local y sin IA, por privacidad.</strong>",
            "Desktop app for household finances: it imports the bank statement, categorises spending using the family's historical criteria and warns when a category goes over its limit. <strong>Local and AI-free, by design.</strong>",
        ),
        "card": (
            "Sustituye el Excel familiar: importa el CSV del banco sin duplicados, categoriza automáticamente la gran mayoría de los movimientos aprendiendo del histórico y ofrece límites por categoría y una previsión del mes que se puede explicar.",
            "Replaces the family spreadsheet: it imports the bank CSV without duplicates, auto-categorises most transactions by learning from history, and provides per-category limits and an explainable monthly forecast.",
        ),
        "chips": ["Python 3.12", "Flet (Flutter)", "SQLite", "openpyxl", "smtplib", "pytest", "Windows .exe"],
        "facts": [
            ("94 %", "categorizados sin intervención en la validación con datos reales", "auto-categorised in the real-data validation"),
            ("1.839", "movimientos etiquetados de los que aprende", "labelled transactions it learns from"),
            ("~340", "tests automáticos", "automated tests"),
            ("0", "datos en la nube", "data in the cloud"),
        ],
        "what": (
            [
                "Llevar las cuentas de casa en Excel funciona hasta que deja de hacerlo: copiar movimientos a mano, categorizarlos uno a uno y darse cuenta a fin de mes de que una partida se ha disparado. Economía Familiar automatiza ese proceso sin sacar los datos del ordenador.",
                "Importas el extracto CSV del banco y la app descarta los duplicados, categoriza cada movimiento con el mismo criterio que la familia ha usado históricamente y deja en una bandeja solo los que no sabe clasificar. Al confirmarlos, aprende.",
                "Encima hay un dashboard que compara cada categoría con su límite o con su media y lleva aparte los gastos excepcionales (cuentan para el ahorro, pero no distorsionan las medias). Se completa con límites mensuales sugeridos desde el histórico, avisos en la app (y por email, si lo activas) y una previsión del gasto del mes que indica de dónde sale cada cifra.",
            ],
            [
                "Keeping household accounts in a spreadsheet works until it doesn't: copying transactions by hand, categorising them one by one and finding out at the end of the month that one category has gone through the roof. Economía Familiar (“Family Finances”) automates that process without data ever leaving the computer.",
                "You import the bank's CSV statement and the app discards duplicates, categorises each transaction with the same criteria the family has used historically and leaves only the ones it can't classify in an inbox. When you confirm them, it learns.",
                "On top of that there is a dashboard that compares each category with its limit or its average and keeps one-off expenses apart (they count towards savings but don't skew the averages). It is completed by monthly limits suggested from history, in-app alerts (and email, if you turn it on) and a forecast of the month's spending that explains where each figure comes from.",
            ],
        ),
        "arch_intro": (
            [
                "Es una app de escritorio en Python con tres capas. La interfaz Flet tiene siete páginas (dashboard, movimientos, importar, pendientes, categorías, límites y previsión) y solo habla con los servicios, que son los casos de uso. Debajo hay un núcleo puro, sin base de datos ni red, con el categorizador, la detección de duplicados, la previsión y los límites.",
                "Los extractos entran por un adaptador por banco (hoy CaixaBank) y el criterio de categorías se aprende al arrancar de los Excel históricos de la familia. Todo se guarda en un SQLite local; si se elige una carpeta de Google Drive, es Drive quien la sincroniza. El único servicio externo es el email opcional para los avisos de límites.",
            ],
            [
                "It is a three-layer Python desktop app. The Flet UI has seven pages (dashboard, transactions, import, pending, categories, limits and forecast) and only talks to the services, which are the use cases. Underneath sits a pure core, with no database or network access, holding the categoriser, duplicate detection, forecast and limits.",
                "Statements come in through one adapter per bank (CaixaBank today) and the category criteria are learned at start-up from the family's historical spreadsheets. Everything is stored in a local SQLite file; if a Google Drive folder is chosen, Drive syncs it. The only external service is optional email for limit alerts.",
            ],
        ),
        "decisions": [
            ("Sin IA, por privacidad",
             "Los movimientos bancarios no salen del ordenador. La categorización es estadística: voto mayoritario por comercio a partir del histórico, más la memoria de lo que el usuario confirma. Cada movimiento guarda de dónde viene su categoría.",
             "No AI, on purpose",
             "Bank transactions never leave the computer. Categorisation is statistical: a majority vote per merchant learned from history, plus memory of what the user confirms. Each transaction records where its category came from."),
            ("Arquitectura por capas con núcleo puro",
             "El núcleo no conoce ni el banco ni la interfaz, y un test automático lo vigila. Añadir otro banco es escribir un adaptador; llevarlo al móvil solo cambiaría la capa de presentación.",
             "Layered architecture with a pure core",
             "The core knows nothing about the bank or the UI, and an automated test enforces it. Adding another bank means writing an adapter; moving to mobile would only change the presentation layer."),
            ("Previsión que se puede explicar",
             "En lugar de una regla de tres, la previsión es el máximo entre el gasto real y la media del mismo mes en años anteriores (o la media general). Los meses atípicos se descartan con el criterio de Tukey para que, por ejemplo, una compra extraordinaria no infle la previsión.",
             "An explainable forecast",
             "Instead of a simple extrapolation, the forecast is the maximum of actual spending and the average for the same month in previous years (or the overall average). Outlier months are discarded using Tukey's rule so that, for instance, a one-off purchase doesn't inflate the forecast."),
            ("Del prototipo al producto",
             "El núcleo de un prototipo ya validado se portó tal cual con sus tests de regresión en lugar de rediseñarlo. Desarrollo guiado por specs, TDD y 19 ADRs.",
             "From prototype to product",
             "The core of an already validated prototype was ported as-is with its regression tests instead of being redesigned. Spec-driven development, TDD and 19 ADRs."),
            ("Local-first con sincronización sencilla",
             "Una app de escritorio para Windows con los datos en Documentos. Si se elige una carpeta de Google Drive, es el cliente de Drive quien la sincroniza entre los dos PCs, con una regla simple: una persona a la vez. Por eso la base de datos se cierra limpia al salir y nunca se sube un archivo a medio escribir.",
             "Local-first, with simple sync",
             "A Windows desktop app with data in Documents. If a Google Drive folder is chosen, the Drive client syncs it between the two PCs under a simple rule: one person at a time. That's why the database is closed cleanly on exit, so a half-written file is never uploaded."),
        ],
    },
]

PREVIOUS = [
    {"name": ("Clasificador de tumores cerebrales", "Brain Tumor Classifier"), "href": "MRI.html", "img": "images/IMG0.jpeg",
     "desc": ("Redes convolucionales (VGG16, VGG19, Inception V3) para clasificar tumores en resonancias magnéticas. 84 % de accuracy y 100 % de recall.",
              "Convolutional networks (VGG16, VGG19, Inception V3) to classify tumours in MRI scans. 84% accuracy and 100% recall.")},
    {"name": ("Potencial económico del teletrabajo en España", "The economic potential of telework in Spain"), "href": "EDA.html", "img": "images/IMG2.jpeg",
     "desc": ("Análisis exploratorio del mercado laboral, el poder adquisitivo y el precio de la vivienda según el lugar de residencia.",
              "Exploratory analysis of the labour market, purchasing power and housing prices depending on place of residence.")},
    {"name": ("Gluby, el asistente de tu acuario", "Gluby, your aquarium assistant"), "href": "Gluby.html", "img": "images/IMG3.jpeg",
     "desc": ("Proyecto multidisciplinar: modelo de detección de peces con CNN desplegado en AWS, liderando el equipo de Data Science.",
              "Multidisciplinary project: a CNN fish-detection model deployed on AWS, leading the Data Science team.")},
    {"name": ("Hackathon JOBMadrid21", "JOBMadrid21 hackathon"), "href": "https://github.com/Jcornejo85/JOBMadrid21", "img": "images/IMG4.png",
     "desc": ("Análisis exploratorio y modelo predictivo de precios integrado con el resto de verticales del equipo.",
              "Exploratory analysis and a price-prediction model integrated with the team's other verticals.")},
    {"name": ("Broomlib", "Broomlib"), "href": "https://github.com/Jcornejo85/broomlib", "img": "images/IMG5.png",
     "desc": ("Paquete de Python para el preanálisis rápido de datasets numéricos y categóricos.",
              "Python package for fast pre-analysis of numerical and categorical datasets.")},
    {"name": ("Clasificador de erupciones volcánicas", "Volcano eruption classifier"), "href": "https://github.com/Jcornejo85/Clasificador-volcanes", "img": "images/IMG6.jpeg",
     "desc": ("Random Forest que predice el tipo de erupción a partir de datos de sensores en las laderas del volcán.",
              "Random Forest predicting eruption type from sensor data on the volcano's slopes.")},
]
