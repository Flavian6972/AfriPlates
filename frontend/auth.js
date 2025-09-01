const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");
const showSignup = document.getElementById("show-signup");
const showLogin = document.getElementById("show-login");

showSignup.addEventListener("click", (e) => {
  e.preventDefault();
  loginForm.classList.add("hidden");
  signupForm.classList.remove("hidden");
});

showLogin.addEventListener("click", (e) => {
  e.preventDefault();
  signupForm.classList.add("hidden");
  loginForm.classList.remove("hidden");
});

// Example submit handler
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("Login successful (demo)");
  window.location.href = "homePage.html"; // redirect to homepage
});

signupForm.addEventListener("submit", (e) => {
  e.preventDefault();
  alert("Signup successful (demo)");
  window.location.href = "homePage.html";
});