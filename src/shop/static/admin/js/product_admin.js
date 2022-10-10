/**
 * Scripts for Product admin page.
 *
 * @file   This files contains JavaScript routines for the admin page of the Product model. 
 * @author Thomas Gwasira
 * @since  13.09.2021
 */

var prev_section = document.getElementById('general');

// document
// .getElementById('general-btn')
// .addEventListener('click', (event) => {
// event.preventDefault();
// });

// document
// .getElementById('product-variants-btn')
// .addEventListener('click', (event) => {
// event.preventDefault();
// });


/**
 * Displays section on Product admin page corresponding to clicked button and hides other sections not relevant.
 *
 * @listens event:onclick
 */
function displayProductAdminPageSection(id) {
    // but.disabled=true

    prev_section.style.display = "none";

    var current_section = document.getElementById(id);
    current_section.style.display = "block";

    prev_section = current_section
}