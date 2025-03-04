let MAX = "max";
let MIN = "min";
let MAXLENGTH = "maxlength";
let MINLENGTH = "minlength";
let NUMBER = "number";
let TEXT = "text";
let FLAG;

// Checkboxes
const requiredFill = document.getElementById("required-fill");
const requiredFillHelpText = document.getElementById("required-fill-help-text");
// Checkboxes

// Radio buttons
const radioButtonNumber = document.getElementById("type-number");
const radioButtonAny = document.getElementById("type-text");
const radioButtonsCountSymbols = document.getElementsByName("max_symbols"); // Number of symbol in input field -> (array)
const radioButtonCustomValue = document.getElementById("static");
// Radio buttons

// Custom input
const inputCustomValue = document.getElementById("static_value");

// Element to view or hide
const span = document.querySelector(".group-form > span");
const textHelp = document.getElementById("help_info");
const templateInput = document.getElementById("template-text");
// Element to view or hide

function loopRadioButtonsIsChecked(arr, type, symbols = [60, 250, 500]) {
  for (let i = 0; i < arr.length - 1; i++) {
    if (arr[i].checked) {
      templateInput.setAttribute(type, symbols[i]);
    }
  }
}

function isAnyRadioChecked() {
  let blockMuted = document.querySelector(".block-muted");
  if (radioButtonNumber.checked || radioButtonAny.checked) {
    blockMuted.style.opacity = "1";
    blockMuted.style.pointerEvents = "all";
  }
}

function unCheckedAllCountRadioButtons() {
  radioButtonsCountSymbols.forEach((radioBtn) => {
    radioBtn.checked = false;
  });
}

function listenerAllRadioButtons(
  checkedValue,
  typeInputMax,
  typeInputMin = ""
) {
  // Add event listener to radio buttons and update input field's max attribute accordingly
  if (checkedValue) {
    radioButtonsCountSymbols.forEach((radioBtn) => {
      radioBtn.addEventListener("change", () => {
        templateInput.removeAttribute(typeInputMax);
        loopRadioButtonsIsChecked(radioButtonsCountSymbols, typeInputMax);
      });
    });

    radioButtonCustomValue.addEventListener("change", () => {
      inputCustomValue.addEventListener("input", () => {
        templateInput.removeAttribute(typeInputMin);
        templateInput.setAttribute(typeInputMax, inputCustomValue.value);
      });
    });
  } else {
    radioButtonsCountSymbols.forEach((radioBtn) => {
      radioBtn.addEventListener("change", () => {
        templateInput.removeAttribute(typeInputMax);
        loopRadioButtonsIsChecked(radioButtonsCountSymbols, typeInputMax);
      });
    });

    radioButtonCustomValue.addEventListener("change", () => {
      inputCustomValue.addEventListener("input", () => {
        templateInput.removeAttribute(typeInputMin);
        templateInput.setAttribute(typeInputMax, inputCustomValue.value);
      });
    });
  }
}

function setAllAttributes() {
  if (FLAG) {
    templateInput.type = NUMBER;

    templateInput.removeAttribute = MAXLENGTH;
    templateInput.removeAttribute = MINLENGTH;

    templateInput.setAttribute(MAX, 40);
    templateInput.setAttribute(MIN, 3);
  } else {
    templateInput.type = TEXT;

    templateInput.removeAttribute = MAX;
    templateInput.removeAttribute = MIN;

    templateInput.setAttribute(MAXLENGTH, 40);
    templateInput.setAttribute(MINLENGTH, 3);
  }
}

// Check if checkbox or radio is checked
function checkboxOrRadioIsChecked() {
  // Get the checked checkbox state and the help text checkbox state
  const isChecked = requiredFill.checked;
  const isCheckedHelpText = requiredFillHelpText.checked;
  const isCheckedRadioButtonNumber = radioButtonNumber.checked;
  const isCheckedRadioButtonAny = radioButtonAny.checked;

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

  // Check if both radio buttons are checked and show the element accordingly
  if (isCheckedRadioButtonNumber) {
    isAnyRadioChecked();
    unCheckedAllCountRadioButtons();
    FLAG = true;

    templateInput.type = "number";

    templateInput.removeAttribute("maxlength");
    templateInput.removeAttribute("minlength");

    templateInput.setAttribute("min", 3);
    templateInput.setAttribute("max", 40);

    // setAllAttributes();

    radioButtonsCountSymbols.forEach((radioBtn) => {
      radioBtn.addEventListener("change", () => {
        templateInput.removeAttribute("maxlength");
        loopRadioButtonsIsChecked(radioButtonsCountSymbols, "max");
      });
    });

    radioButtonCustomValue.addEventListener("change", () => {
      inputCustomValue.addEventListener("input", () => {
        templateInput.removeAttribute("maxlength");
        templateInput.setAttribute("max", inputCustomValue.value);
      });
    });
  } else if (isCheckedRadioButtonAny) {
    isAnyRadioChecked();
    unCheckedAllCountRadioButtons();
    FLAG = false;

    templateInput.type = "text";

    templateInput.removeAttribute("max");
    templateInput.removeAttribute("min");

    templateInput.setAttribute("minlength", 3);
    templateInput.setAttribute("maxlength", 40);
    // setAllAttributes();

    radioButtonsCountSymbols.forEach((radioBtn) => {
      radioBtn.addEventListener("change", () => {
        templateInput.removeAttribute("max");
        loopRadioButtonsIsChecked(radioButtonsCountSymbols, "maxlength");
      });
    });

    radioButtonCustomValue.addEventListener("change", () => {
      inputCustomValue.addEventListener("input", () => {
        templateInput.removeAttribute("max");
        templateInput.setAttribute("maxlength", inputCustomValue.value);
      });
    });
  }
}

// Add event listener to checkbox or radio buttons
requiredFill.addEventListener("change", checkboxOrRadioIsChecked);
requiredFillHelpText.addEventListener("change", checkboxOrRadioIsChecked);
radioButtonNumber.addEventListener("change", checkboxOrRadioIsChecked);
radioButtonAny.addEventListener("change", checkboxOrRadioIsChecked);
