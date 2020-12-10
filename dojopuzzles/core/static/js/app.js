// Select the button
const btn = document.querySelector(".btn-toggle");
// Select the stylesheet <link>
const theme = document.querySelector("#theme-link");

// Listen for a click on the button
btn.addEventListener("click", function() {
  // If the current URL contains "ligh-theme.css"
  if (theme.getAttribute("href") == theme.getAttribute("data-light")) {
    // ... then switch it to "dark-theme.css"
    theme.href = theme.getAttribute("data-dark");
  // Otherwise...
  } else {
    // ... switch it to "light-theme.css"
    theme.href = theme.getAttribute("data-light");
  }
});

const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

if (prefersDarkScheme.matches) {
  theme.href = theme.getAttribute("data-dark");
} else {
  theme.href = theme.getAttribute("data-light");
}