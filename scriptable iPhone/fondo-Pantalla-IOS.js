// Wallpaper motivacional con fondo granulado mate — Scriptable

// ---------- CONFIGURACIÓN ----------
const wallpaperSize = { w: 1290, h: 2796 }; // tamaño imagen (ajusta según tu iPhone)
const backgroundGradient = ["#000000", "#1A1A1A"]; // negro con leve degradado
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
const showDate = true; // muestra la fecha actual
const saveToPhotos = true; // guarda en Fotos automáticamente
const grainIntensity = 0.15; // 0.05 = suave, 0.2 = fuerte
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
    const brightness = Math.random() * 0.2 + 0.4; // gris medio
    const alpha = Math.random() * 0.15; // transparencia
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

// dibujar fondo + textura
drawGradient(ctx, backgroundGradient);
addGrain(ctx, grainIntensity);

// ---- frase principal ----
const phrase = pickPhrase();
const phraseFontSize = Math.floor(ctx.size.width / 12); // tamaño texto principal
ctx.setFont(Font.boldSystemFont(phraseFontSize));
ctx.setTextColor(new Color("#FFFFFF"));
const phraseRect = new Rect(80, ctx.size.height * 0.4, ctx.size.width - 160, ctx.size.height * 0.3);
ctx.drawTextInRect(phrase, phraseRect);

// ---- fecha ----
if (showDate) {
  const now = new Date();
  const formattedDate = now.toLocaleDateString("es-MX", {
    weekday: "long",
    day: "2-digit",
    month: "short"
  });
  ctx.setFont(Font.regularSystemFont(60)); // tamaño aumentado
  ctx.setTextColor(new Color("#E5E7EB"));
  ctx.drawText(formattedDate, new Point(ctx.size.width / 2, ctx.size.height - 140));
}

// ---- exportar imagen ----
const img = ctx.getImage();

// Guardar o mostrar
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

// Vista previa
if (config.runsInApp) {
  QuickLook.present(img);
} else {
  console.log("Imagen creada y guardada en Fotos.");
}