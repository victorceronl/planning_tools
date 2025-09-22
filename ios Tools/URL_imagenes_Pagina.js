(() => {
  // Selecciona todas las imágenes visibles
  const imgs = Array.from(document.querySelectorAll("img"))
    .map(img => img.src)   // obtiene la URL
    .filter(url => url && url.startsWith("http")); // filtra URLs válidas

  if (imgs.length === 0) {
    return "No se encontraron imágenes en esta página.";
  }

  // Devuelve las URLs separadas por salto de línea para que Shortcuts las use
  return imgs.join("\n");
})();


//Genera un listado de URL directo de cada una de las imagenes de una pagina Web