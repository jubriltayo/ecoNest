// Add review without page reload
$("#commentForm").submit(function (e) {
  e.preventDefault();

  $.ajax({
    data: $(this).serialize(),

    method: $(this).attr("method"),
    url: $(this).attr("action"),

    dataType: "json",

    success: function (res) {
      console.log("review submitted");

      if (res.bool == true) {
        $("#review-res").html("Review added succesfully");
        $(".hide-comment-form").hide();
        $(".add-review").hide();

        let _html = `
                    <div class="single-comment justify-content-between d-flex mb-30">
                        <div class="user justify-content-between d-flex">
                            <div class="thumb text-center">
                                <img src="data:image/png;base64,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" alt="" />
                                <br>
                                <a href="#" class="font-heading text-brand">${
                                  res.context.user
                                }</a>
                            </div>
                            <div class="desc">
                                <div class="d-flex justify-content-between mb-10">
                                    <div class="d-flex align-items-center">
                                        <span class="font-xs text-muted">${new Date().toLocaleDateString(
                                          "en-GB",
                                          {
                                            day: "numeric",
                                            month: "short",
                                            year: "numeric",
                                          }
                                        )}</span>
                                    </div>
                                    <div id="rating-${res.context.id}">
                                        // stars will be here
                                    </div>
                                </div>
                                <p class="mb-10">${res.context.review}</p>
                            </div>
                        </div>
                    </div>
                `;

        $(".comment-list").prepend(_html);

        // Generate and append stars based on the rating
        let rating = parseInt(res.context.rating, 5);
        // console.log(`Rating value: ${rating}`);

        let stars = Array(rating)
          .fill('<i class="fas fa-star text-warning"></i>')
          .join("");
        document.getElementById(`rating-${res.context.id}`).innerHTML = stars;
      }
    },
  });
});

$(document).ready(function () {
  // Filter automatically by chwckbox without page reload
  $(".filter-checkbox, #price-filter-btn").on("click", function () {
    // console.log("Checkbox clicked")

    let filter_object = {};

    let min_price = $("#max_price").attr("min");
    let max_price = $("#max_price").val();

    filter_object.min_price = min_price;
    filter_object.max_price = max_price;

    $(".filter-checkbox").each(function () {
      let filter_value = $(this).val();
      let filter_key = $(this).data("filter"); //vendor or category

      // console.log("filter value is: ", filter_value)
      // console.log("filter key is: ", filter_key)

      filter_object[filter_key] = Array.from(
        document.querySelectorAll(`input[data-filter=${filter_key}]:checked`)
      ).map(function (element) {
        return element.value;
      });
    });
    console.log("filter object is : ", filter_object);

    $.ajax({
      url: "/filter-products",
      method: "GET",
      data: filter_object,
      dataType: "json",
      beforeSend: function () {
        console.log("Trying to filter data...");
      },
      success: function (response) {
        console.log("Data filtered successfully", response);
        $("#filtered-product").html(response.data);
      },
    });
  });

  // Price range limits - alert if exceeded
  $("#max_price").on("blur", function () {
    let min_price = $(this).attr("min");
    let max_price = $(this).attr("max");
    let current_price = $(this).val();

    // console.log("Current Price is:", current_price)
    // console.log("Max Price is:", max_price)
    // console.log("Min Price is:", min_price)

    if (
      current_price < parseInt(min_price) ||
      current_price > parseInt(max_price)
    ) {
      // console.log("Price error occured")

      minPrice = Math.round(min_price * 100) / 100;
      maxPrice = Math.round(max_price * 100) / 100;

      // console.log("Max Price is: ", min_price)
      // console.log("Max Price is: ", max_price)

      alert("Price must be between $" + min_price + " and $" + max_price);
      $(this).val(min_price);
      $("#range").val(min_price);
      $(this).focus();

      return false;
    }
  });

  // Add to cart
  $(".add-to-cart-btn").on("click", function () {
    let this_val = $(this);
    let index = this_val.attr("data-index");

    let quantity = $(".product-quantity-" + index).val();
    let product_title = $(".product-title-" + index).val();
    let product_id = $(".product-id-" + index).val();
    let product_price = $(".current-product-price-" + index).text();
    let product_pid = $(".product-pid-" + index).val();
    let product_image = $(".product-image-" + index).val();

    console.log("Quantity: ", quantity);
    console.log("Title: ", product_title);
    console.log("Price: ", product_price);
    console.log("ID: ", product_id);
    console.log("PID: ", product_pid);
    console.log("Image: ", product_image);
    console.log("Index: ", index);
    console.log("Current Element: ", this_val);

    $.ajax({
      url: "/add-to-cart",
      data: {
        id: product_id,
        pid: product_pid,
        image: product_image,
        qty: quantity,
        title: product_title,
        price: product_price,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Adding product to cart");
      },
      success: function (res) {
        this_val.html("✔");
        console.log("Added product to cart");
        $(".cart-items-count").text(res.totalCartItems);
      },
    });
  });

  // Delete from cart
  $(document).on("click", ".delete-product", function () {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);

    console.log("Product ID: ", product_id);
    console.log("Current Element: ", this_val);

    $.ajax({
      url: "/delete-from-cart",
      data: { id: product_id },
      dataType: "json",
      beforeSend: function () {
        console.log("Deleting product from cart");
        this_val.hide();
      },
      success: function (res) {
        console.log("Product deleted from cart");
        this_val.show();
        $(".cart-items-count").text(res.totalCartItems);
        $("#cart-list").html(res.data);
      },
    });
  });

  // Update cart
  $(document).on("click", ".update-product", function () {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);
    let product_quantity = $(".product-qty-" + product_id).val();
    console.log(product_quantity);

    console.log("Product ID: ", product_id);
    console.log("Current Element: ", this_val);

    $.ajax({
      url: "/update-cart",
      data: {
        id: product_id,
        qty: product_quantity,
      },
      dataType: "json",
      beforeSend: function () {
        this_val.hide();
      },
      success: function (res) {
        location.reload();
        this_val.show();
        $(".cart-items-count").text(res.totalCartItems);
        $("#cart-list").html(res.data);
      },
    });
  });

  // Make Default Address
  $(document).on("click", ".make-default-address", function () {
    let id = $(this).attr("data-address-id");
    let this_val = $(this);

    console.log("ID is: ", id);
    console.log("Element is: ", this_val);

    $.ajax({
      url: "/make-default-address",
      data: {
        id: id,
      },
      dataType: "json",
      success: function (res) {
        console.log("Address made default");
        if (res.boolean == true) {
          $(".check").hide();
          $(".action_btn").show();

          $(".check" + id).show();
          $(".button" + id).hide();
        }
      },
    });
  });

  // Add to Wishlist
  $(document).on("click", ".add-to-wishlist", function () {
    let product_id = $(this).attr("data-product-item");
    let this_val = $(this);

    console.log("Product ID is: ", product_id);
    console.log("Element is: ", this_val);

    $.ajax({
      url: "/add-to-wishlist",
      data: {
        id: product_id,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Adding to wishlist");
      },
      success: function (res) {
        this_val.html("✔");
        if (res.bool === true) {
          console.log("Added to wishlist");
        }
      },
    });
  });

  // Delete from wishlist
  $(document).on("click", ".delete-wishlist-product", function () {
    let wishlist_id = $(this).attr("data-wishlist-product");
    let this_val = $(this);

    console.log("Wishlist id", wishlist_id);
    console.log("Element", this_val);

    $.ajax({
      url: "/delete-from-wishlist",
      data: {
        id: wishlist_id,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Deleting from wishlist");
      },
      success: function (res) {
        $("#wishlist-list").html(res.data);
      },
    });
  });

  // Contact
  $(document).on("submit", "#contact-form-ajax", function (e) {
    e.preventDefault();
    console.log("Submitted");

    let full_name = $("#full_name").val();
    let email = $("#email").val();
    let phone = $("#phone").val();
    let subject = $("#subject").val();
    let message = $("#message").val();

    console.log("full name: ", full_name);
    console.log("email: ", email);
    console.log("phone: ", phone);
    console.log("subject: ", subject);
    console.log("message: ", message);

    $.ajax({
      url: "/ajax-contact-form",
      data: {
        full_name: full_name,
        email: email,
        phone: phone,
        subject: subject,
        message: message,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Sending data to server")
      },
      success: function (res) {
        console.log("data sent to server")
        console.log(res.data)
        $(".contact-p").hide()
        $("#contact-form-ajax").hide()
        $("#message-response").html("Message sent successfully")
      }
    });
  });
});

// REFERENCE - Add to cart
// $("#add-to-cart-btn").on("click", function() {
//   let quantity = $("#product-quantity").val();
//   let product_title = $(".product-title").val();
//   let product_id = $(".product-id").val();
//   let product_price = $(".current-product-price").text();
//   let this_val = $(this)

//   console.log("Quantity: ", quantity)
//   console.log("Title: ", product_title)
//   console.log("Price: ", product_price)
//   console.log("ID: ", product_id)
//   console.log("Current Element: ", this_val)

//   $.ajax({
//     url: '/add-to-cart',
//     data: {
//       'id': product_id,
//       'qty': quantity,
//       'title': product_title,
//       'price': product_price
//     },
//     dataType: 'json',
//     beforeSend: function() {
//       console.log("Adding product to cart")
//     },
//     success: function(res) {
//       this_val.html('Item added to cart')
//       console.log("Added product to cart")
//       $(".cart-items-count").text(res.totalCartItems)
//     }
//   })
// })
