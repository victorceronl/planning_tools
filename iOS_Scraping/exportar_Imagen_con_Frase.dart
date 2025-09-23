// Scriptable: Genera una imagen 3024x4032 con fondo negro y texto centrado

// Pedir al usuario que ingrese el texto
let texto = await Prompt("Ingresa el texto que quieres en la imagen:");

// Configuración de la imagen
const width = 3024;
const height = 4032;

// Crear contexto de dibujo
let img = new DrawContext();
img.size = new Size(width, height);
img.opaque = true;
img.respectScreenScale = false;

// Fondo negro
img.setFillColor(new Color("black"));
img.fillRect(new Rect(0, 0, width, height));

// Configuración del texto
let fontSize = 200; // Puedes ajustar según el texto
let font = Font.systemFont(fontSize); // Helvetica o similar
let textColor = Color.white();

// Crear objeto de texto
let textObj = new Text(texto);
textObj.font = font;
textObj.color = textColor;
textObj.lineBreakMode = 1; // Word wrap
textObj.size = new Size(width * 0.9, height * 0.9); // Ajusta al 90% del canvas

// Medir tamaño del texto para centrar
let textSize = img.measureText(texto, { font: font });
let textX = (width - textSize.width) / 2;
let textY = (height - textSize.height) / 2;

// Dibujar el texto
img.drawText(texto, new Point(textX, textY), textObj);

// Obtener la imagen final
let finalImage = img.getImage();

// Guardar o compartir
finalImage.saveToPhotoAlbum(); // Guarda en Fotos
// Script.setShortcutOutput(finalImage); // Si quieres pasar la imagen a Shortcuts

console.log("Imagen creada y guardada en Fotos ✅");
