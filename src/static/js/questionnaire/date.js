// Checkboxes
const requiredFill = document.getElementById("required-fill");
const requiredFillHelpText = document.getElementById("required-fill-help-text");
// Checkboxes

// Element to view or hide
const span = document.querySelector(".group-form > span");
const textHelp = document.getElementById("help_info");
// Element to view or hide

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

// Add event listener to checkbox or radio buttons
requiredFill.addEventListener("change", checkboxOrRadioIsChecked);
requiredFillHelpText.addEventListener("change", checkboxOrRadioIsChecked);
