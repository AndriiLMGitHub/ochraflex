const btnClose = document.querySelector(".btn-close");
const alert = document.querySelector(".alert");

if (btnClose){
  btnClose.addEventListener("click", () => {
    alert.style.display = "none";
    btnClose.removeEventListener("click", () => {}); // Remove event listener after alert is closed
  });
}
