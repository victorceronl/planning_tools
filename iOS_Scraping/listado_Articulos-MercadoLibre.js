(() => {
  // Selecciona los productos en la página de búsqueda de Mercado Libre
  const items = Array.from(document.querySelectorAll("li.ui-search-layout__item"));

  const listado = items.map(el => {
    // Nombre del producto
    const nombre = el.querySelector("h2.ui-search-item__title")?.innerText.trim() || "Sin nombre";

    // Precio del producto
    const precioEntero = el.querySelector(".price-tag-fraction")?.innerText.replace(/[^\d]/g, "") || "";
    const precioDecimal = el.querySelector(".price-tag-cents")?.innerText.replace(/[^\d]/g, "") || "00";
    const precio = precioEntero ? `$${precioEntero}.${precioDecimal}` : "Sin precio";

    return `${nombre} — ${precio}`;
  }).filter(linea => !linea.includes("Sin nombre") && !linea.includes("Sin precio"));

  if (listado.length === 0) {
    return "No encontré artículos. Asegúrate de estar en una página de búsqueda de Mercado Libre.";
  }

  // Devuelve texto plano para Shortcuts
  return listado.join("\n\n");
})();
