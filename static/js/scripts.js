/*!
* Start Bootstrap - Shop Homepage v5.0.6
* Licensed under MIT
*/

// ---------------------------
// Add to Cart with AJAX
// ---------------------------
document.addEventListener("DOMContentLoaded", function () {
    const addToCartForms = document.querySelectorAll(".add-to-cart-form");

    addToCartForms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const formData = new FormData(this);
            const actionUrl = this.getAttribute("action");

            fetch(actionUrl, {
                method: "POST",
                body: formData,
                headers: { "X-Requested-With": "XMLHttpRequest" },
            })
            .then(response => response.json())
            .then(data => {
                if (data.cart_items !== undefined) {
                    document.getElementById("cart-count").innerText = data.cart_items;
                    if (document.getElementById("cart-total") && data.cart_total_price) {
                        document.getElementById("cart-total").innerText = `€${data.cart_total_price.toFixed(2)}`;
                    }

                    const successMessage = document.createElement("div");
                    successMessage.classList.add("alert", "alert-success", "mt-2");
                    successMessage.innerHTML = "Item added to cart!";
                    document.body.appendChild(successMessage);

                    setTimeout(() => successMessage.remove(), 3000);
                } else {
                    window.location.href = actionUrl;
                }
            })
            .catch(error => console.error("Error adding to cart:", error));
        });
    });
});

// ---------------------------
// Dynamic Price Update
// ---------------------------
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

// ---------------------------
// Checkout Validation & Submission
// ---------------------------
document.addEventListener("DOMContentLoaded", function () {
    const payButton = document.getElementById("pay-with-stripe");
    const checkoutForm = document.getElementById("checkout-form");

    if (payButton && checkoutForm) {
        payButton.addEventListener("click", function (event) {
            event.preventDefault();
            if (validateCheckoutForm()) {
                checkoutForm.submit();
            }
        });
    }
});

function validateCheckoutForm() {
    let isValid = true;

    document.querySelectorAll(".error-message").forEach(el => el.remove());

    const formFields = {
        full_name: { field: document.querySelector("input[name='full_name']"), error: "Full Name is required." },
        email: { field: document.querySelector("input[name='email']"), error: "Valid email is required." },
        phone_number: { field: document.querySelector("input[name='phone_number']"), error: "Valid phone number is required." },
        street_address1: { field: document.querySelector("input[name='street_address1']"), error: "Street Address is required." },
        town_or_city: { field: document.querySelector("input[name='town_or_city']"), error: "Town/City is required." },
        country: { field: document.querySelector("select[name='country']"), error: "Country selection is required." }
    };

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[\d\s\-+()]{7,15}$/;

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

function showError(field, message) {
    if (field) {
        const errorElement = document.createElement("div");
        errorElement.className = "error-message text-danger small mt-1";
        errorElement.innerText = message;
        field.classList.add("is-invalid");
        field.parentNode.appendChild(errorElement);
    }
}

// ---------------------------
// Newsletter signup – AJAX
// ---------------------------
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("newsletter-form");
    const box = document.getElementById("newsletter-msg");

    if (!form || !box) return;

    form.addEventListener("submit", e => {
        e.preventDefault();
        const data = new FormData(form);
        fetch(form.action, {
            method : "POST",
            body   : data,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken"     : data.get("csrfmiddlewaretoken")
            }
        })
        .then(r => r.json())
        .then(j => {
            const cls = j.success ? "success" : "danger";
            const txt = j.success || j.error || "⚠️ Something went wrong.";
            box.innerHTML = `
              <div class="alert alert-${cls} alert-dismissible fade show" role="alert">
                ${txt}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>`;
            if (j.success) form.reset();
        })
        .catch(err => {
            console.error("Newsletter error:", err);
            box.innerHTML = `
              <div class="alert alert-danger alert-dismissible fade show" role="alert">
                ⚠️ Server error. Please try again.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>`;
        });
    });
});

// ---------------------------
// Auto-close alerts after 5s (Page Load & Dynamic)
// ---------------------------
function autoCloseAlerts() {
    setTimeout(() => {
        const alerts = document.querySelectorAll(".alert");
        alerts.forEach(alert => {
            if (!alert.classList.contains("fading")) {
                alert.classList.add("fading");
                alert.classList.add("fade-out");
                setTimeout(() => {
                    if (typeof bootstrap !== "undefined" && bootstrap.Alert) {
                        let bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                        bsAlert.close();
                    } else {
                        alert.remove();
                    }
                }, 500);
            }
        });
    }, 5000);
}

document.addEventListener("DOMContentLoaded", autoCloseAlerts);

const alertObserver = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1 && node.classList.contains("alert")) {
                autoCloseAlerts();
            }
        });
    });
});
alertObserver.observe(document.body, { childList: true, subtree: true });