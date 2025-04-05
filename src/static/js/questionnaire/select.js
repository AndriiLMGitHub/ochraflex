document.addEventListener("DOMContentLoaded", () => {
  let ol = document.querySelectorAll(".create-items ol");
  const btnCreateLi = document.querySelector(".create-button-item button");
  let select = document.getElementById("select-template");
  let options = select.getElementsByTagName("option");
  let closeBtn = document.querySelector(".close-icon");

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
    let wrap = document.createElement("div");
    let div1 = document.createElement("div");
    let div2 = document.createElement("div");
    let input = document.createElement("input");

    wrap.classList.add("d-flex","justify-content-between", "align-items-center")
    div2.classList.add("close-icon")

    ol.forEach((list) => {
      list.appendChild(li);
      li.appendChild(wrap);
      wrap.appendChild(div1);
      wrap.appendChild(div2);
      div1.classList.add("w-100")
      div1.appendChild(input);
      input.classList.add("input_reset", "w-100");
      input.setAttribute("placeholder", "Введіть пункт");
    });

    // Отримуємо всі елементи з класом close-btn
    const closeButtons = document.querySelectorAll('.close-icon');

    closeButtons.forEach(button => {
      button.addEventListener('click', function() {
        // Видаляємо батьківський елемент (li)
        this.parentElement.parentElement.remove()
      });
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

  // Отримуємо всі елементи з класом close-btn
  const closeButtons = document.querySelectorAll('.close-icon');

  closeButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Видаляємо батьківський елемент (li)
      this.parentElement.parentElement.remove()
    });
  });

  btnCreateLi.addEventListener("click", createLi);
  btnCreateLi.addEventListener("click", selectTemplate);
  requiredFill.addEventListener("change", checkboxOrRadioIsChecked);
  requiredFillHelpText.addEventListener("change", checkboxOrRadioIsChecked);
});
