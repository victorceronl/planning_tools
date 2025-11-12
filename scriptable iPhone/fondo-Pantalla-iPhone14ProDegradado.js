// Wallpaper motivacional optimizado para iPhone 14 Pro (1179x2556)
// Fondo negro mate con degradado real y textura granular

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

// ---- fondo degradado real ----
function drawGradient(ctx, colors) {
  const grad = new LinearGradient();
  grad.colors = [new Color(colors[0]), new Color(colors[1])];
  grad.locations = [0, 1];
  ctx.setGradient(grad, new Point(0, 0), new Point(0, ctx.size.height));
  ctx.fillRect(new Rect(0, 0, ctx.size.width, ctx.size.height));
}

// ---- efecto granulado mate ----
function addGrain(ctx, intensity) {
  const totalDots = Math.floor(ctx.size.width * ctx.size.height * intensity * 0.001);
  for (let i = 0; i < totalDots; i++) {
    const x = Math.random() * ctx.size.width;
    const y = Math.random() * ctx.size.height;
    const brightness = Math.random() * 0.2 + 0.4;
    const alpha = Math.random() * 0.15;
    const c = Math.floor(brightness * 255);
    ctx.setFillColor(new Color(`#${c.toString(16).padStart(2, "0").repeat(3)}`, alpha));
    ctx.fillRect(new Rect(x, y, 1.2, 1.2));
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
const safeTop = ctx.size.height * 0.18;
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
