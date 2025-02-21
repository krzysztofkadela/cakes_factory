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

// Dynamic Price Update

document.addEventListener("DOMContentLoaded", function () {
    const sizeDropdown = document.getElementById("size");
    const priceDisplay = document.getElementById("product-price");
    const basePrice = parseFloat(priceDisplay.dataset.basePrice); // Get base price from data attribute

    const sizeAdjustments = {
        "Small": 0,
        "Large": 20,
        "X-large": 40
    };

    function updatePrice() {
        const selectedSize = sizeDropdown.options[sizeDropdown.selectedIndex].text.trim();
        const extraCost = sizeAdjustments[selectedSize] || 0;
        const newPrice = basePrice + extraCost;

        if (!isNaN(newPrice)) {
            priceDisplay.innerText = `€${newPrice.toFixed(2)}`;
        }
    }

    if (sizeDropdown) {
        sizeDropdown.addEventListener("change", updatePrice);
    }
});

//check out validation.

document.addEventListener("DOMContentLoaded", function () {
    const payButton = document.getElementById("pay-with-stripe");
    const checkoutForm = document.getElementById("checkout-form");

    if (payButton && checkoutForm) {
        payButton.addEventListener("click", function (event) {
            event.preventDefault();  // Prevent default button behavior

            // Validate form before submitting
            if (validateCheckoutForm()) {
                checkoutForm.submit();  // If valid, submit the form
            }
        });
    }
});

/**
 * ✅ Function to validate checkout form before submitting
 */
document.addEventListener("DOMContentLoaded", function () {
    const payButton = document.getElementById("pay-with-stripe");
    const checkoutForm = document.getElementById("checkout-form");

    if (payButton && checkoutForm) {
        payButton.addEventListener("click", function (event) {
            event.preventDefault();  // Stop default button action

            // Validate form before submitting
            if (validateCheckoutForm()) {
                checkoutForm.submit();  // If valid, submit the form
            }
        });
    } else {
        console.error("⚠️ Checkout form or pay button not found! Check your HTML.");
    }
});

/**
 * ✅ Function to validate checkout form before submitting
 */
document.addEventListener("DOMContentLoaded", function () {
    const payButton = document.getElementById("pay-with-stripe");
    const checkoutForm = document.getElementById("checkout-form");

    if (payButton && checkoutForm) {
        payButton.addEventListener("click", function (event) {
            event.preventDefault();  // Stop default button action

            const isValid = validateCheckoutForm();
            if (isValid) {
                checkoutForm.submit();
            }
        });
    } else {
        console.error("⚠️ pay-with-stripe button or checkout-form not found in HTML.");
    }
});

/**
 * ✅ Function to validate checkout form before submitting
 */
document.addEventListener("DOMContentLoaded", function () {
    const payButton = document.getElementById("pay-with-stripe");
    const checkoutForm = document.getElementById("checkout-form");

    if (payButton && checkoutForm) {
        payButton.addEventListener("click", function (event) {
            event.preventDefault();  // Stop default button action

            if (validateCheckoutForm()) {
                checkoutForm.submit();  // ✅ If valid, submit the form
            }
        });
    } else {
        console.error("⚠️ pay-with-stripe button or checkout-form not found in HTML.");
    }
});

/**
 * ✅ Validates the checkout form and displays errors inline (under the fields).
 * @returns {boolean} True if valid, False if errors exist.
 */
function validateCheckoutForm() {
    let isValid = true;  // Assume form is valid initially

    // Reset previous error messages
    document.querySelectorAll(".error-message").forEach(el => el.remove());

    // Get all form fields
    const formFields = {
        full_name: { field: document.querySelector("input[name='full_name']"), error: "Full Name is required." },
        email: { field: document.querySelector("input[name='email']"), error: "Valid email address is required." },
        phone_number: { field: document.querySelector("input[name='phone_number']"), error: "Valid phone number is required (7-15 digits)." },
        street_address1: { field: document.querySelector("input[name='street_address1']"), error: "Street Address is required." },
        town_or_city: { field: document.querySelector("input[name='town_or_city']"), error: "Town/City is required." },
        country: { field: document.querySelector("select[name='country']"), error: "Country selection is required." }
    };

    // Regex patterns
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[\d\s\-+()]{7,15}$/;

    // Validate fields
    for (let key in formFields) {
        let fieldData = formFields[key];
        let field = fieldData.field;
        let value = field ? field.value.trim() : "";

        if (!value) {
            showError(field, fieldData.error);
            isValid = false;
        }

        // Special validation for email format
        if (key === "email" && value && !emailRegex.test(value)) {
            showError(field, "Invalid email format. Example: user@example.com");
            isValid = false;
        }

        // Special validation for phone number
        if (key === "phone_number" && value && !phoneRegex.test(value)) {
            showError(field, "Invalid phone number. Allowed: digits, spaces, +, (), -");
            isValid = false;
        }
    }

    return isValid;  // ✅ Return true if no errors
}

/**
 * ✅ Displays an inline error message below the input field.
 * @param {HTMLElement} field - The form input/select element.
 * @param {string} message - The error message to display.
 */
function showError(field, message) {
    if (field) {
        const errorElement = document.createElement("div");
        errorElement.className = "error-message text-danger small mt-1";
        errorElement.innerText = message;
        field.classList.add("is-invalid");  // ✅ Bootstrap invalid styling
        field.parentNode.appendChild(errorElement);
    }
}