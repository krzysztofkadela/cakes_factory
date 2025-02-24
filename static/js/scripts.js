/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/

// 🟢 Auto-close alerts after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        let alerts = document.querySelectorAll(".alert");
        alerts.forEach(alert => {
            if (typeof bootstrap !== "undefined" && bootstrap.Alert) {
                let bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000); 
});

// 🛒 Add to Cart with AJAX
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
                    document.getElementById("cart-count").innerText = data.cart_items;
                    if (document.getElementById("cart-total") && data.cart_total_price) {
                        document.getElementById("cart-total").innerText = `€${data.cart_total_price.toFixed(2)}`;
                    }

                    // Success Message
                    const successMessage = document.createElement("div");
                    successMessage.classList.add("alert", "alert-success", "mt-2");
                    successMessage.innerHTML = "Item added to cart!";
                    document.body.appendChild(successMessage);

                    setTimeout(() => successMessage.remove(), 3000); // Auto-remove
                } else {
                    window.location.href = actionUrl;  
                }
            })
            .catch(error => console.error("Error adding to cart:", error));
        });
    });
});

// 🏷️ Dynamic Price Update
document.addEventListener("DOMContentLoaded", function () {
    const sizeDropdown = document.getElementById("size");
    const priceDisplay = document.getElementById("product-price");

    if (sizeDropdown && priceDisplay) {
        const basePrice = parseFloat(priceDisplay.dataset.basePrice);
        const sizeAdjustments = { "Small": 0, "Large": 20, "X-large": 40 };

        sizeDropdown.addEventListener("change", function () {
            const selectedSize = sizeDropdown.options[sizeDropdown.selectedIndex].text.trim();
            const extraCost = sizeAdjustments[selectedSize] || 0;
            const newPrice = basePrice + extraCost;

            if (!isNaN(newPrice)) {
                priceDisplay.innerText = `€${newPrice.toFixed(2)}`;
            }
        });
    }
});

// ✅ Checkout Validation & Submission
document.addEventListener("DOMContentLoaded", function () {
    const payButton = document.getElementById("pay-with-stripe");
    const checkoutForm = document.getElementById("checkout-form");

    if (checkoutForm) {  // ✅ Only run the script if the checkout form exists
        if (payButton) {
            payButton.addEventListener("click", function (event) {
                event.preventDefault(); // Prevent default button behavior

                if (validateCheckoutForm()) {
                    console.log("✅ Checkout form validated! Proceeding to payment.");
                    checkoutForm.submit(); 
                } else {
                    console.error("❌ Checkout form validation failed!");
                }
            });
        } else {
            console.warn("⚠️ Checkout form found, but pay-with-stripe button is missing.");
        }
    } else {
        console.info("ℹ️ Checkout form not found on this page. Skipping checkout script.");
    }
});

// ✅ Function to validate checkout form before submitting
function validateCheckoutForm() {
    let isValid = true;

    // Remove previous error messages
    document.querySelectorAll(".error-message").forEach(el => el.remove());

    // Get form fields
    const formFields = {
        full_name: { field: document.querySelector("input[name='full_name']"), error: "Full Name is required." },
        email: { field: document.querySelector("input[name='email']"), error: "Valid email is required." },
        phone_number: { field: document.querySelector("input[name='phone_number']"), error: "Valid phone number is required." },
        street_address1: { field: document.querySelector("input[name='street_address1']"), error: "Street Address is required." },
        town_or_city: { field: document.querySelector("input[name='town_or_city']"), error: "Town/City is required." },
        country: { field: document.querySelector("select[name='country']"), error: "Country selection is required." }
    };

    // Validation regex
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

        if (key === "email" && value && !emailRegex.test(value)) {
            showError(field, "Invalid email format. Example: user@example.com");
            isValid = false;
        }

        if (key === "phone_number" && value && !phoneRegex.test(value)) {
            showError(field, "Invalid phone number. Allowed: digits, spaces, +, (), -");
            isValid = false;
        }
    }

    return isValid;
}

// ✅ Displays an error message below the input field
function showError(field, message) {
    if (field) {
        const errorElement = document.createElement("div");
        errorElement.className = "error-message text-danger small mt-1";
        errorElement.innerText = message;
        field.classList.add("is-invalid");
        field.parentNode.appendChild(errorElement);
    }
}