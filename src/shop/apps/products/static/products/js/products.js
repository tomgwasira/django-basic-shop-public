/**
 * Scripts for **Products** app pages.
 *
 * @file   This files contains JavaScript routines for the **Products** app pages.
 * @author Thomas Gwasira
 * @since  13.09.2021
 */

selected_options = {}; // stores information about OptionValues selected using buttons

/**
 * Filters ProductVariants based on OptionValue seclection
 * using AJAX.
 *
 * This function handles selection of an OptionValue by using
 * an AJAX request to query the database for ProductVariants
 * of the particular Product having all of the OptionValues
 * selected, and using the response from this request, updating
 * attributes of the `Add to Cart` button as well as enabling
 * OptionValues valid for selection given the current selection.
 *
 * @listens event:onclick
 */
$(document).on("click", ".option-value-btn", function (e) {
  var curr_option_item_pos = parseInt(
    $(this).parent().parent().data("option_item_pos")
  );

  // Add or update option type in dict of selected option types and values
  selected_options[$(this).parent().parent().data("option_type_name")] = {
    option_value_id: $(this).data("option_value_id"),
    option_value_name: $(this).data("option_value_name"),
    option_item_pos: curr_option_item_pos,
  };

  // Clear option types that appear after current option type
  for (var option_type in selected_options) {
    if (
      selected_options[option_type]["option_item_pos"] > curr_option_item_pos
    ) {
      delete selected_options[option_type];
    }
  }

  // AJAX Request
  $.ajax({
    type: "GET",
    url: $(this).data("url"), // URL for view to control ProductVariant filtering
    data: {
      // data passed through AJAX request
      product_id: $(this).data("product_id"),
      selected_options: JSON.stringify(selected_options),
      // csrfmiddlewaretoken: getCookie("csrftoken"),
      action: "option_value_selection",
    },

    // Successful request routine
    success: function (json_response) {
      // Disable all OptionValues a level below current OptionType
      var option_items = document.getElementsByClassName("option-item-wrapper");
      for (var i = 0; i < option_items.length; i++) {
        if (
          parseInt(option_items.item(i).dataset.option_item_pos) >
          curr_option_item_pos
        ) {
          var option_value_btns = option_items
            .item(i)
            .getElementsByClassName("option-value-btn");
          for (var j = 0; j < option_value_btns.length; j++) {
            option_value_btns.item(j).disabled = true;
          }
        }
      }

      // Enable available OptionValues a level below current OptionType
      for (var option_value_id in json_response[
        "available_option_values_data"
      ]) {
        var option_value_btn = document.getElementById(
          "option-value-btn-" + option_value_id
        );
        if (
          parseInt(
            option_value_btn.parentElement.parentElement.dataset.option_item_pos
          ) ==
          curr_option_item_pos + 1
        ) {
          option_value_btn.disabled = false;
        }
      }

      // Set item quantity input attributes
      var item_quantity = document.getElementById("item-quantity");
      var perceived_stock = parseInt(
        json_response["product_variants_data"][0]["perceived_stock"]
      );
      // Reduce item quantity input if greater than perceived stock of current ProductVariant
      if (parseInt(item_quantity.value) > perceived_stock) {
        item_quantity.value = perceived_stock;
      }
      // Set maximum allowable quantity to perceived stock of current ProductVariant
      item_quantity.max = perceived_stock;

      // Set Add to Cart button attributes
      document.getElementById("add-cart-item-btn").dataset.no_of_variants =
        json_response["product_variants_data"].length;
      document.getElementById("add-cart-item-btn").dataset.product_variant_id =
        json_response["product_variants_data"][0]["product_variant_id"];


      // Hide all previously displayed (by AJAX) images
      var product_images_with_option_values = document.getElementsByClassName("product-images-with-option-values-wrapper")
      for (var i = 0; i < product_images_with_option_values.length; i++) {
        product_images_with_option_values.item(i).style.display = "none"
      }
      
      // Display images corresponding to the OptionValue
      // TODO: Assumes there'll every option_type_name always has option_value_id not
      // a bad assumption considering the only way the option_type_name could have
      // been added was by clicking option_value_id, but is there a way to make
      // this more robust
      for (var option_type_name in selected_options) {
        document.getElementById(("product-images-wrapper-" + selected_options[option_type_name]["option_value_id"])).style.display = "block"
      }
    },

    error: function (xhr, errmsg, err) {},
  });
});

/**
 * Adds ProductVariant to 'cart' using AJAX.
 *
 * @listens event:onclick
 */
$(document).on("click", "#add-cart-item-btn", function (e) {
  var item_quantity_input = document.getElementById("item-quantity");
  var add_cart_item_btn = document.getElementById("add-cart-item-btn");

  if (parseInt(add_cart_item_btn.dataset.no_of_variants) == 1) {
    // AJAX request
    $.ajax({
      type: "POST",
      url: $(this).data("url"), // URL for view to control ProductVariant filtering
      data: {
        // data passed through AJAX request
        product_variant_id: add_cart_item_btn.dataset.product_variant_id,
        item_quantity: item_quantity_input.value,
        csrfmiddlewaretoken: getCookie("csrftoken"),
        action: "add_cart_item",
      },

      // Successful request routine
      success: function (json_response) {
        document.getElementById("cart-quantity").innerHTML =
          json_response.cart_quantity;

        // Reduce item quantity input if greater than new perceived stock
        var perceived_stock =
          item_quantity_input.max - item_quantity_input.value;
        if (item_quantity_input.value > perceived_stock) {
          item_quantity_input.value = perceived_stock;
        }

        // Set maximum allowable item quantity input
        item_quantity_input.max = perceived_stock;
      },
      error: function (xhr, errmsg, err) {console.log(errmsg)},
    });
  } else {
    console.log("Ensure all options are selected.");
  }
});
