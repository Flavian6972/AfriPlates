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

// Login form handler
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = loginForm.querySelector('input[type="email"]').value;
  const password = loginForm.querySelector('input[type="password"]').value;

  try {
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: email,
        password: password
      })
    });

    const data = await response.json();

    if (response.ok) {
      alert(`Welcome back, ${data.username}!`);
      window.location.href = "/";
    } else {
      if (data.action === "signup") {
        alert(`${data.error}. Please sign up first.`);
        // Auto-switch to signup form
        loginForm.classList.add("hidden");
        signupForm.classList.remove("hidden");
        // Pre-fill email
        signupForm.querySelector('input[type="email"]').value = email;
      } else {
        alert(data.error);
      }
    }
  } catch (error) {
    alert('Login failed. Please try again.');
  }
});

// Signup form handler
signupForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = signupForm.querySelector('input[type="text"]').value;
  const email = signupForm.querySelector('input[type="email"]').value;
  const password = signupForm.querySelector('input[type="password"]').value;

  try {
    const response = await fetch('/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: email,
        password: password
      })
    });

    const data = await response.json();

    if (response.ok) {
      alert('Account created successfully! Please log in.');
      // Switch to login form and pre-fill email
      signupForm.classList.add("hidden");
      loginForm.classList.remove("hidden");
      loginForm.querySelector('input[type="email"]').value = email;
    } else {
      alert(data.error);
    }
  } catch (error) {
    alert('Signup failed. Please try again.');
  }
});