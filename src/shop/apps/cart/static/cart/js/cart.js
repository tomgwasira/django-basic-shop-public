/**
 * Scripts for cart page.
 *
 * @file   This files contains JavaScript routines for the cart summary page. 
 * @author Thomas Gwasira
 * @since  13.09.2021
 */

/**
 * Handles update of a cart item using AJAX.
 *
 * @listens event:onclick
 */
$(document).on('click', '.update-cart-item-btn', function (e) {
    e.preventDefault();

    var product_variant_id = $(this).data('product-variant-id')

    $.ajax({
        type: 'POST',
        url: $(this).data('url'),
        data: {
            product_variant_id: product_variant_id,
            item_quantity: $('#item-quantity-' + product_variant_id).val(),
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'update_cart_item'
        },
        success: function (json_response) {
            document.getElementById('cart-quantity').innerHTML = json_response.cart_quantity;

        },
        error: function (xhr, errmsg, err) { }
    });
})


/**
 * Handles deletion of a cart item using AJAX.
 *
 * @listens event:onclick
 */
$(document).on('click', '.delete-cart-item-btn', function (e) {
    e.preventDefault();

    var product_variant_id = $(this).data('product-variant-id')

    $.ajax({
        type: 'POST',
        url: $(this).data('url'),
        data: {
            product_variant_id: product_variant_id,
            csrfmiddlewaretoken: getCookie('csrftoken'),
            action: 'delete_cart_item'
        },
        success: function (json_response) {
            $('.cart-item-wrapper[data-index = "' + product_variant_id + '"]').remove();
            document.getElementById('cart-quantity').innerHTML = json_response.cart_quantity
            if (json_response.cart_quantity == 0) {
                document.getElementById('cart-empty-message-wrapper-1').style.display = "block";
                document.getElementById('cart-summary-wrapper').style.display = "none";
            }
        },
        error: function (xhr, errmsg, err) { }
    });
})

