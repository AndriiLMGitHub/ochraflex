// Функція ініціалізації дропдаунів
function initializeDropdowns() {
  // Знаходимо всі дропдауни на сторінці
  const dropdowns = document.querySelectorAll(".dropdown-setting");

  dropdowns.forEach((dropdown) => {
    const trigger = dropdown.querySelector(".trigger"); // Елемент, який активує меню
    const menu = dropdown.querySelector(".dropdown-menu-setting"); // Саме меню

    // Додаємо обробник кліку на тригер
    trigger.addEventListener("click", (event) => {
      event.preventDefault(); // Запобігаємо стандартним діям елемента, який викликав подію (наприклад, переход на нову сторінку)
      event.stopPropagation(); // Зупиняємо спливання події, щоб не закривати меню
      closeAllDropdowns(); // Закриваємо всі відкриті меню перед відкриттям цього
      menu.classList.toggle("open"); // Відкриваємо/закриваємо меню
    });
  });

  // Закриваємо меню при кліку за межами
  document.addEventListener("click", () => {
    closeAllDropdowns();
  });

  // Закриваємо всі відкриті меню
  function closeAllDropdowns() {
    dropdowns.forEach((dropdown) => {
      const menu = dropdown.querySelector(".dropdown-menu-setting");
      menu.classList.remove("open"); // Закриваємо меню
    });
  }
}

// Ініціалізуємо дропдауни після завантаження DOM
document.addEventListener("DOMContentLoaded", initializeDropdowns);
