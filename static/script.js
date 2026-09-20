const form = document.getElementById("passwordForm");

const passwordInput = document.getElementById("password");

const togglePassword =
    document.getElementById("togglePassword");

const result =
    document.getElementById("result");

const scoreElement =
    document.getElementById("score");

const strengthElement =
    document.getElementById("strength");

const strengthFill =
    document.getElementById("strengthFill");

const checksContainer =
    document.getElementById("checks");

const warningsContainer =
    document.getElementById("warnings");

const recommendationsContainer =
    document.getElementById("recommendations");


// SHOW / HIDE PASSWORD

togglePassword.addEventListener("click", () => {

    if (passwordInput.type === "password") {

        passwordInput.type = "text";

        togglePassword.textContent = "Hide";

    } else {

        passwordInput.type = "password";

        togglePassword.textContent = "Show";

    }

});


// ANALYZE PASSWORD

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const password = passwordInput.value;

    if (!password) {

        result.classList.add("hidden");

        alert("Please enter a password.");

        return;
    }


    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                password: password
            })

        });


        const data = await response.json();


        if (!response.ok) {

            alert(data.error || "Something went wrong.");

            return;
        }


        displayResults(data);


    } catch (error) {

        alert(
            "Unable to connect to the application."
        );

    }

});


// DISPLAY RESULTS

function displayResults(data) {

    result.classList.remove("hidden");


    // SCORE

    scoreElement.textContent =
        `${data.score}/10`;


    // STRENGTH

    strengthElement.textContent =
        data.strength;


    // STRENGTH BAR

    strengthFill.style.width =
        `${data.score * 10}%`;


    // CHECKS

    checksContainer.innerHTML = "";


    const checkNames = {

        length: "At least 12 characters",

        uppercase: "Uppercase letters",

        lowercase: "Lowercase letters",

        number: "Numbers",

        special: "Special characters",

        no_common_password: "Not a common password",

        no_common_word: "No common words",

        no_sequence: "No predictable sequence",

        no_repeated_characters: "No repeated characters"

    };


    for (const key in data.checks) {

        const check = document.createElement("div");

        check.classList.add("check");


        if (data.checks[key]) {

            check.classList.add("pass");

            check.textContent =
                "✓ " + checkNames[key];

        } else {

            check.classList.add("fail");

            check.textContent =
                "✗ " + checkNames[key];

        }


        checksContainer.appendChild(check);

    }


    // WARNINGS

    warningsContainer.innerHTML = "";


    if (data.warnings.length === 0) {

        const item = document.createElement("li");

        item.textContent =
            "No major warnings detected.";

        warningsContainer.appendChild(item);

    } else {

        data.warnings.forEach(warning => {

            const item = document.createElement("li");

            item.textContent = warning;

            warningsContainer.appendChild(item);

        });

    }


    // RECOMMENDATIONS

    recommendationsContainer.innerHTML = "";


    data.recommendations.forEach(recommendation => {

        const item = document.createElement("li");

        item.textContent = recommendation;

        recommendationsContainer.appendChild(item);

    });

}