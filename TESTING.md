# Testing

## This document outlines the testing process for the Cake Factory e-commerce application. It includes HTML, CSS, JavaScript, and Python validation results, functionality checks, UX testing, and automated testing.

#### HTML Validation:
 *  All pages passed W3C HTML Validation.
  - The code was validated using W3C Markup Validation Service.
  - No major errors were found.

 * Pages Validated:
  - Homepage
  ![Main](/READMEmedia/html_main_page_valid.png)
  - Product List Page
  ![Main](/READMEmedia/html_main_page_valid.png)
  - Product Details Page
  - Shopping Cart
  - Checkout Page
  - User Login & Signup Pages
  - User Profile Page
  - 404 Custom Error Page

---

#### CSS Validation
 * Validated with W3C CSS Validator.
  - Result: Passed with no critical errors.
![Main](/READMEmedia/css_no_errors.png)

---

#### JavaScript Validation
 * Validated with JSHint.
 - No major syntax errors.
 - 43 warnings (ES6 version) "supports modern browsers only" If older browsers need support.

---

### PEP8 & Code Quality Testing

To ensure clean, maintainable, and professional Python code, we used the following tools:

#### Tools Used:
- `flake8`: Checked for line length, indentation, whitespace, unused variables.
- `black`: Used optionally for auto-formatting before manual flake8 passes.
- `ruff`: Used with selected rules for E231, E251, and E712 to catch style violations.
- VSCode Pylint Extension (for real-time linting assistance).

#### Summary:
- All files passed `flake8` (max-line-length=79).
- All major errors and warnings have been addressed.
- Settings confirmed:
  - Proper indentation and whitespace
  - No unused imports
  - Line length set to 79 characters
  - Decorator and function spacing validated

##### Before: 
![Before](/READMEmedia/flack8errors1.png)

---

![Before](/READMEmedia/flack8errors2.png)

---

##### After : 
![After](/READMEmedia/flack0errors.png)

---

##### setup.cfg :

```
[flake8]
max-line-length = 79
exclude = migrations, __pycache__, manage.py, .vscode/*
```

## Manual Testing 


| Function                      | User Action                                                                 | Outcome                                                                                               | Result |
|------------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|--------|
| **Load Home Page**            | Access the Cake Factory homepage                                           |   Homepage loads successfully with navigation menu, hero section, and featured products.         | Pass   |
| **Signup Page**          | Click "Sign Up" from the navigation                             |  Signup page loads with fields for username, email, password, and a submit button.              | Pass   |
| **Login Page**                | Click "Sign In" from the navigation | Login page loads with username and password fields and a submit button. | Pass |
| **Browse Products**          |  Click "Categories" > "All Products" in the navigation |  Products page loads displaying available cakes and cupcakes with images, names, and prices.  | Pass |
| **Filter Products**          |  Use the category filter dropdown     |  Products page refreshes, displaying only products within the selected category.    | Pass |
| **View Product Details**     | Click on a Details button product from the products page | Product detail page loads with description, price, size options, customization options, and images. | Pass |
| **Add Product to Cart**      | Select size and customization options, then click "Add to Cart" | Product successfully added to cart, and cart icon in navigation updates the item count. | Pass |
| **View Shopping Cart**       | Click "Cart" icon from navigation  | Shopping cart page loads, showing added products with quantity, customization details, and pricing. | Pass |
| **Update Quantity in Cart** | Adjust product quantity in the shopping cart | Cart updates, recalculating product quantities and total price accordingly. | Pass |
| **Remove Item from Cart**    | Click "Remove" next to an item in the shopping cart | Item successfully removed, and the cart updates instantly reflecting changes. | Pass |
| **Proceed to Checkout**      | From the cart page, click "Proceed to Checkout" | Checkout page loads displaying cart items, billing/shipping fields, delivery date/time selections. | Pass |
| **Place an Order** | Fill out all required checkout fields and click "Pay With Stripe" | Stripe Checkout initiates; payment processed successfully and redirects to the order confirmation page. | Pass |
| **Order Confirmation** | Complete Stripe payment | Order confirmation page displays successfully with order details and order number. | Problem Detected |
| **View Order History** | Logged-in user clicks "Order History" from profile navigation | Order history page loads, displaying a list of past orders with statuses. | Pass |
| **Retry Payment** | From Order History, click "Retry Payment" on an unpaid order | Stripe Checkout loads, allowing the user to retry payment. Payment processed successfully. | Pass |
| **Newsletter Signup** | Enter email in the footer newsletter signup form and click "Subscribe" | Newsletter signup confirmed with success message. | Pass |
| **Custom 404 Page** | Navigate to a non-existent URL | Custom 404 page loads, displaying "Page not found" message with link back to homepage. | Pass |
| **Logout** | Click "Logout" from the navigation | User is logged out successfully and redirected to the homepage. | Pss |
| **SEO Metadata** | Inspect page source on homepage | Meta tags, description, canonical URL, sitemap, and robots.txt correctly implemented and accessible. | Pass |


---

## Manual Testing Admin Panel


| Function                      | User Action                                                                 | Outcome                                                                                               | Result |
|------------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|--------|
| **Admin Login**            | Visit /admin/, enter correct username/password, and submit.| Admin dashboard loads successfully, displaying available models and site management tools.            | Pass   |
| **View Product List**      | In the admin dashboard, click on Manage Products under app models. | Product list page loads displaying all products, their prices, categories, and statuses. | Pss |
| **Add New Product**        | On the product list page, click "Add Product", fill details, submit. | New product is successfully created, visible in the product list. | Fail/Product Model Need img url field |
| **Edit Existing Product** | From the product list, select an existing product, edit details, submit. | Product details update successfully and changes reflect immediately. | Pass |
| **Delete Product** | From the product list, select a product, click "Delete", confirm. | Product is successfully deleted and no longer visible in the product list. | Pass |
| **View User List** | Click Manage Users under authentication and authorization section. | Displays a list of all registered users with usernames, emails, and active statuses. | Pass |
| **View Order List** | Select Manage Orders in admin dashboard. | Order page loads with a list of all placed orders, including statuses and totals. | Pass |
| **Update Order Status** | 	Select an order, change its status (e.g., Shipped, Delivered). | Order status updates successfully and is immediately reflected. | Pass |
| **Manage Newsletter Subscribers** | Manage Subscribers from admin dashboard. | Subscriber list loads, displaying all email addresses subscribed. | Pass |
| **Delete Newsletter Subscriber** | Select a subscriber, click "Delete", confirm deletion. | Subscriber is successfully removed from the newsletter list. | Pass |

---

## Lighthouse Testing Results

| Page                    | Performance | Accessibility | Best Practices | SEO  | Notes                          |
|-------------------------|-------------|----------------|----------------|------|---------------------------------|
| **Home Page**           | 95          | 94             | 96             | 100  | Loads fast, fully optimized     |
| **Product List Page**   | 54          | 90             | 96             | 92  | Great listing speed & layout    |
| **Product Detail Page** | 100         | 87             | 99             | 100  | Detail and image loads well     |
| **Cart Page**           | 88          | 91             | 98             | 100  | JS-heavy interactions handled   |
| **Checkout Page**       | 87          | 93             | 97             | 100  | Form validation & SEO good      |
| **Login Page**          | 96          | 100            | 97             | 100  | Clean and simple auth form      |
| **Register Page**       | 95          | 100            | 96             | 100  | Strong field labeling & ARIA    |
| **Admin Management Page**| 89         | 92             | 95             | 100  | Data loads fine, minor delays   |

---

### Lighthouse Home Page: 

![Main](/READMEmedia/lighthouse_main_1.png)

![Main](/READMEmedia/lighthouse_main_2.png)

### Lighthouse Product List Page:

![Product](/READMEmedia/lighthouse_product_list.png)

### Lighthouse Product Details Page:

![Product](/READMEmedia/lighthouse_product_detail.png)

# Bug detected fix:

## Newsletter & Subscription Bugfix Validation:

- Issue: 500 errors on /newsletter-signup/ and /users/manage/subscriptions/
- Cause: Missing 'active' field migration for NewsletterSubscriber (Heroku DB out of sync)
- Fixes:
  - Applied pending migrations on Heroku
  - Cleaned up view logic, added @login_required decorators
  - Confirmed AJAX newsletter signup success response
  - Confirmed subscription management loads subscribers without errors
- Commands Used:
  - `heroku run python manage.py migrate --plan`
  - `heroku run python manage.py migrate`
- Status: Fixed and Verified on Heroku production.

## Email Sending Validation (SMTP via SendGrid):

We validated production email delivery using SendGrid’s SMTP integration to ensure real transactional emails work in live environments (e.g., signup confirmation, password reset).

SMTP Configuration:
- Backend: django.core.mail.backends.smtp.EmailBackend
- Host: smtp.sendgrid.net
- Port: 587
- TLS: Enabled
- Username: apikey
- Password: (SendGrid API key)
- Verified Sender Email: cakefactorystore24@gmail.com

Email Test Process:

| Test                   | Description                                                        | Status              |
| ---------------------- | ------------------------------------------------------------------ | ------------------- |
| **SMTP Shell Test**    | Sent test email using `send_mail()` from Django shell.             | ✅ Sent successfully |
| **Verified Sender**    | Used verified sender address (per SendGrid dashboard).             | ✅ Passed            |
| **Retry & Delivery**   | Verified email received in inbox with correct subject and message. | ✅ Passed            |
| **SendGrid Dashboard** | Email logged under Activity tab.                                   | ✅ Verified          |

```
from django.core.mail import send_mail

send_mail(
    subject="🎂 Cake Factory Email Test",
    message="✅ Success! Email via SendGrid SMTP 🎉",
    from_email="cakefactorystore24@gmail.com",
    recipient_list=["----------------------"],
    fail_silently=False,
)

```
#### Test verifycation img :

##### User Sign Up form : 

![Sign Up Test](/READMEmedia/SignUpteatEmail1.png)

##### Verification Email Sent: 

![Sign Up Test](/READMEmedia/SignUpEmailverification1.png)

##### Email Verified:

![Sign Up Test](/READMEmedia/versignin.png)

##### Login Successful:

![Sign Up Test](/READMEmedia/verisucceslogedin.png)


