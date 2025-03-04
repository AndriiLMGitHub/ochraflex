document.addEventListener("DOMContentLoaded", () => {
  let ol = document.querySelectorAll(".create-items ol");
  const btnCreateLi = document.querySelector(".create-button-item button");
  let select = document.getElementById("select-template");
  let options = select.getElementsByTagName("option");

  // Checkboxes
  const requiredFill = document.getElementById("required-fill");
  const requiredFillHelpText = document.getElementById(
    "required-fill-help-text"
  );
  // Checkboxes

  // Element to view or hide
  const span = document.querySelector(".group-form > span");
  const textHelp = document.getElementById("help_info");
  // Element to view or hide

  function createLi() {
    let li = document.createElement("li");
    let input = document.createElement("input");

    ol.forEach((list) => {
      list.appendChild(li);
      li.appendChild(input);
      input.classList.add("input_reset");
      input.setAttribute("placeholder", "Введіть пункт");
    });
  }

  function selectTemplate() {
    let inputs = document.querySelectorAll(".input_reset");
    let option = document.createElement("option");

    inputs.forEach((input) => {
      input.addEventListener("input", () => {
        select.appendChild(option);
        option.text = input.value;
      });
    });
  }

  // Check if checkbox or radio is checked
  function checkboxOrRadioIsChecked() {
    // Get the checked checkbox state and the help text checkbox state
    const isChecked = requiredFill.checked;
    const isCheckedHelpText = requiredFillHelpText.checked;

    // Check if either checkbox is checked and show the element accordingly
    if (isChecked) {
      span.style.display = "block";
    } else {
      span.style.display = "none";
    }

    // Check if help text is visible and change its visibility accordingly
    if (isCheckedHelpText) {
      textHelp.style.display = "block";
    } else {
      textHelp.style.display = "none";
    }
  }

  btnCreateLi.addEventListener("click", createLi);
  btnCreateLi.addEventListener("click", selectTemplate);
  requiredFill.addEventListener("change", checkboxOrRadioIsChecked);
  requiredFillHelpText.addEventListener("change", checkboxOrRadioIsChecked);
});
