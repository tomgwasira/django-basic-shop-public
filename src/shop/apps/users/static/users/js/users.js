/**
 * Scripts for **Users** app pages.
 *
 * @file   This files contains JavaScript routines for the **Users** app pages.
 * @author Thomas Gwasira
 * @since  13.09.2021
 */

/**
 * Confirms and deactivates a customer account.
 *
 * This function handles uses an AJAX request to deactivate a customer
 * account.
 *
 * @listens event:onclick
 */
$(document).on("click", "#confirm-deactivate-customer-account-btn", function (e) {
   // AJAX Request
   $.ajax({
        type: "GET",
        url: $(this).data("url"),
        data: {
            csrfmiddlewaretoken: getCookie("csrftoken"),
        },
 
        // Successful request routine
        success: function (json_response) {
            // console.log("Hi")
            // Redirect to success_url given in JSON response
            window.location.href = json_response["next_url"]

        },
 
        error: function (xhr, errmsg, err) {
            console.log("Failed to deactivate customer account.");
        },
    });
});