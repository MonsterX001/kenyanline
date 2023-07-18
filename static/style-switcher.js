const styleSwitcherToggle = document.querySelector(".style-switcher-toggle");
const styleSwitcher = document.querySelector(".style-switcher");
const alternateStyles = document.querySelectorAll(".alternate-style");
const dayNight = document.querySelector(".day-night");

// Function to set the active style
function setActiveStyle(color) {
  alternateStyles.forEach((style) => {
    if (color === style.getAttribute("title")) {
      style.removeAttribute("disabled");
    } else {
      style.setAttribute("disabled", "true");
    }
  });
}

// Function to toggle the style switcher
function toggleStyleSwitcher() {
  styleSwitcher.classList.toggle("open");

  // Save the style switcher state to localStorage
  const isStyleSwitcherOpen = styleSwitcher.classList.contains("open");
  localStorage.setItem("isStyleSwitcherOpen", isStyleSwitcherOpen.toString());
}

// Function to toggle day/night mode
function toggleDayNightMode() {
  dayNight.querySelector("i").classList.toggle("fa-sun");
  dayNight.querySelector("i").classList.toggle("fa-moon");
  document.body.classList.toggle("dark");

  // Save the day/night mode to localStorage
  const isDarkMode = document.body.classList.contains("dark");
  localStorage.setItem("isDarkMode", isDarkMode.toString());
}

// Add event listeners
styleSwitcherToggle.addEventListener("click", toggleStyleSwitcher);
dayNight.addEventListener("click", toggleDayNightMode);

// Restore the style switcher state from localStorage
const isStyleSwitcherOpen = localStorage.getItem("isStyleSwitcherOpen");
if (isStyleSwitcherOpen && isStyleSwitcherOpen === "true") {
  styleSwitcher.classList.add("open");
}

// Restore the day/night mode from localStorage
const isDarkMode = localStorage.getItem("isDarkMode");
if (isDarkMode && isDarkMode === "true") {
  dayNight.querySelector("i").classList.add("fa-sun");
  document.body.classList.add("dark");
}

// Listen for scroll event and close the style switcher if open
window.addEventListener("scroll", () => {
  if (styleSwitcher.classList.contains("open")) {
    styleSwitcher.classList.remove("open");
  }
});

// Save the style switcher state to localStorage when it's toggled
styleSwitcherToggle.addEventListener("click", () => {
  const isStyleSwitcherOpen = styleSwitcher.classList.contains("open");
  localStorage.setItem("isStyleSwitcherOpen", isStyleSwitcherOpen.toString());
});





/*
const styleSwitcherToggle = document.querySelector(".style-switcher-toggle");
const styleSwitcher = document.querySelector(".style-switcher");
const alternateStyles = document.querySelectorAll(".alternate-style");
const dayNight = document.querySelector(".day-night");

// Function to set the active style
function setActiveStyle(color) {
  alternateStyles.forEach((style) => {
    if (color === style.getAttribute("title")) {
      style.removeAttribute("disabled");
    } else {
      style.setAttribute("disabled", "true");
    }
  });
}

// Function to toggle the style switcher
function toggleStyleSwitcher() {
  styleSwitcher.classList.toggle("open");

  // Save the style switcher state to localStorage
  const isStyleSwitcherOpen = styleSwitcher.classList.contains("open");
  localStorage.setItem("isStyleSwitcherOpen", isStyleSwitcherOpen);
}

// Function to toggle day/night mode
function toggleDayNightMode() {
  dayNight.querySelector("i").classList.toggle("fa-sun");
  dayNight.querySelector("i").classList.toggle("fa-moon");
  document.body.classList.toggle("dark");

  // Save the day/night mode to localStorage
  const isDarkMode = document.body.classList.contains("dark");
  localStorage.setItem("isDarkMode", isDarkMode);
}

// Add event listeners
styleSwitcherToggle.addEventListener("click", toggleStyleSwitcher);
dayNight.addEventListener("click", toggleDayNightMode);

// Restore the style switcher state from localStorage
const isStyleSwitcherOpen = localStorage.getItem("isStyleSwitcherOpen");
if (isStyleSwitcherOpen === "true") {
  styleSwitcher.classList.add("open");
}

// Restore the day/night mode from localStorage
const isDarkMode = localStorage.getItem("isDarkMode");
if (isDarkMode === "true") {
  dayNight.querySelector("i").classList.add("fa-sun");
  document.body.classList.add("dark");
}

// Listen for scroll event and close the style switcher if open
window.addEventListener("scroll", () => {
  if (styleSwitcher.classList.contains("open")) {
    styleSwitcher.classList.remove("open");
  }
});

// Save the style switcher state to localStorage when it's toggled
styleSwitcherToggle.addEventListener("click", () => {
  const isStyleSwitcherOpen = styleSwitcher.classList.contains("open");
  localStorage.setItem("isStyleSwitcherOpen", isStyleSwitcherOpen);
});

/*const styleSwitcherToggle = document.querySelector(".style-switcher-toggle");
const styleSwitcher = document.querySelector(".style-switcher");
const alternateStyles = document.querySelectorAll(".alternate-style");
const dayNight = document.querySelector(".day-night");

// Function to set the active style
function setActiveStyle(color) {
  alternateStyles.forEach((style) => {
    if (color === style.getAttribute("title")) {
      style.removeAttribute("disabled");
    } else {
      style.setAttribute("disabled", "true");
    }
  });
}

// Function to toggle the style switcher
function toggleStyleSwitcher() {
  styleSwitcher.classList.toggle("open");
}

// Function to toggle day/night mode
function toggleDayNightMode() {
  dayNight.querySelector("i").classList.toggle("fa-sun");
  dayNight.querySelector("i").classList.toggle("fa-moon");
  document.body.classList.toggle("dark");

  // Save the day/night mode to localStorage
  const isDarkMode = document.body.classList.contains("dark");
  localStorage.setItem("isDarkMode", isDarkMode);
}

// Add event listeners
styleSwitcherToggle.addEventListener("click", toggleStyleSwitcher);
dayNight.addEventListener("click", toggleDayNightMode);

// Restore the style switcher state from localStorage
const isStyleSwitcherOpen = localStorage.getItem("isStyleSwitcherOpen");
if (isStyleSwitcherOpen === "true") {
  styleSwitcher.classList.add("open");
}

// Restore the day/night mode from localStorage
const isDarkMode = localStorage.getItem("isDarkMode");
if (isDarkMode === "true") {
  dayNight.querySelector("i").classList.add("fa-sun");
  document.body.classList.add("dark");
}

// Listen for scroll event and close the style switcher if open
window.addEventListener("scroll", () => {
  if (styleSwitcher.classList.contains("open")) {
    styleSwitcher.classList.remove("open");
  }
});

// Save the style switcher state to localStorage when it's toggled
styleSwitcherToggle.addEventListener("click", () => {
  const isStyleSwitcherOpen = styleSwitcher.classList.contains("open");
  localStorage.setItem("isStyleSwitcherOpen", isStyleSwitcherOpen);
});





/*const styleSwitcherToggle = document.querySelector(".style-switcher-toggle");
styleSwitcherToggle.addEventListener("click", () => {
    document.querySelector(".style-switcher").classList.toggle("open");
})
window.addEventListener("scroll", () =>{
    if(document.querySelector(".style-switcher").classList.contains("open"))
    {
        document.querySelector(".style-switcher").classList.remove('open');
    }
})

const alternateStyles = document.querySelectorAll(".alternate-style");
function setActiveStyle(color)
{
    alternateStyles.forEach((style) => {
        if(color === style.getAttribute("title")){
            style.removeAttribute("disabled");
        }
        else{
            style.setAttribute("disabled", "True")
        }
    })
}

const dayNight = document.querySelector(".day-night");
dayNight.addEventListener("click", () => {
    dayNight.querySelector("i").classList.toggle("fa-sun");
    dayNight.querySelector("i").classList.toggle("fa-moon");
    document.body.classList.toggle("dark");
})
window.addEventListener("load", () => {
    if(document.body.classList.contains("dark")){
        dayNight.querySelector("i").classList.add("fa-sun");
    }
    else{
        dayNight.querySelector("i").classList.add("fa-moon");
    }

})*/


