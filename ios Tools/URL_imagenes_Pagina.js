(() => {
  // Selecciona todas las imágenes visibles
  const imgs = Array.from(document.querySelectorAll("img"))
    .map(img => img.src)   // obtiene la URL
    .filter(url => url && url.startsWith("http")); // filtra URLs válidas

  if (imgs.length === 0) {
    completion("No se encontraron imágenes en esta página.");
  } else {
    // Devuelve las URLs separadas por salto de línea
    completion(imgs.join("\n\n\n"));
  }
})();
