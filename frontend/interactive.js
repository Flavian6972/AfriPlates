let selectedCountry = "";
let userName = "";

// Logout functionality
document.addEventListener('DOMContentLoaded', function () {
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async function (e) {
      e.preventDefault();
      try {
        const response = await fetch('/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (response.ok) {
          alert('You have been logged out successfully.');
          window.location.reload(); // Refresh to update the navigation
        }
      } catch (error) {
        alert('Logout failed. Please try again.');
      }
    });
  }
});

function login() {
  console.log('Continue button clicked')
  userName = document.getElementById("username").value;
  console.log(userName)
  if (userName.trim() === "") {
    alert("Please enter your name");
    return;
  }
  document.getElementById("login-section").classList.add("hidden");
  document.getElementById("country-section").classList.remove("hidden");
}

function selectCountry(country) {
  selectedCountry = country;
  document.getElementById("country-title").innerText = `Ingredients for ${country} recipes`;
  document.getElementById("country-section").classList.add("hidden");
  document.getElementById("ingredients-section").classList.remove("hidden");
}

async function getRecipes() {
  let ingredients = document.getElementById("ingredients").value;

  try {
    let res = await fetch("http://127.0.0.1:5000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients, country: selectedCountry })
    });

    let data = await res.json();
    let container = document.getElementById("results");
    container.innerHTML = "";

    if (res.ok) {
      let card = document.createElement("div");
      card.className = "recipe-card";
      card.innerText = data.recipes;
      container.appendChild(card);
    } else {
      let errorCard = document.createElement("div");
      errorCard.className = "recipe-card";
      errorCard.style.color = "red";
      errorCard.innerText = data.error;
      container.appendChild(errorCard);

      if (res.status === 401) {
        // Redirect to login if not authenticated
        setTimeout(() => {
          window.location.href = "/login";
        }, 2000);
      }
    }
  } catch (error) {
    let container = document.getElementById("results");
    container.innerHTML = `<div class="recipe-card" style="color: red;">Error: ${error.message}</div>`;
  }
}

// Function to load popular recipes
async function loadPopularRecipes() {
  try {
    const response = await fetch('/popular-recipes');
    const data = await response.json();

    if (response.ok) {
      const element = document.getElementById('popular-recipes');
      if (element) {
        if (typeof data.recipes === 'string') {
          element.innerHTML = `<a href="#" onclick="showRecipeModal('${data.recipes.replace(/'/g, "\\'")}')">View Popular Recipes</a>`;
        } else {
          element.innerHTML = `<a href="#" onclick="showRecipesModal(${JSON.stringify(data.recipes).replace(/"/g, '&quot;')})">View Popular Recipes</a>`;
        }
      }
    }
  } catch (error) {
    console.error('Error loading popular recipes:', error);
  }
}

// Function to load recipe stats
async function loadRecipeStats() {
  try {
    const response = await fetch('/recipe-stats');
    const data = await response.json();

    if (response.ok) {
      const element = document.getElementById('recipes-count');
      if (element) {
        element.textContent = `${data.weekly_recipes} this week`;
      }
    }
  } catch (error) {
    console.error('Error loading recipe stats:', error);
  }
}

// Function to load trending ingredients
async function loadTrendingIngredients() {
  try {
    const response = await fetch('/trending-ingredients');
    const data = await response.json();

    if (response.ok) {
      const element = document.getElementById('trending-ingredient');
      if (element) {
        if (typeof data.ingredients === 'string') {
          element.innerHTML = `<a href="#" onclick="showIngredientsModal('${data.ingredients.replace(/'/g, "\\'")}')">View Trending Ingredients</a>`;
        } else {
          element.innerHTML = `<a href="#" onclick="showIngredientsModal(${JSON.stringify(data.ingredients).replace(/"/g, '&quot;')})">View Trending Ingredients</a>`;
        }
      }
    }
  } catch (error) {
    console.error('Error loading trending ingredients:', error);
  }
}

// Function to show recipe modal
function showRecipeModal(content) {
  alert(`Popular Recipes:\n\n${content}`);
}

// Function to show recipes modal with buy option
function showRecipesModal(recipes) {
  let content = "Popular Recipes:\n\n";
  recipes.forEach((recipe, index) => {
    content += `${index + 1}. ${recipe.title}\n${recipe.content}\n`;
    if (recipe.is_premium) {
      content += `Price: $${recipe.price}\n`;
    }
    content += "\n";
  });

  const userChoice = confirm(content + "\nWould you like to purchase a premium recipe?");
  if (userChoice) {
    // Find first premium recipe
    const premiumRecipe = recipes.find(r => r.is_premium);
    if (premiumRecipe) {
      buyRecipe(premiumRecipe.id);
    } else {
      alert("No premium recipes available at the moment.");
    }
  }
}

// Function to show ingredients modal
function showIngredientsModal(ingredients) {
  alert(`Trending Ingredients:\n\n${ingredients}`);
}

// Function to buy recipe
async function buyRecipe(recipeId) {
  const paymentMethod = prompt("Choose payment method (mpesa/card/bank):", "mpesa");
  if (!paymentMethod) return;

  try {
    const response = await fetch('/buy-recipe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        recipe_id: recipeId,
        payment_method: paymentMethod
      })
    });

    const data = await response.json();

    if (response.ok) {
      alert(`Payment successful! Transaction ID: ${data.transaction_id}\n\nRecipe Content:\n${data.recipe_content}`);
    } else {
      alert(`Payment failed: ${data.error}`);
      if (response.status === 401) {
        window.location.href = "/login";
      }
    }
  } catch (error) {
    alert(`Payment error: ${error.message}`);
  }
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', function () {
  loadPopularRecipes();
  loadRecipeStats();
  loadTrendingIngredients();
});