// Lista de frases
const frases = [
  "Sigue avanzando, aunque sea lento.",
  "Hoy es un buen día para comenzar.",
  "La disciplina vence al talento.",
  "Un pequeño progreso cada día suma grandes resultados.",
  "Hazlo por tu futuro."
];

// Seleccionar frase aleatoria
const fraseAleatoria = frases[Math.floor(Math.random() * frases.length)];

// Copiar al portapapeles
Pasteboard.copy(fraseAleatoria);

// Mostrar alerta
let alert = new Alert();
alert.title = "Frase aleatoria";
alert.message = fraseAleatoria;
alert.addAction("OK");
await alert.present();