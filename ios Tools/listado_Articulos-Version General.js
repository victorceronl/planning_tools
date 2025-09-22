(() => {
  // Selecciona elementos del DOM (ajusta los selectores según la página)
  const items = Array.from(document.querySelectorAll(".product, .item, .card, .s-main-slot .s-result-item"));

  const listado = items.map(el => {
    // Intenta encontrar nombre y precio
    const nombre = el.querySelector("h2, h3, .title, .product-title, .a-text-normal")?.innerText.trim() || "Sin nombre";
    const precio = el.querySelector(".price, .a-price-whole, .product-price, .value")?.innerText.trim() || "Sin precio";

    return `${nombre} — ${precio}`;
  }).filter(linea => !linea.includes("Sin nombre") || !linea.includes("Sin precio"));

  if (listado.length === 0) {
    return "No encontré artículos. Ajusta los selectores según el ecommerce.";
  }

  // Lo devuelve en texto plano para que Shortcuts lo use
  return listado.join("\n\n");
})();
