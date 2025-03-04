const btnAdd = document.querySelector(".add-field button");

btnAdd.addEventListener("click", (e) => {
  e.stopPropagation(); // Остановка всплытия события
  document.querySelector(".dropdown-fields").style.display = "block";
});

// Закрытие всех меню при клике вне их
document.addEventListener("click", () => {
  document.querySelector(".dropdown-fields").style.display = "none";
});
