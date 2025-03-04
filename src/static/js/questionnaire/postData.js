document.addEventListener("DOMContentLoaded", () => {
  const maxSymbolsRadios = document.querySelectorAll(
    'input[name="max_symbols"]'
  );
  const staticValueBlock = document.getElementById("static-value-block");
  console.log(staticValueBlock);

  maxSymbolsRadios.forEach((radio) => {
    radio.addEventListener("change", () => {
      if (radio.value === "static") {
        staticValueBlock.style.display = "block";
      } else {
        staticValueBlock.style.display = "none";
      }
    });
  });
});
