// =========================
// SHOW AND HIDE PASSWORD
// =========================

let passwordButtons =
    document.querySelectorAll(".show-password");


passwordButtons.forEach(function(button) {

    button.addEventListener("click", function() {

        let input =
            document.getElementById(
                button.dataset.target
            );


        if (input.type == "password") {

            input.type = "text";

            button.innerText = "Hide";

        }
        else {

            input.type = "password";

            button.innerText = "Show";

        }

    });

});


// =========================
// CHECK PASSWORDS
// =========================

let registerForm =
    document.getElementById("register-form");


if (registerForm) {

    registerForm.addEventListener(
        "submit",
        function(event) {


            let password =
                document.getElementById(
                    "password"
                ).value;


            let confirmPassword =
                document.getElementById(
                    "confirm_password"
                ).value;


            let error =
                document.getElementById(
                    "confirm-error"
                );


            if (password != confirmPassword) {

                event.preventDefault();

                error.hidden = false;

            }
            else {

                error.hidden = true;

            }

        }
    );

}