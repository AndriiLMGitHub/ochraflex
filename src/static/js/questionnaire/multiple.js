document.addEventListener("DOMContentLoaded", () => {
  let ol = document.querySelectorAll(".create-items ol");
  const btnCreateLi = document.querySelector(".create-button-item button");
  // Checkboxes
  const requiredFill = document.getElementById("required-fill");
  // Checkboxes

  // Element to view or hide
  const span = document.querySelector(".group-form > span");
  // Element to view or hide

  function createLi() {
    let li = document.createElement("li");
    let input = document.createElement("input");

    ol.forEach((list) => {
      list.appendChild(li);
      li.appendChild(input);
      input.classList.add("input_reset");
      input.setAttribute("placeholder", "Введіть пункт");
      input.setAttribute("required", "true");
    });
  }

  // Check if checkbox or radio is checked
  function checkboxOrRadioIsChecked() {
    // Get the checked checkbox state and the help text checkbox state
    const isChecked = requiredFill.checked;

    // Check if either checkbox is checked and show the element accordingly
    if (isChecked) {
      span.style.display = "block";
    } else {
      span.style.display = "none";
    }
  }

  btnCreateLi.addEventListener("click", createLi);
  requiredFill.addEventListener("change", checkboxOrRadioIsChecked);
});
