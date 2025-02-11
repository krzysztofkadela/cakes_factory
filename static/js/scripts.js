/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/

// close messages after 5s automatic...


document.addEventListener("DOMContentLoaded", function () {
  setTimeout(function () {
      let alerts = document.querySelectorAll(".alert");
      alerts.forEach(alert => {
          let bsAlert = new bootstrap.Alert(alert);
          bsAlert.close();
      });
  }, 5000); // Auto-dismiss after 5 seconds
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".add-to-cart-btn").forEach((btn) => {
      btn.addEventListener("click", function (event) {
          event.preventDefault();

          let productId = this.getAttribute("data-product-id");
          let sizeId = document.querySelector("select[name='size']").value || "";
          let quantity = document.querySelector("input[name='quantity']").value || 1;
          let csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

          fetch(`/orders/cart/add/${productId}/`, {
              method: "POST",
              headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                  "X-CSRFToken": csrfToken,
              },
              body: `quantity=${quantity}&size=${sizeId}`,
          })
          .then((response) => response.json())
          .then((data) => {
              document.querySelector("#cart-count").textContent = data.cart_items;
              document.querySelector("#cart-total").textContent = `€${data.cart_total_price.toFixed(2)}`;
          })
          .catch((error) => console.error("Error:", error));
      });
  });
});