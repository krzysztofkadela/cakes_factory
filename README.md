# 🎂 Cake Factory - E-commerce Project 🍰

## 🚀 Live Project
🔗 **Cake Factory on Heroku**: [Cake Factory](https://cake-factory-65cd55cbb35d.herokuapp.com/)

---

![Am_I_Responsive](READMEmedia/cake-store-preview.png)

Cake Factory is an **elegant e-commerce platform** built using **Django**. Customers can **browse, order, and purchase** custom cakes and cupcakes for special occasions. The platform integrates **Stripe** for secure payments, offers **custom cake ordering**, and includes **marketing features** like newsletters and a Facebook Business Page.

This project was developed as part of a **Full-Stack Web Development course**, ensuring it meets industry standards in **security, UX, and functionality**.

## [Features](#features-1)
* ### [MainPage](#main-page)
  * #### [MainPageDelas](#main-page-offer-section)
  * #### [MainPageLocation](#main-page-location-section)
  * #### [MainPageCustomerComments](#main-page-customers-comments-section)
* ### [Navbar](#navbar-1)
* ### [About](#about-page)
* ### [Menu Page](#menu-page-1)
* ### [Account for Users](#account-for-users-1)
* ### [Footer Section](#footer-section-1)
### [Technologies](#technologies-1)
### [Programs_Used_in_project](#programs-used-in-project)
### [Testing](#testing-1)
* [Validation_reports](#validation-reports)
* [Manual_Testing](#manual-testing)
* [Making_a_Reservation](#making-a-reservation)
* [Deleting_a_Reservation](#deleting-a-reservation)
### [Automated Testing](#automated-testing)
### [Deployment](#deployment)
### [Bugs Detected](#bugs-detected)
### [Credits](#credits)
* [Other](#other)
---

# Features:
### General
* Fully **responsive** for mobile and desktop users 
* **User authentication** (register, login, logout)
* **Role-based access** (Admin vs Customer)
* **Secure checkout** process with **Stripe integration**

### Shopping & Orders
* Browse **cake products** with categories
* Add cakes to the **shopping cart**
* Apply **discount codes** (future feature)
* **Order tracking & confirmation emails**

### Admin Panel
* **Manage product listings** (add/edit/delete cakes)
* Track **customer orders & payments**
* Manage **users and newsletters**

### Marketing & SEO 
* **Facebook Business Page** integration
* **Newsletter signup** for exclusive discounts 
* **SEO optimization** (meta tags, robots.txt, sitemap.xml) 

# Features some screenshots:

## Main Page:
![Main page](/READMEmedia/main_page.png) 
* navbar
* hero section
* footer

## Navbar :
#### [Menu](#features)
  ![Navbar](/READMEmedia/navbar.png)
   #### Left section(Main Navigation)
   * Home → href="{% url 'home' %}"
   * About → href="{% url 'about' %}"
   * Categories (Dropdown)
     - All Products → href="{% url 'product_list' %}"
     - Dynamically generated category links based on available product categories.
  #### Right Section (User Account & Cart)
  * Account (Dropdown)
   - Profile (if logged in) → href="{% url 'user_profile' %}"
   - Logout (if logged in) → href="{% url 'account_logout' %}"
   - Sign In (if logged out) → href="{% url 'account_login' %}"
   - Sign Up (if logged out) → href="{% url 'account_signup' %}"
  * Cart → href="{% url 'cart_view' %}"
   - Displays the number of items in the cart dynamically.

## About Page :
#### Basic page not finish yet:
#### [Avout](#features)
  ![About](/READMEmedia/main.png)
   * Info about restaurant

## Product List :
#### [Product_list](#features)
  ![Product_list](/READMEmedia/product_list.png)
   * Displays product list. 

## Product details :
#### [Product_detail](#features)
  ![Product_detail](/READMEmedia/product_detail.png)
  #### Product Image:
   * A high-quality image showcasing the cake.
   * A detailed description of ingredients, flavors, and customization options.
  #### Size Selection (if applicable):
   * Users can choose between Small, Large, X-Large, affecting pricing.
  #### Price:
   * Adjusted based on the selected size.
  #### Quantity Selector:
   * Customization Field (functionality need to be aproved)
   * A text field where users can add special requests (e.g., "Happy Birthday John!").
  #### Add to Cart Button:
   * Adds the product to the user's cart.
   * Uses AJAX for a seamless experience without page reloads.
  #### Back to Products Button:
   * A button or breadcrumb link allowing users to return to the product listing page.

## Shopping Cart Page :
#### [Menu](#features)
  ![signin](/screenshots/sininform.png)
  #### Cart Item List:
   * Displays a table/list view of all products added to the cart.
   * Each row contains:
    - Product Name
    - Size Selection (if applicable)
    - Quantity (with an update feature)
    - Price per unit
    - Subtotal price (quantity × unit price)
    - Remove Button
  #### Update Quantity:
   * Users can modify the quantity of each item.
   * Clicking Update adjusts the subtotal dynamically.
  #### Customization Requests:
   * If a product has customization, it is displayed below the product name.
  #### Cart Summary:
   * Displays total price of all items in the cart.
   * Delivery Charges: Calculated if applicable.
   * Grand Total: Order total including any additional costs.
  #### Proceed to Checkout Button:
   * Redirects users to the checkout page to complete the order.
  #### Continue Shopping Button:
   * Links back to the Product Listing Page for more browsing.



  ### Logout form:

  ![Signout](/screenshots/signout.png)
   * For user to logout from his account.

## Options for logged in users:
#### [Menu](#features)
  
   ### Make reservation (book table):

  ![Makereservation](/screenshots/makereservation.png)
   * User can easy make reservation by using reservation form.

  ### Manage reservation see reservation status:

  ![Reservation](/screenshots/reservation.png)
   * User can easy check reservation status can also cancel reservation.

  ### Leave a comment:

  ![Comments](/screenshots/comments.png)
   * In this section user can add/delete or edit comments.
   * Only comments done by loged in user are displayed in this section.
   * User can only change his comments.


## Footer section:
#### [Menu](#features)
   
   ![Footer](/screenshots/footer.png)
   * Social media links (for now only facbook page is active, more is comming soon)
   * Subscribe to Neesletter
   ![Footer](/screenshots/footer.png)


## User Experience (UX)

###  **Target Audience**  
-  Cake lovers looking for **delicious treats**  
-  Individuals planning **special events** (birthdays, weddings, parties)  
-  Small businesses needing **bulk cake orders**

###  **Wireframes & UX Planning**  
Wireframes & UX documentation are included in the **docs/** folder. 

###  **Color Scheme**  
The project follows a **Classic & Elegant** theme:  
**Soft Gold (#E8C39E)** |  **Rich Chocolate (#5D4037)** |  **Vanilla Cream (#FAF3E0)** |  **Cherry Red (#D7263D)**  

---

##  Technology Stack:
#### [Menu](#features)
 ### **Backend**
 * **Python & Django** (Django Framework)
 * **PostgreSQL** (Relational Database)
 * **Stripe API** (Secure payments)
 * **AWS S3** (Media storage)
 
 ### **Frontend**  
 * **HTML, CSS, JavaScript** (Custom UI)
 * **Bootstrap 5 & Crispy Forms**
 * **Django Templating**

 ### **Deployment & Hosting**
 * **Heroku** (Cloud hosting)
 * **GitHub** (Version control)
 * **AWS S3** (Static & media files)
 * **Mailchimp** (Newsletter service)
 ---

## 🏗 Installation & Setup

### 1️⃣ Clone the Repository  
```
bash

git clone https://github.com/krzysztofkadela/cakes_factory.git  
cd cakes_factory 
```
### 2️⃣ Set Up Virtual Environment  
```
bash

python -m venv env  
source env/bin/activate  # On Windows: env\Scripts\activate   
```
### 3️⃣ Install Dependencies  
```
bash

 pip install -r requirements.txt  
```
### 4️⃣ Set Up Environment Variables
* Create a .env file and add:  
```
env

SECRET_KEY=your-secret-key  
DATABASE_URL=your-database-url  
STRIPE_SECRET_KEY=your-stripe-secret  
AWS_ACCESS_KEY_ID=your-aws-key  
AWS_SECRET_ACCESS_KEY=your-aws-secret   
```
### 5️⃣ Apply Migrations & Run Server
```
bash

python manage.py migrate  
python manage.py runserver   
```
##  Deployment:
#### [Menu](#features)
#### The application is deployed on Heroku with static/media files stored on AWS S3.

### Steps to Deploy:
 
   * Push Code to GitHub:
   ```
   bash

   git add .  
   git commit -m "Deploying Cake Factory"  
   git push origin main 
   ```
   * Deploy to Heroku:
  ```
    bash

    heroku create cake-factory  
    heroku config:set DISABLE_COLLECTSTATIC=1  
    git push heroku main 
  ```
   * Run Migrations on Heroku:
  ```
    bash

    heroku run python manage.py migrate 
  ```
   * Collect Static Files
  ```
    bash

    heroku run python manage.py collectstatic --noinput  
  ```
  ### Simply deploy on Heroku Dashboard:

---

##   Search Engine Optimization (SEO):
 - Meta Descriptions: Added for better search visibility
 - Robots.txt: Blocks unwanted crawling
 - Sitemap.xml: Helps Google index the website
 - Canonical Links: Avoids duplicate content issues
 - Custom 404 Page: Prevents user frustration

##   Security Measures:
 - All secret keys hidden in .env
 - HTTPS enforced (via Heroku settings)
 - Role-based authentication (Admin vs. Customer)
 - CSRF protection enabled


## Bugs Detected:
#### [Menu](#features)

 - **Issue with Reservation Date Input**: 
 
   **Resolution**: 
 
  
## Unfixed Bugs:
  * All detected bugs have been fixed.

## Credits:
  *  To check the correct operation of most functions, the following was used:
     [Python Tutor](https://pythontutor.com/visualize.html#mode=edit)
  *  Template use for a project was downloaded from https://themewagon.com/themes/

### Other:
  
   * Much of the information about python was obtained from https://www.w3schools.com/python/.

#### [Menu](#features)