/* Portfolio 2026: portada inmersiva. Una red neuronal 3D (Three.js) que se recorre con el scroll (GSAP ScrollTrigger + Lenis).
   Cómo se comunica cada neurona (simplificado de la biología real):
     1. Llegan señales por las dendritas, desde las puntas hacia el soma.
     2. El soma integra y dispara.
     3. El potencial de acción sale por el axón; en el axón mielinizado salta de nodo en nodo (nodos de Ranvier).
     4. En la terminal sináptica se liberan neurotransmisores hacia la neurona siguiente.
   El texto solo aparece en los puntos de interés. Generado por tools/build.py junto con index.html. */
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const root = document.documentElement;
function hasGL() { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } }
if (!hasGL() || !window.gsap || !window.ScrollTrigger) (window.__static || (() => root.classList.add('static')))();
else boot();

function boot() {
const { gsap, ScrollTrigger } = window;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const small = Math.min(innerWidth, innerHeight) < 700;

/* ---------- utilidades ---------- */
let seed = 20211;
const rnd = () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
const lerp = (a, b, t) => a + (b - a) * t;
const randUnit = () => { const u = rnd() * 2 - 1, th = rnd() * Math.PI * 2, s = Math.sqrt(1 - u * u); return new THREE.Vector3(s * Math.cos(th), u, s * Math.sin(th)); };
const win = (p, a, b, f = 0.01) => smooth(a, a + f, p) * (1 - smooth(b - f, b, p));
const css = (el, prop) => getComputedStyle(el).getPropertyValue(prop).trim();

const C = { lavender: new THREE.Color('#a98bff'), mist: new THREE.Color('#e2d6ff'), violet: new THREE.Color('#7c4dff') };
const VIOLETS = ['#7c4dff', '#8f63ff', '#a98bff', '#6a45d9', '#b77bff', '#cf6bff', '#7c4dff', '#9d7bff'].map(c => new THREE.Color(c));
const pick = () => VIOLETS[(rnd() * VIOLETS.length) | 0];

/* ---------- línea de tiempo (progreso del scroll 0..1) ---------- */
const sceneEls = [...document.querySelectorAll('.scene')];
const oldEls = [...document.querySelectorAll('.old a')];
const NP = sceneEls.length, S0 = 0.37, S1 = 0.89, PL = (S1 - S0) / NP;
const SC = sceneEls.map((el, i) => {
  const s = S0 + i * PL;
  return { el, i, slug: el.id, s, fire: s + 0.27 * PL, show: [s + 0.345 * PL, s + 0.93 * PL], color: new THREE.Color(css(el, '--ch') || '#a98bff'), o: -1 };
});

/* ---------- render ---------- */
const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: 'high-performance' });
const DPR = Math.min(devicePixelRatio || 1, small ? 1.5 : 1.75);
renderer.setPixelRatio(DPR);
renderer.setClearColor(0x000000, 1);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 700);
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const BLOOM = 0.72;
const bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), BLOOM, 0.4, 0.36);
composer.addPass(bloom);
composer.addPass(new OutputPass());

function radial(stops) {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  stops.forEach(([o, a]) => gr.addColorStop(o, `rgba(255,255,255,${a})`));
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}
const SOFT = radial([[0, 1], [0.22, 0.85], [0.55, 0.18], [1, 0]]);
const CORE = radial([[0, 1], [0.12, 0.9], [0.3, 0.22], [0.6, 0.04], [1, 0]]); // núcleo nítido: menos «bola de luz»
const RING = radial([[0, 0], [0.62, 0], [0.8, 0.9], [0.88, 0.5], [1, 0]]);     // anillo: «esta neurona se puede abrir»

const mats = [];
const G = `float g(float x, float c, float w){ float t = (x - c) / w; return exp(-t * t); }`;
// Ciclo de una neurona (0..1): 0–0.36 entradas por dendritas, 0.38 disparo, 0.38–0.9 potencial de acción por el axón.
const CYCLE = `
  float cyc(float seed, float per){ return uAuto > 0.5 ? fract(uTime / per + seed) * uSpan : uDrive; }`;

/* puntos genéricos (tejido, corteza, explosiones) */
function pointsMat({ opacity = 1, gain = 1, near = 3, burst = false, tex = SOFT, maxPx = 24 } = {}) {
  const m = new THREE.ShaderMaterial({
    uniforms: { uTex: { value: tex }, uScale: { value: 500 }, uOpacity: { value: opacity }, uGain: { value: gain }, uProg: { value: 0 }, uNear: { value: near }, uMaxPx: { value: maxPx } },
    vertexShader: `
      attribute float aSize; attribute vec3 aColor; ${burst ? 'attribute vec3 aDir;' : ''}
      uniform float uScale, uProg, uNear, uMaxPx;
      varying vec3 vColor; varying float vFade;
      void main(){
        vec3 p = position ${burst ? '+ aDir * uProg' : ''};
        vec4 mv = modelViewMatrix * vec4(p, 1.0);
        float d = -mv.z;
        gl_PointSize = min(aSize * uScale / max(d, 0.5), uMaxPx);
        vFade = smoothstep(260.0, 40.0, d) * smoothstep(uNear * 0.25, uNear, d);
        vColor = aColor;
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      uniform sampler2D uTex; uniform float uOpacity, uGain;
      varying vec3 vColor; varying float vFade;
      void main(){ float a = texture2D(uTex, gl_PointCoord).a; gl_FragColor = vec4(vColor * uGain, a * uOpacity * vFade); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
  });
  m.userData.px = maxPx; mats.push(m); return m;
}
function makePoints(A, mat) {
  const g = new THREE.BufferGeometry();
  for (const [k, n] of [['position', 3], ['aColor', 3], ['aSize', 1], ['aDir', 3], ['aSeed', 1], ['aPer', 1], ['aOff', 1]]) if (A[k]) g.setAttribute(k, new THREE.Float32BufferAttribute(A[k], n));
  const pts = new THREE.Points(g, mat); pts.frustumCulled = false; scene.add(pts); return pts;
}

/* dendritas y axones: la luz recorre la rama según el ciclo de la neurona */
function treeMat({ auto = false, base = 1, gain = 2.2, span = 1 } = {}) {
  const m = new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 }, uDrive: { value: -1 }, uAuto: { value: auto ? 1 : 0 }, uSpan: { value: span }, uBase: { value: base }, uGain: { value: gain }, uLit: { value: 0 } },
    vertexShader: `
      attribute vec3 aColor; attribute float aDn; attribute float aAx; attribute float aSeed; attribute float aPer;
      uniform float uTime, uDrive, uAuto, uSpan, uBase, uGain, uLit;
      varying vec3 vCol; varying float vB;
      ${G} ${CYCLE}
      void main(){
        float c = cyc(aSeed, aPer), b = 0.0;
        if (c >= 0.0 && c <= 1.0) {
          if (aAx < 0.5) {
            b += c < 0.4 ? g(aDn, 1.0 - c / 0.36, 0.13) * (0.3 + 0.7 * clamp(c / 0.36, 0.0, 1.0)) : 0.0;
            b += g(c, 0.38, 0.035) * (1.0 - aDn) * 1.3;
          } else if (c > 0.36) {
            float f = (c - 0.38) / 0.52;
            b += g(aDn, f, 0.045) * 1.8 + (aDn < f ? exp((aDn - f) * 9.0) * 0.25 : 0.0);
          }
        }
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        vB = (uBase + b * uGain + uLit) * smoothstep(230.0, 22.0, -mv.z);
        vCol = aColor;
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `varying vec3 vCol; varying float vB; void main(){ gl_FragColor = vec4(vCol * vB, 1.0); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
  });
  mats.push(m); return m;
}
/* somas: núcleo pequeño que destella al disparar */
function somaMat({ auto = false, span = 1, gain = 1 } = {}) {
  const m = new THREE.ShaderMaterial({
    uniforms: { uTex: { value: CORE }, uScale: { value: 500 }, uMaxPx: { value: 26 }, uTime: { value: 0 }, uDrive: { value: -1 }, uAuto: { value: auto ? 1 : 0 }, uSpan: { value: span }, uGain: { value: gain }, uLit: { value: 0 } },
    vertexShader: `
      attribute float aSize; attribute vec3 aColor; attribute float aSeed; attribute float aPer;
      uniform float uScale, uMaxPx, uTime, uDrive, uAuto, uSpan, uGain, uLit;
      varying vec3 vColor; varying float vB; varying float vFade;
      ${G} ${CYCLE}
      void main(){
        float c = cyc(aSeed, aPer);
        float flash = (c >= 0.0 && c <= 1.0) ? g(c, 0.38, 0.03) : 0.0;
        float charge = (c >= 0.0 && c < 0.38) ? c / 0.38 * 0.35 : 0.0;
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        float d = -mv.z;
        gl_PointSize = min(aSize * (1.0 + flash * 0.9) * uScale / max(d, 0.5), uMaxPx * (1.0 + flash));
        vB = (0.55 + charge + flash * 2.4 + uLit) * uGain;
        vFade = smoothstep(240.0, 30.0, d) * smoothstep(0.6, 2.5, d);
        vColor = aColor;
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      uniform sampler2D uTex; varying vec3 vColor; varying float vB; varying float vFade;
      void main(){ float a = texture2D(uTex, gl_PointCoord).a; gl_FragColor = vec4(vColor * vB, a * vFade); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
  });
  m.userData.px = 26; mats.push(m); return m;
}
/* axón mielinizado (tubo): vaina tenue, nodos de Ranvier y potencial de acción que salta de nodo en nodo */
function axonMat({ color, seg = 1.8, train = 0 } = {}) {
  const m = new THREE.ShaderMaterial({
    uniforms: { uCol: { value: color.clone() }, uLen: { value: 1 }, uFront: { value: -99 }, uOn: { value: 0 }, uSeg: { value: seg }, uTime: { value: 0 }, uTrain: { value: train }, uVis: { value: 1 } },
    vertexShader: `
      varying vec2 vUv; varying vec3 vN; varying vec3 vV; varying float vFade;
      void main(){
        vUv = uv; vec4 mv = modelViewMatrix * vec4(position, 1.0);
        vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz);
        vFade = smoothstep(200.0, 20.0, -mv.z);
        gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      uniform vec3 uCol; uniform float uLen, uFront, uOn, uSeg, uTime, uTrain, uVis;
      varying vec2 vUv; varying vec3 vN; varying vec3 vV; varying float vFade;
      void main(){
        float x = vUv.x * uLen, m = fract(x / uSeg);
        float node = smoothstep(0.9, 0.95, m) * (1.0 - smoothstep(0.97, 1.0, m));
        float rim = pow(1.0 - abs(dot(vN, vV)), 1.4);
        float d = x - uFront;
        float head = exp(-d * d / 1.6) * (0.55 + 0.7 * node) * 0.9 + exp(-d * d / 9.0) * 0.18;
        float tail = d < 0.0 ? exp(d / 5.0) * 0.12 : 0.0;
        float dd = mod(x - uTime * 6.5, 21.0) - 10.5;
        float spikes = exp(-dd * dd / 1.2) * (0.25 + 0.5 * node) * uTrain;
        float b = (0.03 + 0.04 * node) * (0.3 + rim) + (head + tail) * uOn + spikes * 0.6;
        gl_FragColor = vec4(uCol * b * vFade * uVis, 1.0);
      }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
  });
  mats.push(m); return m;
}

/* anillos de sonar alrededor de las neuronas que se pueden abrir */
function ringMat() {
  const m = new THREE.ShaderMaterial({
    uniforms: { uTex: { value: RING }, uScale: { value: 500 }, uMaxPx: { value: 160 }, uT: { value: 0 }, uOpacity: { value: 0 } },
    vertexShader: `
      attribute float aSize; attribute vec3 aColor; attribute float aOff;
      uniform float uScale, uMaxPx, uT; varying vec3 vColor; varying float vPh;
      void main(){
        vPh = fract(uT + aOff);
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = min(aSize * (0.45 + 1.55 * vPh) * uScale / max(-mv.z, 0.5), uMaxPx);
        vColor = aColor; gl_Position = projectionMatrix * mv;
      }`,
    fragmentShader: `
      uniform sampler2D uTex; uniform float uOpacity; varying vec3 vColor; varying float vPh;
      void main(){ float a = texture2D(uTex, gl_PointCoord).a; gl_FragColor = vec4(vColor, a * uOpacity * (1.0 - vPh) * (1.0 - vPh)); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending
  });
  m.userData.px = 160; mats.push(m); return m;
}

/* ---------- cerebro: corteza de partículas con filamentos ---------- */
const BR = { x: 30, y: 26, z: 42 };
const insideBrain = (v, k = 1) => (v.x / BR.x) ** 2 + (v.y / BR.y) ** 2 + (v.z / BR.z) ** 2 < k;
function shellPoint(d, hemi, depth) {
  const g = 1 + 0.07 * Math.sin(d.x * 9 + d.z * 4) * Math.cos(d.y * 11 - d.z * 6) + 0.045 * Math.sin(d.z * 17 + d.y * 5);
  return new THREE.Vector3(hemi * 3.2 + d.x * (BR.x - 3) * g * depth, d.y * BR.y * g * depth * (d.y < 0 ? 0.82 : 1), d.z * BR.z * g * depth);
}
let shellMat;
{
  const A = { position: [], aColor: [], aSize: [] }, N = small ? 8000 : 14000;
  for (let i = 0; i < N;) {
    const d = randUnit(), hemi = rnd() < 0.5 ? -1 : 1;
    if (d.x * hemi < -0.08) continue;
    const v = shellPoint(d, hemi, 1 - rnd() * rnd() * 0.12);
    A.position.push(v.x, v.y, v.z);
    const c = pick(), k = 0.28 + rnd() * 0.42; A.aColor.push(c.r * k, c.g * k, c.b * k); A.aSize.push(0.26 + rnd() * 0.6); i++;
  }
  for (let f = 0; f < 14; f++) {
    let d = randUnit(); const hemi = d.x < 0 ? -1 : 1, step = randUnit().multiplyScalar(0.05);
    for (let k = 0; k < 70; k++) {
      d.add(step).add(randUnit().multiplyScalar(0.012)).normalize();
      const v = shellPoint(d, hemi, 0.97 + rnd() * 0.03);
      A.position.push(v.x + (rnd() - .5) * .6, v.y + (rnd() - .5) * .6, v.z + (rnd() - .5) * .6);
      const c = rnd() < 0.7 ? C.lavender : C.mist, kk = 0.55 + rnd() * 0.45; A.aColor.push(c.r * kk, c.g * kk, c.b * kk); A.aSize.push(0.5 + rnd() * 0.9);
    }
  }
  shellMat = pointsMat({ opacity: 0.85, near: 28 });
  makePoints(A, shellMat);
}

/* ---------- recorrido de la cámara ---------- */
const curve = new THREE.CatmullRomCurve3([
  [0, 6, 120], [0, 4, 70], [2, 2, 36], [-10, 8, 24], [8, -4, 10], [-6, 6, -2], [12, 10, -10],
  [0, 0, -16], [-14, -6, -22], [6, 8, -30], [16, -8, -24], [0, 14, -10], [0, 50, 30], [70, 40, 110]
].map(p => new THREE.Vector3(...p)), false, 'centripetal');
const UA = SC.map((c, i) => 0.465 + i * (0.165 / Math.max(1, NP - 1)));
const KEYS = [[0, 0], [0.12, 0.215], [0.33, 0.40], [S0, 0.43]];
SC.forEach((c, i) => { c.u = UA[i]; KEYS.push([c.fire, UA[i]], [c.s + 0.91 * PL, UA[i] + 0.012]); });
KEYS.push([0.92, 0.86], [1, 1]);
function uOfP(p) { for (let i = 1; i < KEYS.length; i++) if (p <= KEYS[i][0]) { const [p0, u0] = KEYS[i - 1], [p1, u1] = KEYS[i]; return lerp(u0, u1, (p - p0) / (p1 - p0)); } return 1; }
function pOfU(u) { for (let i = 1; i < KEYS.length; i++) if (u <= KEYS[i][1]) { const [p0, u0] = KEYS[i - 1], [p1, u1] = KEYS[i]; return lerp(p0, p1, (u - u0) / (u1 - u0)); } return 1; }
const UP = new THREE.Vector3(0, 1, 0);
const sideAt = u => new THREE.Vector3().crossVectors(curve.getTangentAt(clamp(u, 0, 1)), UP).normalize();

/* ---------- árboles neuronales ---------- */
const TB = () => ({ position: [], aColor: [], aDn: [], aAx: [], aSeed: [], aPer: [] });
// Dendritas ramificadas (aDn = distancia al soma normalizada) y un axón largo y suave (aAx = 1).
function neuronTree(B, origin, { color, branches, len, depth, axon = 0, axonDir, seedV, per, bright = 1 }) {
  const verts = []; let maxD = 0;
  (function grow(p0, d0, nb, L, dep) {
    for (let b = 0; b < nb; b++) {
      let dir = randUnit(), p = p0.clone(), d = d0; const steps = 4 + ((rnd() * 4) | 0);
      for (let s = 0; s < steps; s++) {
        const q = p.clone().addScaledVector(dir, L / steps), d2 = d + L / steps;
        verts.push([p, d], [q, d2]); maxD = Math.max(maxD, d2);
        dir.add(randUnit().multiplyScalar(0.5)).normalize();
        if (dep > 0 && rnd() < 0.32) grow(q, d2, 1 + (rnd() < 0.4 ? 1 : 0), L * 0.55, dep - 1);
        p = q; d = d2;
      }
    }
  })(origin, 0, branches, len, depth);
  for (const [v, d] of verts) {
    const k = d / maxD; B.position.push(v.x, v.y, v.z);
    const f = (1 - 0.55 * k) * bright; B.aColor.push(color.r * f, color.g * f, color.b * f);
    B.aDn.push(k); B.aAx.push(0); B.aSeed.push(seedV); B.aPer.push(per);
  }
  if (axon > 0) {
    let dir = (axonDir || randUnit()).clone().normalize(), p = origin.clone(); const steps = 30;
    for (let s = 0; s < steps; s++) {
      const q = p.clone().addScaledVector(dir, axon / steps);
      [[p, s / steps], [q, (s + 1) / steps]].forEach(([v, k]) => {
        B.position.push(v.x, v.y, v.z); const f = 0.75 * bright; B.aColor.push(color.r * f, color.g * f, color.b * f);
        B.aDn.push(k); B.aAx.push(1); B.aSeed.push(seedV); B.aPer.push(per);
      });
      dir.add(randUnit().multiplyScalar(0.1)).normalize(); p = q;
    }
  }
}
function treeMesh(B, mat) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(B.position, 3));
  for (const k of ['aColor']) g.setAttribute(k, new THREE.Float32BufferAttribute(B[k], 3));
  for (const k of ['aDn', 'aAx', 'aSeed', 'aPer']) g.setAttribute(k, new THREE.Float32BufferAttribute(B[k], 1));
  const l = new THREE.LineSegments(g, mat); l.frustumCulled = false; scene.add(l); return l;
}

/* fondo: tejido y neuronas con actividad espontánea */
const bgTree = treeMat({ auto: !reduce, base: 1, gain: 2.0, span: 2.6 });
const bgSoma = somaMat({ auto: !reduce, span: 2.6, gain: 0.9 });
{
  const T = { position: [], aColor: [], aSize: [] };
  for (let i = 0; i < (small ? 900 : 1600); i++) {
    const v = new THREE.Vector3((rnd() * 2 - 1) * BR.x, (rnd() * 2 - 1) * BR.y, (rnd() * 2 - 1) * BR.z);
    if (!insideBrain(v, 0.9)) { i--; continue; }
    T.position.push(v.x, v.y, v.z); const c = pick(), k = 0.1 + rnd() * 0.14; T.aColor.push(c.r * k, c.g * k, c.b * k); T.aSize.push(0.07 + rnd() * 0.12);
  }
  makePoints(T, pointsMat({ opacity: 0.7, near: 8, maxPx: 7, tex: CORE }));

  const B = TB(), S = { position: [], aColor: [], aSize: [], aSeed: [], aPer: [] };
  for (let i = 0; i < (small ? 85 : 160); i++) {
    const v = curve.getPointAt(0.21 + rnd() * 0.47).add(randUnit().multiplyScalar(6 + rnd() * 20));
    if (!insideBrain(v, 0.92)) { i--; continue; }
    const c = pick(), sd = rnd(), per = 5 + rnd() * 9;
    neuronTree(B, v, { color: c.clone().multiplyScalar(0.42), branches: 3 + ((rnd() * 3) | 0), len: 4 + rnd() * 5, depth: 1, axon: 8 + rnd() * 10, seedV: sd, per });
    S.position.push(v.x, v.y, v.z); S.aColor.push(c.r * 0.55, c.g * 0.55, c.b * 0.55); S.aSize.push(0.32 + rnd() * 0.36); S.aSeed.push(sd); S.aPer.push(per);
  }
  treeMesh(B, bgTree);
  makePoints(S, bgSoma);
}

/* ---------- axón principal: el impulso que guía el recorrido ---------- */
const AX0 = 0.2, AX1 = 0.67, AXDROP = -3.0;
const axonPts = Array.from({ length: 240 }, (_, i) => curve.getPointAt(lerp(AX0, AX1, i / 239)).addScaledVector(UP, AXDROP));
const axonCurve = new THREE.CatmullRomCurve3(axonPts);
const axonLen = axonCurve.getLength();
const mainAxon = axonMat({ color: C.lavender, train: reduce ? 0 : 1 });
mainAxon.uniforms.uLen.value = axonLen;
scene.add(new THREE.Mesh(new THREE.TubeGeometry(axonCurve, 900, 0.06, 6, false), mainAxon));

/* ---------- neuronas con nombre ---------- */
const NODES = [];
const labelsEl = document.getElementById('labels');
function namedNeuron({ pos, color, big, label, pFire, href }) {
  const tm = treeMat({ base: 0.55, gain: big ? 2.6 : 2.2 });
  const B = TB();
  neuronTree(B, pos, { color, branches: big ? 9 : 5, len: big ? 12 : 6, depth: big ? 2 : 1, axon: big ? 22 : 10, seedV: 0, per: 1, bright: big ? 0.85 : 0.7 });
  const lines = treeMesh(B, tm);
  const sm = somaMat({ gain: big ? 1.2 : 1 });
  makePoints({ position: [pos.x, pos.y, pos.z], aColor: [color.r, color.g, color.b], aSize: [big ? 1.1 : 0.7], aSeed: [0], aPer: [1] }, sm);
  let burst = null;
  if (big) {
    const A = { position: [], aColor: [], aSize: [], aDir: [] };
    for (let i = 0; i < (small ? 200 : 340); i++) {
      A.position.push(pos.x, pos.y, pos.z); const d = randUnit().multiplyScalar(0.35 + rnd() * 0.9); A.aDir.push(d.x, d.y, d.z);
      const c = rnd() < 0.75 ? color : C.mist; A.aColor.push(c.r, c.g, c.b); A.aSize.push(0.08 + rnd() * 0.18);
    }
    burst = pointsMat({ opacity: 0, gain: 1.1, burst: true, tex: CORE, maxPx: 10 }); makePoints(A, burst);
  }
  const ring = ringMat();
  makePoints({ position: [pos.x, pos.y, pos.z, pos.x, pos.y, pos.z], aColor: [color.r, color.g, color.b, color.r, color.g, color.b], aSize: [big ? 3.2 : 1.8, big ? 3.2 : 1.8], aOff: [0, 0.5] }, ring);
  const node = { pos, color, big, tm, sm, burst, label, pFire, ring, ph: rnd(), o: -1, sx: -1e4, sy: -1e4 };
  if (label) { node.el = label; label.style.color = '#' + color.getHexString(); if (!big) label.tabIndex = -1; }
  NODES.push(node); return node;
}
// Proyectos anteriores (2021–2022): neuronas pequeñas junto al recorrido
const nOld = oldEls.length;
oldEls.forEach((el, i) => {
  const u = 0.258 + i * (0.13 / Math.max(1, nOld - 1));
  const pos = curve.getPointAt(u).addScaledVector(sideAt(u), i % 2 ? -5.2 : 5.2).addScaledVector(UP, [1, -1, 1.5, 0.5, -1.5, 1][i % 6]);
  for (let k = 0; k < 40 && !insideBrain(pos, 0.72); k++) pos.multiplyScalar(0.96);
  namedNeuron({ pos, color: C.mist, big: false, label: el, pFire: pOfU(u - 0.003) });
});
// Proyectos 2026: neurona grande delante de la parada, con una sinapsis desde el axón principal
SC.forEach((c, i) => {
  const t = curve.getTangentAt(c.u);
  const pos = curve.getPointAt(c.u).addScaledVector(t, 13).addScaledVector(sideAt(c.u), (i % 2 ? -1 : 1) * 2.7).addScaledVector(UP, [1.5, 1, -1, 1.5][i % 4]);
  const lab = document.createElement('a'); lab.className = 'plabel'; lab.href = c.slug + '.html'; lab.tabIndex = -1; lab.dataset.open = c.slug;
  lab.textContent = c.el.querySelector('h2').textContent; labelsEl.appendChild(lab);
  c.node = namedNeuron({ pos, color: c.color, big: true, label: lab, pFire: c.fire });
  c.node.scene = c;
  c.pos = pos;
  // colateral del axón principal hasta la neurona, con su botón sináptico
  let best = 0, bd = 1e9; axonPts.forEach((q, k) => { const d = q.distanceToSquared(pos); if (d < bd) { bd = d; best = k; } });
  const A = axonPts[best].clone(), dirIn = A.clone().sub(pos).normalize(), E = pos.clone().addScaledVector(dirIn, 1.6);
  const mid = A.clone().lerp(E, 0.5).addScaledVector(UP, 1.8);
  const col = new THREE.CatmullRomCurve3([A, mid, E]);
  const cm = axonMat({ color: c.color, seg: 1.2 }); cm.uniforms.uLen.value = col.getLength(); cm.uniforms.uVis.value = 0;
  scene.add(new THREE.Mesh(new THREE.TubeGeometry(col, 120, 0.05, 6, false), cm));
  c.col = cm;
  const bouton = somaMat({ gain: 0.8 });
  makePoints({ position: [E.x, E.y, E.z], aColor: [c.color.r, c.color.g, c.color.b], aSize: [0.4], aSeed: [0], aPer: [1] }, bouton);
  c.bouton = bouton;
  // vesículas: neurotransmisores que cruzan la hendidura sináptica
  const V = { position: [], aColor: [], aSize: [], aDir: [] };
  for (let k = 0; k < 46; k++) {
    V.position.push(E.x, E.y, E.z);
    const d = dirIn.clone().multiplyScalar(-(0.7 + rnd() * 0.6)).add(randUnit().multiplyScalar(0.28)); V.aDir.push(d.x, d.y, d.z);
    V.aColor.push(C.mist.r, C.mist.g, C.mist.b); V.aSize.push(0.035 + rnd() * 0.04);
  }
  c.ves = pointsMat({ opacity: 0, gain: 1.1, burst: true, tex: CORE, maxPx: 6 }); makePoints(V, c.ves);
});

/* ---------- HUD: texto solo en los puntos de interés ---------- */
const track = document.getElementById('track');
let lenis = null;
const yOf = p => p * (track.offsetHeight - innerHeight) + track.offsetTop;
function scrollToP(p, immediate) {
  if (lenis) lenis.scrollTo(yOf(p), immediate ? { immediate: true } : { duration: 2.4 });
  else window.scrollTo({ top: yOf(p), behavior: immediate || reduce ? 'auto' : 'smooth' });
}
const restOf = c => c.fire + 0.32 * PL; // momento en que la escena se ve completa
const STOPS = [['intro', 0], ['old', 0.25], ...SC.map(c => [c.slug, restOf(c)]), ['contacto', 0.975]];
const progress = document.getElementById('progress'), fill = document.getElementById('fill');
const stopBtns = [...progress.querySelectorAll('button')].map((b, i) => {
  const p = STOPS[i] ? STOPS[i][1] : 1; b.style.top = (p * 100) + '%';
  b.addEventListener('click', () => scrollToP(p)); return { b, p };
});
const fx = [];
const addFx = (el, a, b, f = 0.01, slide = true) => el && fx.push({ el, a, b, f, slide, o: -1 });
addFx(document.getElementById('intro'), -1, 0.05);
addFx(document.getElementById('y2021'), 0.128, 0.172, 0.012, false);
addFx(document.getElementById('y2026'), 0.333, 0.372, 0.01, false);
addFx(document.getElementById('contacto'), 0.905, 2);
function setVis(el, o, slide) {
  el.style.opacity = o;
  if (!reduce && slide) el.style.transform = `translateY(${((1 - o) * 14).toFixed(1)}px)`;
  const hid = o < 0.03; el.style.visibility = hid ? 'hidden' : 'visible'; el.inert = hid;
}
function updateHUD(p) {
  for (const f of fx) {
    let o = f.a < 0 ? 1 - smooth(f.b - f.f, f.b, p) : win(p, f.a, f.b, f.f);
    o = Math.round(o * 100) / 100;
    if (o !== f.o) {
      f.o = o; setVis(f.el, o, f.slide);
      // contacto: un solo destello en orden cada vez que aparece (se rearma al ocultarse)
      if (f.el.id === 'contacto') { if (o > 0.6) f.el.classList.add('lit'); else if (o < 0.05) f.el.classList.remove('lit'); }
    }
  }
  for (const c of SC) {
    let o = Math.round(win(p, c.show[0], c.show[1], 0.012) * 100) / 100;
    if (o !== c.o) {
      c.o = o; c.el.style.opacity = o; c.el.style.setProperty('--in', o);
      const hid = o < 0.03; c.el.style.visibility = hid ? 'hidden' : 'visible'; c.el.inert = hid;
      c.el.classList.toggle('on', o > 0.5);
    }
    const v = c.el.querySelector('video');
    if (v) {
      if (!v.src && p > c.s - 0.02 && p < c.s + PL + 0.02) { v.src = v.dataset.src; v.load(); }
      const want = o > 0.35 && !sheetOpen;
      if (want && v.paused) v.play().catch(() => {}); else if (!want && !v.paused) v.pause();
    }
  }
  fill.style.transform = `scaleY(${p.toFixed(4)})`;
  stopBtns.forEach(s => s.b.classList.toggle('on', p >= s.p - 0.02));
}
const v3 = new THREE.Vector3();
function updateLabels(p) {
  const W = innerWidth, H = innerHeight;
  for (const n of NODES) {
    if (!n.el) continue;
    const w = n.big ? win(p, n.pFire - 0.03, n.pFire + 0.012, 0.008) : win(p, n.pFire - 0.03, n.pFire + 0.003, 0.006);
    v3.copy(n.pos); const dist = v3.distanceTo(camera.position); v3.project(camera);
    const vis = v3.z < 1 && Math.abs(v3.x) < 1.1 && Math.abs(v3.y) < 1.1;
    let o = vis ? w * clamp(1.4 - dist / (n.big ? 45 : 26)) : 0;
    o = Math.round(o * 100) / 100;
    if (o !== n.o) { n.o = o; n.el.style.opacity = o; n.el.style.visibility = o < 0.03 ? 'hidden' : 'visible'; n.el.classList.toggle('live', o > 0.5); n.el.tabIndex = o > 0.5 ? 0 : -1; }
    n.sx = (v3.x * 0.5 + 0.5) * W; n.sy = (-v3.y * 0.5 + 0.5) * H;
    n.clickable = vis && (o > 0.45 || (n.big && n.scene.o > 0.5 && dist < 60));
    if (o > 0) {
      if (!n.el._w) n.el._w = n.el.offsetWidth;
      const x = clamp((v3.x * 0.5 + 0.5) * W + (n.big ? 30 : 14), 12, W - n.el._w - 40);
      n.el.style.transform = `translate(${x.toFixed(1)}px, ${((-v3.y * 0.5 + 0.5) * H - (n.big ? 30 : 12)).toFixed(1)}px)`;
    }
  }
}

/* ---------- ficha completa del proyecto (se carga desde su página) ---------- */
const sheet = document.getElementById('sheet'), sheetBody = document.getElementById('sheet-body'), sheetPage = document.getElementById('sheet-page');
let sheetOpen = false, lastFocus = null;
async function openSheet(slug, trigger) {
  lastFocus = trigger || document.activeElement;
  sheetOpen = true; sheet.hidden = false; root.classList.add('sheet-open');
  if (lenis) lenis.stop();
  sheetPage.href = slug + '.html';
  sheetBody.innerHTML = '<p class="sheet-loading"><span data-l="es">Cargando…</span><span data-l="en">Loading…</span></p>';
  sheet.querySelector('.sheet-close').focus();
  try {
    const r = await fetch(slug + '.html'); if (!r.ok) throw new Error(r.status);
    const doc = new DOMParser().parseFromString(await r.text(), 'text/html');
    const post = doc.querySelector('.post'); if (!post) throw new Error('sin contenido');
    post.querySelectorAll('.actions').forEach(n => n.remove());
    sheetBody.replaceChildren(...[...post.childNodes].map(n => document.importNode(n, true)));
    sheet.scrollTop = 0;
  } catch (e) { location.href = slug + '.html'; }
}
function closeSheet() {
  if (!sheetOpen) return;
  sheetOpen = false; sheet.hidden = true; root.classList.remove('sheet-open');
  sheetBody.querySelectorAll('video').forEach(v => v.pause());
  sheetBody.replaceChildren();
  if (lenis) lenis.start();
  if (lastFocus) lastFocus.focus();
}
document.querySelectorAll('[data-open]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); openSheet(b.dataset.open, b); }));
sheet.querySelector('.sheet-close').addEventListener('click', closeSheet);
sheet.addEventListener('click', e => { if (e.target === sheet) closeSheet(); });
addEventListener('keydown', e => { if (e.key === 'Escape') closeSheet(); });
// Las neuronas con proyecto se pueden pulsar: el cursor cambia y la neurona se ilumina al pasar por encima.
let hovered = null;
function nodeAt(x, y) {
  let best = null, bd = 1e9;
  for (const n of NODES) if (n.clickable) { const d = Math.hypot(n.sx - x, n.sy - y), r = n.big ? 80 : 46; if (d < r && d < bd) { bd = d; best = n; } }
  return best;
}
function setHover(n) {
  if (n === hovered) return;
  if (hovered && hovered.el) hovered.el.classList.remove('hover');
  hovered = n; canvas.style.cursor = n ? 'pointer' : '';
  if (n && n.el) n.el.classList.add('hover');
}
canvas.addEventListener('pointermove', e => { if (e.pointerType === 'mouse') setHover(nodeAt(e.clientX, e.clientY)); });
canvas.addEventListener('pointerleave', () => setHover(null));
canvas.addEventListener('click', e => {
  const n = nodeAt(e.clientX, e.clientY); if (!n) return;
  if (n.big) openSheet(n.scene.slug, n.el);
  else if (n.el.target === '_blank') window.open(n.el.href, '_blank', 'noopener'); else location.href = n.el.href;
});
document.querySelectorAll('.old a, .plabel').forEach(el => {
  el.addEventListener('mouseenter', () => setHover(NODES.find(n => n.el === el) || null));
  el.addEventListener('mouseleave', () => setHover(null));
});
labelsEl.addEventListener('click', e => { const a = e.target.closest('.plabel'); if (a) { e.preventDefault(); openSheet(a.dataset.open, a); } });

/* ---------- tamaño ---------- */
function resize() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h, false); composer.setPixelRatio(DPR); composer.setSize(w, h);
  if (small) bloom.setSize(Math.round(w * DPR / 2), Math.round(h * DPR / 2));
  const portrait = h > w;
  camera.fov = portrait ? 74 : 60; camera.aspect = w / h;
  if (portrait) camera.setViewOffset(w, h, 0, h * 0.1, w, h); else camera.clearViewOffset();
  camera.updateProjectionMatrix();
  const scale = (h * DPR) / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2));
  mats.forEach(m => { if (m.uniforms.uScale) m.uniforms.uScale.value = scale; if (m.uniforms.uMaxPx) m.uniforms.uMaxPx.value = m.userData.px * DPR; });
  NODES.forEach(n => { if (n.el) n.el._w = 0; });
}
addEventListener('resize', resize); resize();

/* ---------- scroll: GSAP ScrollTrigger + Lenis ---------- */
gsap.registerPlugin(ScrollTrigger);
const state = { p: 0 };
if (!reduce && window.Lenis) { lenis = new window.Lenis({ lerp: 0.075, smoothWheel: true }); lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
const st = gsap.to(state, { p: 1, ease: 'none', scrollTrigger: { trigger: '#track', start: 'top top', end: 'bottom bottom', scrub: reduce ? true : (lenis ? 0.7 : 1.2) } });
// Enlaces directos: index.html#careercraft lleva a esa neurona; #projects al primer proyecto (enlaces antiguos)
function jumpToHash() {
  const h = decodeURIComponent(location.hash.slice(1)); if (!h) return;
  const c = SC.find(c => c.slug === h) || (h === 'projects' ? SC[0] : null);
  const p = c ? restOf(c) : h === 'contacto' ? 0.975 : h === 'previous' ? 0.25 : null;
  if (p === null) return;
  scrollToP(p, true); state.p = p; st.scrollTrigger && st.progress(p);
}
addEventListener('hashchange', jumpToHash);
requestAnimationFrame(jumpToHash);

// Movimiento reducido: vistas fijas por parada con un fundido corto, sin vuelo de cámara.
const veil = document.getElementById('veil'); let restIdx = -1;
function restP(p) {
  let i = 0; STOPS.forEach(([, sp], k) => { if (p >= sp - 0.04) i = k; });
  if (i !== restIdx) { if (restIdx !== -1) { veil.style.transition = 'none'; veil.style.opacity = 1; requestAnimationFrame(() => { veil.style.transition = ''; veil.style.opacity = 0; }); } restIdx = i; }
  return STOPS[i][1] === 0 ? 0.02 : STOPS[i][1];
}

/* ---------- bucle ---------- */
const look = new THREE.Vector3(), lookTarget = new THREE.Vector3(), ORIGIN = new THREE.Vector3();
let started = false;
const drive = (p, f) => clamp((p - (f - 0.022)) / 0.058); // entradas → disparo (0.38) → axón
function frame() {
  if (sheetOpen && started) return;
  const t = performance.now() / 1000, p = reduce ? restP(state.p) : state.p, u = uOfP(p);

  // cámara: órbita lenta en la portada, vuelo por la curva dentro del cerebro
  const camPos = curve.getPointAt(clamp(u, 0, 1)).addScaledVector(UP, 1.1);
  if (!reduce) { const o = 1 - smooth(0, 0.09, p); camPos.x += Math.sin(t * 0.4) * 0.25 + Math.sin(t * 0.16) * 26 * o; camPos.y += Math.sin(t * 0.33) * 0.2 + Math.sin(t * 0.11) * 8 * o; }
  camera.position.copy(camPos);
  lookTarget.copy(curve.getPointAt(clamp(u + 0.025, 0, 1)));
  for (const c of SC) { const w = Math.exp(-(((p - (c.fire + 0.02)) / 0.05) ** 2)); lookTarget.lerp(c.pos, 0.8 * w); }
  for (const n of NODES) if (!n.big) { const w = Math.exp(-(((p - n.pFire + 0.012) / 0.012) ** 2)); lookTarget.lerp(n.pos, 0.3 * w); }
  lookTarget.lerp(ORIGIN, 1 - smooth(0.05, 0.12, p));
  lookTarget.lerp(ORIGIN, smooth(0.86, 0.95, p));
  if (!started || reduce || window.__shot) look.copy(lookTarget); else look.lerp(lookTarget, 0.08);
  camera.lookAt(look);

  // impulso por el axón principal
  const inside = smooth(0.12, 0.15, p) * (1 - smooth(0.86, 0.9, p));
  mainAxon.uniforms.uOn.value = inside;
  mainAxon.uniforms.uFront.value = clamp((u + 0.04 - AX0) / (AX1 - AX0), -0.05, 1.05) * axonLen;

  // neuronas: entradas, disparo y salida por el axón
  const outro = smooth(0.86, 0.97, p);
  let maxFire = 0;
  for (const n of NODES) {
    const d = drive(p, n.pFire);
    n.tm.uniforms.uDrive.value = d > 0 && d < 1 ? d : -1;
    n.sm.uniforms.uDrive.value = d > 0 && d < 1 ? d : -1;
    const on = smooth(-0.004, 0.01, p - n.pFire);
    n.tm.uniforms.uBase.value = 0.5 + on * 0.45;
    n.tm.uniforms.uLit.value = n.sm.uniforms.uLit.value = outro * 0.6;
    if (n.big) {
      const fire = Math.exp(-(((p - n.pFire) / 0.012) ** 2)); maxFire = Math.max(maxFire, fire);
      const bp = clamp((p - n.pFire + 0.003) / 0.05);
      n.burst.uniforms.uProg.value = bp * 9;
      n.burst.uniforms.uOpacity.value = bp > 0 && bp < 1 ? (1 - bp) ** 1.4 * 0.85 : 0;
    }
  }
  // sinapsis: el potencial llega por la colateral, se liberan vesículas y la neurona responde
  for (const c of SC) {
    const a = c.fire - 0.03, cl = clamp((p - a) / 0.016);
    c.col.uniforms.uVis.value = win(p, c.s - 0.01, c.s + PL, 0.01);
    c.col.uniforms.uOn.value = cl > 0 && cl < 1 ? 1 : 0;
    c.col.uniforms.uFront.value = cl * c.col.uniforms.uLen.value;
    c.col.uniforms.uTrain.value = reduce ? 0 : win(p, c.fire + 0.01, c.s + PL - 0.005) * 0.6;
    const vq = clamp((p - (a + 0.014)) / 0.016);
    c.ves.uniforms.uProg.value = vq; c.ves.uniforms.uOpacity.value = Math.sin(Math.PI * vq) * 0.9;
    c.bouton.uniforms.uGain.value = (0.5 + 2 * Math.exp(-(((cl - 1) / 0.12) ** 2))) * c.col.uniforms.uVis.value;
  }
  bloom.strength = BLOOM + maxFire * 0.25;
  shellMat.uniforms.uGain.value = 1.3 + 0.7 * (1 - smooth(0.06, 0.13, p)) + 0.9 * outro;
  shellMat.uniforms.uOpacity.value = 0.85 - 0.62 * smooth(0.1, 0.16, p) * (1 - smooth(0.84, 0.9, p));
  bgTree.uniforms.uLit.value = bgSoma.uniforms.uLit.value = outro * 0.4;
  for (const n of NODES) {
    const h = n === hovered ? 1 : 0;
    n.hv = lerp(n.hv || 0, h, 0.15);
    n.ph = (n.ph + (reduce ? 0 : 0.0065 + 0.008 * n.hv)) % 1;
    n.ring.uniforms.uT.value = n.ph;
    const want = n.clickable ? (n.big && n.scene.o > 0.5 ? 0.35 : 0.75) + 0.4 * n.hv : 0;
    n.ring.uniforms.uOpacity.value = lerp(n.ring.uniforms.uOpacity.value, want, 0.12);
    n.sm.uniforms.uGain.value = (n.big ? 1.2 : 1) * (1 + 1.4 * n.hv);
    n.tm.uniforms.uBase.value += 0.6 * n.hv;
  }
  mats.forEach(m => { if (m.uniforms.uTime) m.uniforms.uTime.value = t; });

  composer.render();
  updateHUD(p);
  updateLabels(p);
  if (!started) { started = true; window.__booted = true; }
}
gsap.ticker.add(frame);
document.addEventListener('visibilitychange', () => document.hidden ? gsap.ticker.sleep() : gsap.ticker.wake());
}
