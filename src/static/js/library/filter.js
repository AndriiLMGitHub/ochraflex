// Функція ініціалізації дропдаунів
function initializeDropdownFilter() {
    // Знаходимо всі дропдауни на сторінці
    const dropdown = document.querySelector(".setting-trigger-filter");
    
    const trigger = dropdown.querySelector(".trigger-filter"); // Елемент, який активує меню
    const menu = dropdown.querySelector(".dropdown-menu-setting-filter"); // Саме меню

    // Додаємо обробник кліку на тригер
    trigger.addEventListener("click", (event) => {
        event.preventDefault(); // Запобігаємо стандартним діям елемента, який викликав подію (наприклад, переход на нову сторінку)
        event.stopPropagation(); // Зупиняємо спливання події, щоб не закривати меню
        menu.classList.toggle("open"); // Відкриваємо/закриваємо меню
    });
    
    }
    
// Ініціалізуємо дропдауни після завантаження DOM
document.addEventListener("DOMContentLoaded", initializeDropdownFilter);