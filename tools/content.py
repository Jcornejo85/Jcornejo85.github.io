# -*- coding: utf-8 -*-
"""Contenido bilingüe (ES/EN) de los proyectos del portfolio.

Editar aquí y regenerar con:  python3 tools/build.py
"""

PROJECTS = [
    # ------------------------------------------------------------------ CareerCraft
    {
        "slug": "careercraft",
        "name": "CareerCraft",
        "cover": "images/projects/careercraft-cover.svg",
        "video": None,  # p. ej. {"src": "assets/video/careercraft-demo.mp4", "poster": "images/projects/careercraft-poster.jpg"}
        "link": None,
        "tagline": (
            "Asistente de carrera con IA: construye un perfil profesional verificado y genera CVs adaptados a cada oferta <strong>sin inventar nada</strong>.",
            "AI career assistant: it builds a verified professional profile and generates CVs tailored to each job offer <strong>without making anything up</strong>.",
        ),
        "card": (
            "Asistente de carrera con IA que construye tu perfil, analiza cada oferta y genera un CV adaptado que pasa una auditoría de veracidad antes de exportarse. Incluye simulador de entrevistas con feedback STAR.",
            "AI career assistant that builds your profile, analyses each job offer and generates a tailored CV that must pass a truthfulness audit before export. Includes an interview simulator with STAR feedback.",
        ),
        "chips": ["Python", "FastAPI", "React + TypeScript", "Claude (Sonnet / Haiku)", "RAG", "PostgreSQL + pgvector", "Celery + Redis", "WeasyPrint", "Docker"],
        "facts": [
            ("~$0.04", "coste por CV generado", "cost per generated CV"),
            ("20/20", "exageraciones detectadas en el banco de evaluación", "exaggerations caught in the eval set"),
            ("~840", "tests automáticos", "automated tests"),
            ("10", "plantillas PDF legibles por ATS", "ATS-readable PDF templates"),
        ],
        "what": (
            [
                "Escribir un CV distinto para cada oferta es lento, y los generadores con IA tienden a <em>adornar</em> la experiencia. CareerCraft parte de la idea contraria: primero construye una <strong>base de hechos verificada</strong> sobre ti y después redacta a partir de ella con el enfoque más favorable, siempre que siga siendo defendible.",
                "Puedes empezar subiendo tu CV o tu PDF de LinkedIn, o con una entrevista conversacional que solo pregunta por lo que falta. Al pegar una oferta, la app cruza cada requisito con tu perfil (cubierto, implícito con evidencia o ausente), genera el CV en el idioma de la oferta y lo somete a una auditoría antes de dejarte exportarlo.",
            ],
            [
                "Writing a different CV for every job offer is slow, and AI generators tend to <em>embellish</em> experience. CareerCraft takes the opposite approach: it first builds a <strong>verified fact base</strong> about you and then writes from it with the most favourable framing that is still defensible.",
                "You can start by uploading your CV or LinkedIn PDF, or through a conversational interview that only asks about what is missing. When you paste a job offer, the app matches each requirement against your profile (covered, implied with evidence, or missing), generates the CV in the offer's language and audits it before letting you export it.",
            ],
        ),
        "flow": (
            """flowchart TD
  A["Subes tu CV / LinkedIn<br/>o pegas texto"] --> B["La IA extrae los datos<br/>con confianza por campo"]
  A2["Entrevista conversacional<br/>(solo pregunta lo que falta)"] --> C
  B --> C["Revisas y confirmas<br/>nada entra sin tu OK"]
  C --> D[("Perfil verificado")]
  D --> E["Indexado para búsqueda semántica<br/>(RAG)"]
  F["Pegas una oferta"] --> G["Análisis de requisitos<br/>+ preguntas para concretar logros"]
  E --> H["Genera el CV adaptado<br/>en el idioma de la oferta"]
  G --> H
  H --> I{"Auditoría de<br/>veracidad"}
  I -- "corrige" --> H
  I --> J["Revisas bullet a bullet<br/>cobertura + score ATS"]
  J --> K["PDF final<br/>(plantillas ATS)"]
  D --> L["Simulador de entrevistas<br/>feedback STAR contra tu perfil"]
""",
            """flowchart TD
  A["Upload your CV / LinkedIn<br/>or paste text"] --> B["AI extracts the data<br/>with per-field confidence"]
  A2["Conversational interview<br/>(asks only what is missing)"] --> C
  B --> C["You review and confirm<br/>nothing enters without your OK"]
  C --> D[("Verified profile")]
  D --> E["Indexed for semantic search<br/>(RAG)"]
  F["Paste a job offer"] --> G["Requirement analysis<br/>+ questions to pin down achievements"]
  E --> H["Generates the tailored CV<br/>in the offer's language"]
  G --> H
  H --> I{"Truthfulness<br/>audit"}
  I -- "fix" --> H
  I --> J["Review bullet by bullet<br/>coverage + ATS score"]
  J --> K["Final PDF<br/>(ATS templates)"]
  D --> L["Interview simulator<br/>STAR feedback against your profile"]
""",
        ),
        "arch": (
            """flowchart TB
  UI["SPA React + TypeScript"] --> API["API FastAPI<br/>(JWT)"]
  subgraph SVC["Servicios"]
    ING["Ingesta<br/>PDF / DOCX"]
    ONB["Onboarding<br/>conversacional"]
    JOB["Análisis de oferta<br/>+ cruce de requisitos"]
    GEN["Generador de CV"]
    QA["Gate de calidad<br/>reglas + jueces LLM"]
    INT["Motor de entrevistas"]
    REN["Render PDF<br/>Jinja2 + WeasyPrint"]
  end
  API --> ING & ONB & JOB & INT & REN
  ING & ONB --> PROF[("Perfil<br/>PostgreSQL")]
  PROF --> RAG["Embeddings"] --> VEC[("pgvector")]
  JOB --> GEN
  PROF --> GEN --> QA
  QA -. "bucle de corrección" .-> GEN
  ING & GEN & QA & JOB & INT --> LLM["Capa LLM<br/>Claude Sonnet / Haiku"]
  LLM --> CRED[("Créditos y costes")]
""",
            """flowchart TB
  UI["React + TypeScript SPA"] --> API["FastAPI API<br/>(JWT)"]
  subgraph SVC["Services"]
    ING["Ingestion<br/>PDF / DOCX"]
    ONB["Conversational<br/>onboarding"]
    JOB["Offer analysis<br/>+ requirement matching"]
    GEN["CV generator"]
    QA["Quality gate<br/>rules + LLM judges"]
    INT["Interview engine"]
    REN["PDF render<br/>Jinja2 + WeasyPrint"]
  end
  API --> ING & ONB & JOB & INT & REN
  ING & ONB --> PROF[("Profile<br/>PostgreSQL")]
  PROF --> RAG["Embeddings"] --> VEC[("pgvector")]
  JOB --> GEN
  PROF --> GEN --> QA
  QA -. "correction loop" .-> GEN
  ING & GEN & QA & JOB & INT --> LLM["LLM layer<br/>Claude Sonnet / Haiku"]
  LLM --> CRED[("Credits & costs")]
""",
        ),
        "decisions": [
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
             "Cada tarea usa el modelo que necesita (Haiku para extraer, Sonnet para redactar), con prompt caching y un ledger de créditos atómico. Coste medido: unos 4 céntimos de dólar por CV.",
             "Cost under control",
             "Each task uses the model it needs (Haiku to extract, Sonnet to write), with prompt caching and an atomic credit ledger. Measured cost: about 4 US cents per CV."),
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
        "flow": (
            """flowchart TD
  ESC["Escuela<br/>lección + ejercicio"] --> F[("Fichas del mundo<br/>personajes, lugares, facciones…")]
  F <--> MESA["Mesa de trabajo<br/>lienzo infinito"]
  F --> V["Vistas derivadas<br/>cronología · relaciones · hilos · estructuras"]
  F --> MAN["Manuscrito por escenas<br/>menciones + corrector"]
  MAN --> DOCX["Exportar a Word"]
  INV["Investigación hecha con Claude<br/>(documento HTML)"] --> IMP["Importar y enlazar<br/>con fichas"] --> F
  F --> CTX["Contexto visible y editable<br/>ficha + relaciones + búsqueda"]
  CTX --> IA["Asistente IA<br/>revisa continuidad, pregunta, sugiere"]
  IA -. "no escribe la prosa" .-> MAN
  F --> GAL["Galería<br/>ilustraciones de personajes y escenas"]
""",
            """flowchart TD
  ESC["School<br/>lesson + exercise"] --> F[("World entities<br/>characters, places, factions…")]
  F <--> MESA["Workbench<br/>infinite canvas"]
  F --> V["Derived views<br/>timeline · relationships · threads · structures"]
  F --> MAN["Scene-based manuscript<br/>mentions + spell checker"]
  MAN --> DOCX["Export to Word"]
  INV["Research done with Claude<br/>(HTML document)"] --> IMP["Import and link<br/>to entities"] --> F
  F --> CTX["Visible, editable context<br/>entity + relations + search"]
  CTX --> IA["AI assistant<br/>checks continuity, asks, suggests"]
  IA -. "never writes the prose" .-> MAN
  F --> GAL["Gallery<br/>character and scene illustrations"]
""",
        ),
        "arch": (
            """flowchart TB
  subgraph APP["App de escritorio (Tauri 2)"]
    UI["UI React 19<br/>+ stores Zustand"] --> CORE["core/<br/>TypeScript puro"]
    CORE --> PLAT["Capa de plataforma"]
    CORE --> CTX["Constructor de contexto"]
    RUST["Proceso Rust<br/>red + llavero"]
  end
  PLAT --> FS[("Carpeta del proyecto<br/>Markdown + YAML + JSON Canvas")]
  FS --> IDX[("Índice SQLite + FTS5<br/>en WASM, reconstruible")]
  IDX --> CTX
  CTX --> RUST
  RUST --> KEY[("Llavero del SO")]
  RUST --> ANT["Claude API<br/>streaming"]
  RUST --> OLL["Ollama<br/>(local)"]
  RUST --> OAI["OpenAI Images"]
  RUST -. "eventos en streaming" .-> UI
""",
            """flowchart TB
  subgraph APP["Desktop app (Tauri 2)"]
    UI["React 19 UI<br/>+ Zustand stores"] --> CORE["core/<br/>pure TypeScript"]
    CORE --> PLAT["Platform layer"]
    CORE --> CTX["Context builder"]
    RUST["Rust process<br/>network + keychain"]
  end
  PLAT --> FS[("Project folder<br/>Markdown + YAML + JSON Canvas")]
  FS --> IDX[("SQLite + FTS5 index<br/>in WASM, rebuildable")]
  IDX --> CTX
  CTX --> RUST
  RUST --> KEY[("OS keychain")]
  RUST --> ANT["Claude API<br/>streaming"]
  RUST --> OLL["Ollama<br/>(local)"]
  RUST --> OAI["OpenAI Images"]
  RUST -. "streaming events" .-> UI
""",
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
             "Las claves de API se guardan en el llavero del sistema y nunca llegan a JavaScript. Todas las peticiones salen desde Rust hacia una lista cerrada de destinos, y la CSP impide conexiones directas desde la interfaz.",
             "Secure-by-design AI",
             "API keys live in the OS keychain and never reach JavaScript. Every request goes out through Rust to a closed list of destinations, and the CSP blocks direct network calls from the UI."),
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
            ("RLS", "aislamiento de datos por hogar", "per-household data isolation"),
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
        "flow": (
            """flowchart TD
  R1["Una frase, una web<br/>o texto pegado"] --> AI1["Claude estructura la receta"]
  AI1 --> REC["Encaje con el catálogo<br/>+ aviso de alérgenos"]
  REC --> REV1["Revisas y guardas"] --> BOOK[("Recetario")]
  T["Foto o PDF del ticket"] --> VIS["Claude Vision<br/>lee las líneas"] --> REV2["Revisas"] --> PAN[("Despensa")]
  P["«Semana ligera,<br/>pescado dos días»"] --> HK["Haiku interpreta<br/>la petición"]
  HK --> FIL["Filtro determinista<br/>sin alérgenos · ≤ 40 recetas"]
  BOOK --> FIL
  FIL --> SON["Sonnet compone<br/>el menú"] --> REV3["Revisas"] --> MENU[("Menú semanal")]
  MENU --> LIST["Lista de la compra<br/>= menú − despensa"]
  PAN --> LIST
  LIST --> RT["Compartida en tiempo real<br/>con la familia"]
  MENU --> COOK["Modo cocina<br/>descuenta de la despensa"] --> PAN
""",
            """flowchart TD
  R1["A sentence, a website<br/>or pasted text"] --> AI1["Claude structures the recipe"]
  AI1 --> REC["Match against the catalogue<br/>+ allergen warning"]
  REC --> REV1["Review and save"] --> BOOK[("Recipe book")]
  T["Receipt photo or PDF"] --> VIS["Claude Vision<br/>reads the lines"] --> REV2["Review"] --> PAN[("Pantry")]
  P["“Light week,<br/>fish twice”"] --> HK["Haiku interprets<br/>the request"]
  HK --> FIL["Deterministic filter<br/>no allergens · ≤ 40 recipes"]
  BOOK --> FIL
  FIL --> SON["Sonnet composes<br/>the menu"] --> REV3["Review"] --> MENU[("Weekly menu")]
  MENU --> LIST["Shopping list<br/>= menu − pantry"]
  PAN --> LIST
  LIST --> RT["Shared in real time<br/>with the family"]
  MENU --> COOK["Cooking mode<br/>deducts from the pantry"] --> PAN
""",
        ),
        "arch": (
            """flowchart TB
  U["Móvil (PWA)"] --> FE["Next.js 16 / React 19<br/>+ service worker"]
  FE --> TRPC["API tRPC<br/>(serverless en Vercel)"]
  TRPC --> MW["Middlewares<br/>auth · hogar · plan · cupo IA"]
  MW --> AIL["Capa IA<br/>tool-use + Zod + guardarraíles"]
  AIL --> HAI["Claude Haiku"]
  AIL --> SON["Claude Sonnet"]
  AIL --> VIS["Sonnet Vision"]
  AIL --> WEB["Webs de recetas<br/>(fetch anti-SSRF)"]
  AIL --> LED[("Ledger de coste")]
  TRPC --> DB[("Supabase Postgres<br/>Drizzle + RLS")]
  FE --> ST[("Storage<br/>imágenes")]
  DB --> RT["Realtime"] --> FE
""",
            """flowchart TB
  U["Mobile (PWA)"] --> FE["Next.js 16 / React 19<br/>+ service worker"]
  FE --> TRPC["tRPC API<br/>(serverless on Vercel)"]
  TRPC --> MW["Middlewares<br/>auth · household · plan · AI quota"]
  MW --> AIL["AI layer<br/>tool-use + Zod + guardrails"]
  AIL --> HAI["Claude Haiku"]
  AIL --> SON["Claude Sonnet"]
  AIL --> VIS["Sonnet Vision"]
  AIL --> WEB["Recipe websites<br/>(SSRF-safe fetch)"]
  AIL --> LED[("Cost ledger")]
  TRPC --> DB[("Supabase Postgres<br/>Drizzle + RLS")]
  FE --> ST[("Storage<br/>images")]
  DB --> RT["Realtime"] --> FE
""",
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
            ("Datos multi-hogar seguros",
             "Row Level Security en Postgres junto con un middleware de hogar en cada endpoint. La lista de la compra se comparte por Supabase Realtime en un componente aislado.",
             "Safe multi-household data",
             "Postgres Row Level Security combined with a household middleware on every endpoint. The shopping list is shared via Supabase Realtime in an isolated component."),
        ],
    },
    # ------------------------------------------------------------------ Economía Familiar
    {
        "slug": "economia-familiar",
        "name": "Economía Familiar",
        "cover": "images/projects/economia-familiar-cover.svg",
        "video": None,
        "link": None,
        "tagline": (
            "App de escritorio para las finanzas de casa: importa el extracto del banco, categoriza los gastos con el criterio histórico de la familia y avisa antes de pasarse del presupuesto. <strong>Local y sin IA, por privacidad.</strong>",
            "Desktop app for household finances: it imports the bank statement, categorises spending using the family's historical criteria and warns before the budget is exceeded. <strong>Local and AI-free, by design.</strong>",
        ),
        "card": (
            "Sustituye el Excel familiar: importa el CSV del banco sin duplicados, categoriza el 94 % de los movimientos de forma automática aprendiendo del histórico y ofrece límites por categoría y una previsión del mes que se puede explicar.",
            "Replaces the family spreadsheet: it imports the bank CSV without duplicates, auto-categorises 94% of transactions by learning from history, and provides per-category limits and an explainable monthly forecast.",
        ),
        "chips": ["Python 3.12", "Flet (Flutter)", "SQLite", "openpyxl", "smtplib", "pytest", "Windows .exe"],
        "facts": [
            ("94 %", "movimientos categorizados automáticamente", "transactions auto-categorised"),
            ("1.839", "movimientos históricos de aprendizaje", "historical transactions learned from"),
            ("~340", "tests automáticos", "automated tests"),
            ("0", "datos en la nube", "data in the cloud"),
        ],
        "what": (
            [
                "Llevar las cuentas de casa en Excel funciona hasta que deja de hacerlo: copiar movimientos a mano, categorizarlos uno a uno y darse cuenta a fin de mes de que una partida se ha disparado. Economía Familiar automatiza ese proceso sin sacar los datos del ordenador.",
                "Importas el extracto CSV del banco y la app descarta los duplicados, categoriza cada movimiento con el mismo criterio que la familia ha usado históricamente y deja en una bandeja solo los que no sabe clasificar. Al confirmarlos, aprende. Encima hay un dashboard, límites mensuales por categoría con avisos en la app y por email, y una previsión del gasto del mes que indica de dónde sale cada cifra.",
            ],
            [
                "Keeping household accounts in a spreadsheet works until it doesn't: copying transactions by hand, categorising them one by one and finding out at the end of the month that one category has gone through the roof. Economía Familiar (“Family Finances”) automates that process without data ever leaving the computer.",
                "You import the bank's CSV statement and the app discards duplicates, categorises each transaction with the same criteria the family has used historically and leaves only the ones it can't classify in an inbox. When you confirm them, it learns. On top of that there is a dashboard, monthly limits per category with in-app and email alerts, and a forecast of the month's spending that explains where each figure comes from.",
            ],
        ),
        "flow": (
            """flowchart TD
  CSV["Extracto CSV del banco"] --> ADP["Adaptador del banco<br/>formato, importes, fechas"]
  ADP --> DED["Detecta duplicados"]
  XLS["Excel históricos<br/>de la familia"] --> TRN["Aprende el criterio<br/>comercio → categoría"]
  TRN --> CAT{"¿Categoría<br/>conocida?"}
  DED --> CAT
  CAT -- "sí (~94 %)" --> DB[("SQLite local")]
  CAT -- "no" --> PEN["Bandeja de pendientes<br/>confirmas con un toque"]
  PEN -- "recuerda tu respuesta" --> TRN
  PEN --> DB
  DB --> DASH["Dashboard del mes"]
  DB --> LIM["Límites por categoría<br/>avisos en app y email"]
  DB --> FC["Previsión del mes<br/>real · estacional · media"]
""",
            """flowchart TD
  CSV["Bank CSV statement"] --> ADP["Bank adapter<br/>format, amounts, dates"]
  ADP --> DED["Detects duplicates"]
  XLS["Family's historical<br/>spreadsheets"] --> TRN["Learns the criteria<br/>merchant → category"]
  TRN --> CAT{"Known<br/>category?"}
  DED --> CAT
  CAT -- "yes (~94%)" --> DB[("Local SQLite")]
  CAT -- "no" --> PEN["Pending inbox<br/>confirm with one tap"]
  PEN -- "remembers your answer" --> TRN
  PEN --> DB
  DB --> DASH["Monthly dashboard"]
  DB --> LIM["Per-category limits<br/>in-app and email alerts"]
  DB --> FC["Monthly forecast<br/>actual · seasonal · average"]
""",
        ),
        "arch": (
            """flowchart TB
  U["Usuario"] --> UI["UI Flet<br/>7 páginas"]
  UI --> SVC["Servicios<br/>ingesta · categorías · límites · avisos · previsión"]
  subgraph CORE["core/ (Python puro, sin dependencias de UI ni banco)"]
    CATG["Categorizador"]
    DEDU["Dedup"]
    FCST["Previsión<br/>media robusta (Tukey)"]
    ALR["Límites y avisos"]
  end
  SVC --> CATG & DEDU & FCST & ALR
  SVC --> ADP["Adaptador CaixaBank"]
  SVC <--> DB[("SQLite")]
  DB -. "opcional" .-> DRV["Carpeta Google Drive<br/>(sincronizar 2 PCs)"]
  ALR --> SMTP["Email (SMTP)"]
""",
            """flowchart TB
  U["User"] --> UI["Flet UI<br/>7 pages"]
  UI --> SVC["Services<br/>ingestion · categories · limits · alerts · forecast"]
  subgraph CORE["core/ (pure Python, no UI or bank dependencies)"]
    CATG["Categoriser"]
    DEDU["Dedup"]
    FCST["Forecast<br/>robust mean (Tukey)"]
    ALR["Limits & alerts"]
  end
  SVC --> CATG & DEDU & FCST & ALR
  SVC --> ADP["CaixaBank adapter"]
  SVC <--> DB[("SQLite")]
  DB -. "optional" .-> DRV["Google Drive folder<br/>(sync 2 PCs)"]
  ALR --> SMTP["Email (SMTP)"]
""",
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
             "Un ejecutable de Windows con los datos en Documentos y, opcionalmente, en una carpeta de Google Drive para compartirlos entre dos PCs. La base de datos se cierra limpia al salir para no subir un archivo a medio escribir.",
             "Local-first with simple sync",
             "A Windows executable with data in Documents and, optionally, in a Google Drive folder to share it between two PCs. The database is closed cleanly on exit so a half-written file is never uploaded."),
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
