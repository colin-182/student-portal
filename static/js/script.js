document.addEventListener("DOMContentLoaded", function () {

    /*
     * Project Date Validation
     *
     * Prevents the user from selecting an end date
     * that occurs before the project start date.
     */

    const startDate = document.getElementById("id_start_date");
    const endDate = document.getElementById("id_end_date");

    if (startDate && endDate) {

        function validateDates() {

            const existingError =
                document.getElementById("project-date-error");

            if (existingError) {
                existingError.remove();
            }

            endDate.classList.remove("is-invalid");

            if (
                startDate.value &&
                endDate.value &&
                endDate.value < startDate.value
            ) {

                const error = document.createElement("div");

                error.id = "project-date-error";
                error.className = "text-danger small mt-1";
                error.textContent =
                    "End date cannot be before the start date.";

                endDate.classList.add("is-invalid");

                endDate.parentNode.appendChild(error);
            }
        }

        startDate.addEventListener(
            "change",
            validateDates
        );

        endDate.addEventListener(
            "change",
            validateDates
        );
    }


    /*
     * Bootstrap Notification Auto-Dismiss
     *
     * Automatically closes dismissible Bootstrap alerts
     * after five seconds.
     */

    const alerts = document.querySelectorAll(
        ".alert.alert-dismissible"
    );

    alerts.forEach(function (alert) {

        setTimeout(function () {

            const bootstrapAlert =
                bootstrap.Alert.getOrCreateInstance(alert);

            bootstrapAlert.close();

        }, 5000);

    });

});