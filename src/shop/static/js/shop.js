/**
 * Scripts for **Shop** project.
 *
 * @file   This files contains JavaScript routines used by various pages in the **Shop** project.
 * @author Thomas Gwasira
 * @since  13.09.2021
 */

/**
 * Returns csrftoken value.
 *
 * Source code: https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
 * Did not use external JavaScript Cookie library because it required
 * npm installation.
 *
 * @param   {string}    name:   Name of cookie
 * @return  {string}        :   CSRF token value from cookie
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
