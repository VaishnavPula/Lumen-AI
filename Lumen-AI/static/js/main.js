// Light and dark mode


// Get all theme buttons

let buttons = document.querySelectorAll(".theme-toggle");


// Get saved theme

let theme = localStorage.getItem("theme");


// If saved theme is dark,
// add dark-mode to the body

if (theme == "dark") {

    document.body.classList.add("dark-mode");

}


// Set the correct button symbol

buttons.forEach(function(button) {

    if (document.body.classList.contains("dark-mode")) {

        button.innerText = "☀️";

    }
    else {

        button.innerText = "🌙";

    }

});


// Change theme when button is clicked

buttons.forEach(function(button) {

    button.addEventListener("click", function() {


        // Add or remove dark-mode

        document.body.classList.toggle("dark-mode");


        // Check current mode

        if (document.body.classList.contains("dark-mode")) {


            // Save dark mode

            localStorage.setItem("theme", "dark");


            // Change button

            button.innerText = "☀️";

        }
        else {


            // Save light mode

            localStorage.setItem("theme", "light");


            // Change button

            button.innerText = "🌙";

        }

    });

});