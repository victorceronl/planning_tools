(() => {
  // Extrae todo el texto de la página
  const texto = document.body.innerText;

  // Devuelve el resultado al Atajo
  completion(texto);
})();