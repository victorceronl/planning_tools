// Wallpaper motivacional optimizado para iPhone 14 Pro (1179x2556)
// Centrado visual, fondo negro mate granulado

// ---------- CONFIGURACIÓN ----------
const wallpaperSize = { w: 1179, h: 2556 }; // tamaño real iPhone 14 Pro
const backgroundGradient = ["#000000", "#1A1A1A"]; // negro degradado
const grainIntensity = 0.15; // 0.05=sutil, 0.2=marcado
const phraseList = [
  "Hazlo con ganas o no lo hagas.",
  "Pequeños pasos, grandes resultados.",
  "La constancia vence a la resistencia.",
  "Aprende, fabrica, mejora.",
  "Cada pieza cuenta.",
  "Hoy es un buen día para avanzar.",
  "Enfócate en el proceso, no solo en el resultado.",
  "Mejor hecho que perfecto.",
  "No pares hasta estar orgulloso.",
  "Tu disciplina definirá tu destino."
];
const showDate = true;
const saveToPhotos = true;
// -----------------------------------

// Crear contexto
const ctx = new DrawContext();
ctx.size = new Size(wallpaperSize.w, wallpaperSize.h);
ctx.opaque = true;
ctx.setTextAlignedCenter();

// ---- utilidades color ----
function hexToRgb(hex) {
  const h = hex.replace("#", "");
  const bigint = parseInt(h, 16);
  return {
    r: (bigint >> 16) & 255,
    g: (bigint >> 8) & 255,
    b: bigint & 255
  };
}
function componentToHex(c) {
  const s = c.toString(16);
  return s.length == 1 ? "0" + s : s;
}
function rgbToHex(r, g, b) {
  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

// ---- fondo degradado ----
function drawGradient(ctx, colors) {
  const startRgb = hexToRgb(colors[0]);
  const endRgb = hexToRgb(colors[1]);
  const steps = 200;
  for (let i = 0; i < steps; i++) {
    const t = i / (steps - 1);
    const r = Math.round(startRgb.r + (endRgb.r - startRgb.r) * t);
    const g = Math.round(startRgb.g + (endRgb.g - startRgb.g) * t);
    const b = Math.round(startRgb.b + (endRgb.b - startRgb.b) * t);
    const hex = rgbToHex(r, g, b);
    ctx.setFillColor(new Color(hex));
    const y = Math.floor((ctx.size.height / steps) * i);
    ctx.fillRect(new Rect(0, y, ctx.size.width, ctx.size.height / steps));
  }
}

// ---- efecto granulado mate ----
function addGrain(ctx, intensity) {
  const totalDots = Math.floor(ctx.size.width * ctx.size.height * intensity * 0.001);
  for (let i = 0; i < totalDots; i++) {
    const x = Math.random() * ctx.size.width;
    const y = Math.random() * ctx.size.height;
    const brightness = Math.random() * 0.2 + 0.4;
    const alpha = Math.random() * 0.15;
    const colorValue = Math.floor(brightness * 255);
    const hex = rgbToHex(colorValue, colorValue, colorValue);
    ctx.setFillColor(new Color(hex, alpha));
    ctx.fillRect(new Rect(x, y, 1.5, 1.5));
  }
}

// ---- frase aleatoria ----
function pickPhrase() {
  return phraseList[Math.floor(Math.random() * phraseList.length)];
}

// ---- dibujar fondo + textura ----
drawGradient(ctx, backgroundGradient);
addGrain(ctx, grainIntensity);

// ---- definir área segura visual ----
// zona superior: reloj y dynamic island
const safeTop = ctx.size.height * 0.18;
// zona inferior: barra de desbloqueo
const safeBottom = ctx.size.height * 0.12;
const usableHeight = ctx.size.height - safeTop - safeBottom;

// ---- frase principal ----
const phrase = pickPhrase();
const phraseFontSize = Math.floor(ctx.size.width / 11);
ctx.setFont(Font.boldSystemFont(phraseFontSize));
ctx.setTextColor(new Color("#FFFFFF"));
const phraseRect = new Rect(80, safeTop + usableHeight * 0.35, ctx.size.width - 160, usableHeight * 0.3);
ctx.drawTextInRect(phrase, phraseRect);

// ---- fecha ----
if (showDate) {
  const now = new Date();
  const formattedDate = now.toLocaleDateString("es-MX", {
    weekday: "long",
    day: "2-digit",
    month: "short"
  });
  ctx.setFont(Font.regularSystemFont(58));
  ctx.setTextColor(new Color("#E5E7EB"));
  ctx.drawText(formattedDate, new Point(ctx.size.width / 2, safeTop + usableHeight * 0.8));
}

// ---- exportar imagen ----
const img = ctx.getImage();

if (saveToPhotos) {
  try {
    await Photos.save(img);
    const n = new Notification();
    n.title = "Wallpaper creado";
    n.body = "Imagen guardada en Fotos 📸";
    n.schedule();
  } catch (e) {
    console.log("Error al guardar en Fotos: " + e);
  }
}

// vista previa
if (config.runsInApp) {
  QuickLook.present(img);
} else {
  console.log("Imagen creada y guardada en Fotos.");
}