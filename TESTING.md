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

#### Python Code & PEP8 Compliance: 
 * Validated with: flake8 for PEP8 compliance.
 * No major syntax issues found.
 * Ensured:
  - Proper indentation.
  - Maximum line length (79 characters).
  - Removed unused imports.


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
| **View Product List**      | In the admin dashboard, click on Products under app models. | Product list page loads displaying all products, their prices, categories, and statuses. | Pss |
| **Add New Product**        | On the product list page, click "Add Product", fill details, submit. | New product is successfully created, visible in the product list. | Fail/Product Model Need img url field |
| **Edit Existing Product** | From the product list, select an existing product, edit details, submit. | Product details update successfully and changes reflect immediately. | Pass |
| **Delete Product** | From the product list, select a product, click "Delete", confirm. | Product is successfully deleted and no longer visible in the product list. | Pass |
| **View User List** | Click Users under authentication and authorization section. | Displays a list of all registered users with usernames, emails, and active statuses. | Pass |



---