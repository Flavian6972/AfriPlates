let selectedCountry = "";
    let userName = "";

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
      let res = await fetch("http://127.0.0.1:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients, country: selectedCountry })
      });
      let data = await res.json();

      let container = document.getElementById("results");
      container.innerHTML = "";

      let card = document.createElement("div");
      card.className = "recipe-card";
      card.innerText = data.recipes;
      container.appendChild(card);
    }