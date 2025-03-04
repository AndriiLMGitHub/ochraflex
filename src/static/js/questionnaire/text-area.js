// Checkboxes
const requiredFill = document.getElementById("required-fill");
const requiredFillHelpText = document.getElementById("required-fill-help-text");
// Checkboxes

// Radio buttons
const radioButtonText = document.getElementById("type-text");
const radioButtonsCountSymbols = document.getElementsByName("max_symbols"); // Number of symbol in input field -> (array)
// Radio buttons

// Element to view or hide
const span = document.querySelector(".group-form > span");
const textHelp = document.getElementById("help_info");
const templateInput = document.getElementById("template-text");
// Element to view or hide

function loopRadioButtonsIsChecked(arr, type, symbols = [60, 250, 500, 1000]) {
  for (let i = 0; i < arr.length; i++) {
    if (arr[i].checked) {
      templateInput.setAttribute(type, symbols[i]);
    }
  }
}

function setValue() {
  // Set the input field's value and max attribute accordingly
  loopRadioButtonsIsChecked(radioButtonsCountSymbols, "maxlength");
}

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

function isRadioChecked() {
  let blockMuted = document.querySelector(".block-muted");
  if (radioButtonText.checked) {
    blockMuted.style.opacity = "1";
    blockMuted.style.pointerEvents = "all";
  }
}

// Add event listener to checkbox or radio buttons
requiredFill.addEventListener("change", checkboxOrRadioIsChecked);
requiredFillHelpText.addEventListener("change", checkboxOrRadioIsChecked);
radioButtonText.addEventListener("change", isRadioChecked);
radioButtonsCountSymbols.forEach((radioBtn) => {
  radioBtn.addEventListener("change", setValue);
});
