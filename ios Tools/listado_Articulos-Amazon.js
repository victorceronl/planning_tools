(() => {
  // Selecciona los productos en la página de resultados de Amazon
  const items = Array.from(document.querySelectorAll("div.s-main-slot > div.s-result-item"));

  const listado = items.map(el => {
    // Nombre del producto
    const nombre = el.querySelector("h2 a span")?.innerText.trim() || "Sin nombre";
    
    // Precio del producto
    const precioEntero = el.querySelector(".a-price-whole")?.innerText.replace(/[^\d]/g, "") || "";
    const precioDecimal = el.querySelector(".a-price-fraction")?.innerText.replace(/[^\d]/g, "") || "00";
    const precio = precioEntero ? `$${precioEntero}.${precioDecimal}` : "Sin precio";

    return `${nombre} — ${precio}`;
  }).filter(linea => !linea.includes("Sin nombre") && !linea.includes("Sin precio"));

  if (listado.length === 0) {
    return "No encontré artículos. Asegúrate de estar en una página de búsqueda de Amazon.";
  }

  // Devuelve texto plano para Shortcuts
  return listado.join("\n\n");
})();
