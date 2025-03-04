// Получаем все элементы меню
const menus = document.querySelectorAll(".menu");

menus.forEach((menu) => {
  const dropdown = menu.querySelector(".dropdown");

  // Открытие/закрытие конкретного меню
  menu.addEventListener("click", (event) => {
    event.stopPropagation(); // Остановка всплытия события
    const isDropdownVisible = dropdown.style.display === "block";
    // Скрыть все остальные меню
    document.querySelectorAll(".dropdown").forEach((d) => {
      d.style.display = "none";
    });
    // Показать/скрыть текущее меню
    dropdown.style.display = isDropdownVisible ? "none" : "block";
  });
});

// Закрытие всех меню при клике вне их
document.addEventListener("click", () => {
  document.querySelectorAll(".dropdown").forEach((dropdown) => {
    dropdown.style.display = "none";
  });
});
