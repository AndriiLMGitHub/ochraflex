document.addEventListener('DOMContentLoaded', function() {
    const burgerIcon = document.querySelector('.burger-icon');
    const menuItems = document.querySelector('.menu-items');

    burgerIcon.addEventListener('click', function(event) {
        event.preventDefault();
        menuItems.classList.toggle('active');
    });

    // Закрити меню, якщо клікнуто поза ним
    document.addEventListener('click', function(event) {
        if (!menuItems.contains(event.target) && !burgerIcon.contains(event.target)) {
            menuItems.classList.remove('active');
        }
    });
});