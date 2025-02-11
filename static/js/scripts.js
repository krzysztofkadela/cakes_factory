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
  const addToCartForms = document.querySelectorAll(".add-to-cart-form");

  addToCartForms.forEach((form) => {
      form.addEventListener("submit", function (event) {
          event.preventDefault();  // Prevent full page reload

          const formData = new FormData(this);
          const actionUrl = this.getAttribute("action");

          fetch(actionUrl, {
              method: "POST",
              body: formData,
              headers: {
                  "X-Requested-With": "XMLHttpRequest",
              },
          })
          .then(response => response.json())
          .then(data => {
              if (data.cart_items !== undefined) {
                  // Update cart count in the navbar
                  document.getElementById("cart-count").innerText = data.cart_items;
                  document.getElementById("cart-total").innerText = `€${data.cart_total_price.toFixed(2)}`;

                  // Show success message
                  const successMessage = document.createElement("div");
                  successMessage.classList.add("alert", "alert-success", "mt-2");
                  successMessage.innerHTML = "Item added to cart!";
                  document.body.appendChild(successMessage);

                  setTimeout(() => successMessage.remove(), 3000); // Auto-remove after 3 sec
              } else {
                  window.location.href = actionUrl;  // Redirect to cart page if JSON fails
              }
          })
          .catch(error => console.error("Error adding to cart:", error));
      });
  });
});