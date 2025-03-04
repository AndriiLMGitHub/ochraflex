const tabLinks = document.querySelectorAll(".tab-link");
const tabContents = document.querySelectorAll(".tab-content");

tabLinks.forEach((link) => {
  link.addEventListener("click", () => {
    // Remove 'active' class from all links and contents
    tabLinks.forEach((link) => link.classList.remove("active"));
    tabContents.forEach((content) => content.classList.remove("active"));

    // Add 'active' class to clicked link and corresponding content
    link.classList.add("active");
    document.getElementById(link.dataset.tab).classList.add("active");
  });
});
