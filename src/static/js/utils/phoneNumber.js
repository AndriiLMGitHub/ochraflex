window.addEventListener('DOMContentLoaded', () => {
      // Масив з мовами
  const languages = [
    { code: "cz", name: "Czech Republic", flag: "🇨🇿", phoneCode: "+420" },
    { code: "de", name: "Germany", flag: "🇩🇪", phoneCode: "+49" },
  ];

  // Функція ініціалізації форми
  function initializePhoneForm(form) {
    const languageDropdown = form.querySelector(".languageDropdown");
    const selectedLanguage = form.querySelector(".selectedLanguage");
    const phoneNumberInput = form.querySelector(".phoneNumberInput");

    // Ініціалізація за замовчуванням
    let currentLanguage = languages[0];
    updateLanguageDisplay(currentLanguage);
    setPhoneNumberMask(currentLanguage);

    // Функція оновлення мови
    function updateLanguageDisplay(language) {
      selectedLanguage.innerHTML = `${language.flag} ${language.name}`;
      languageDropdown.value = language.code;
    }

    // Функція оновлення маски для телефону
    function setPhoneNumberMask(language) {
      const phoneCode = language.phoneCode;
    
      // Зберігаємо тільки введені цифри без коду країни
      let userInput = phoneNumberInput.value.replace(/^\+\d+\s*/, "");
    
      // Оновлюємо значення з новим кодом країни
      phoneNumberInput.value = phoneCode + " " + userInput;
    
      phoneNumberInput.setAttribute("placeholder", `${phoneCode} XXX-XXX-XXX`);
    
      phoneNumberInput.addEventListener("input", (event) => {
        let cursorPosition = phoneNumberInput.selectionStart;
    
        // Забираємо все, що йде перед кодом країни
        if (!phoneNumberInput.value.startsWith(phoneCode)) {
          phoneNumberInput.value = phoneCode + " " + phoneNumberInput.value.replace(/^\+\d+\s*/, "");
        }
    
        // Запобігаємо введенню перед кодом країни
        if (cursorPosition < phoneCode.length + 1) {
          phoneNumberInput.setSelectionRange(phoneCode.length + 1, phoneCode.length + 1);
        }
      });
    }

    // Обробник зміни мови
    languageDropdown.addEventListener("change", (event) => {
      const selectedCode = event.target.value;
      currentLanguage = languages.find((lang) => lang.code === selectedCode);
      updateLanguageDisplay(currentLanguage);
      setPhoneNumberMask(currentLanguage);
    });

    // Генерація елементів dropdown
    function populateLanguageDropdown() {
      languages.forEach((language) => {
        const option = document.createElement("option");
        option.value = language.code;
        option.textContent = `${language.flag} ${language.name}`;
        languageDropdown.appendChild(option);
      });
    }

    // Виклик функції генерації dropdown
    populateLanguageDropdown();

    // Встановлення значення за замовчуванням
    languageDropdown.value = currentLanguage.code;
  }

  // Ініціалізація всіх форм на сторінці
  const phoneForms = document.querySelectorAll(".phoneForm");
  phoneForms.forEach((form) => initializePhoneForm(form));
})