// Checkboxes
const requiredFill = document.getElementById("required-fill");
// Checkboxes

// Element to view or hide
const span = document.querySelector(".group-form > span");
// Element to view or hide

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

// Add event listener to checkbox
requiredFill.addEventListener("change", checkboxOrRadioIsChecked);
