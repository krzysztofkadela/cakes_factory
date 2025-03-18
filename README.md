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
![Main page](/screenshots/mainpage.png) 
* navbar
* main
* footer

## Navbar :
#### [Menu](#features)
  ![Navbar](/screenshots/navbarlogin.png)
   * Depending on the user's status, different sharing options

## About Page :
#### Basic page not finish yet:
#### [Avout](#features)
  ![About](/screenshots/aboutpage.png)
   * Info about restaurant

## Menu Page :
#### [Menu](#features)
  ![Menu](/screenshots/menu.png)
   * Displays the entire restaurant menu. 

## Account for users :
#### [Menu](#features)
  ### Registration form:

  ![Registration](/screenshots/registerform.png)
   * New user is able to create account.
   * Acount is needed to add comment and make table reservation.

  ### Login form for registered user:

  ![signin](/screenshots/sininform.png)
   * Registered user can login.

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
   * Includes contact number, location, email adrres.
   * Address
   * Opening hours


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



---
## Testing:
#### [Menu](#features)

### Validation reports:
  #### Main page html validation report:
  * ![mainpage](/screenshots/htmlmainpage.png)
  #### About page html validation report:
  * ![aboutnpage](/screenshots/htmlabout.png)
  #### Resrevation page html validation report:
  * ![reservationnpage](/screenshots/htmlreservation.png)

  * No errors found in html.
  
## Manual Testing:
#### [Menu](#features)

 #### Register new user

<table>
  <tr>
    <th>User Choice</th>
    <th>Expected Action</th>
    <th>Result Correct Input</th>
    <th>Result Incorrect Input</th>
  </tr>
  <tr>
    <td>Register new user navbar link</td>
    <td>Display the registration form</td>
    <td>Form displays</td>
    <td>No wrong input required is only link.</td>
  </tr>
  <tr>
    <td> Fill out registration form</td>
    <td>Complete the form and submit .</td>
    <td>A success message confirming registration appears</td>
    <td>Error message indicating what fields need correction.</td>
  </tr>
  <tr>
    <td>Correctly filled email address </td>
    <td>Check email field for valid email format</td>
    <td>Acknowledgment of successful email entry</td>
    <td>Error about invalid email format appears </td>
  </tr>
  <tr>
    <td>Password confirmation</td>
    <td>Confirm passwords match</td>
    <td>Registration is successful; user is created</td>
    <td>Error indicating passwords do not match appears</td>
  </tr>

</table>

#### Logged-in User Adds Comment

<table>
  <tr>
    <th>User Choice</th>
    <th>Expected Action</th>
    <th>Result Correct Input</th>
    <th>Result Incorrect Input</th>
  </tr>
  <tr>
    <td>Navigate to comments section</td>
    <td>Access the comments feature</td>
    <td>Displays the current comments and an input form to add new comments</td>
    <td>No comments found message</td>
  </tr>
  <tr>
    <td>Fill out comment form </td>
    <td>Complete the form and submit.</td>
    <td>A success message confirming registration appears</td>
    <td> Error message indicating that the comment is empty or invalid</td>
  </tr>
  <tr>
    <td>View added comment</td>
    <td>Refresh or navigate back to comments section </td>
    <td>The new comment appears in the list of comments </td>
    <td> No change in comments displayed</td>
  </tr>
</table>

#### Logged-in User Making a Reservation

<table>
  <tr>
    <th>User Choice</th>
    <th>Expected Action</th>
    <th>Result Correct Input</th>
    <th>Result Incorrect Input</th>
  </tr>
  <tr>
    <td>Navigate to reservation section</td>
    <td>Access the make reservation page</td>
    <td>Displays the booking form with fields to fill</td>
    <td>No wrong input</td>
  </tr>
  <tr>
    <td>Fill out reservation form</td>
    <td>Complete the form with valid details</td>
    <td>A success message confirming the reservation appears</td>
    <td>Warning message indicating that the fields cannot be empty</td>
  </tr>
  <tr>
    <td>Select booking date</td>
    <td>Choose a valid booking date from the calendar</td>
    <td>Shows the selected date in the form</td>
    <td></td>
  </tr>
  <tr>
    <td> Select booking time</td>
    <td>Choose a booking time from the available options</td>
    <td>Shows the selected time in the form</td>
    <td></td>
  </tr>
  <tr>
    <td>Attempt to make reservation less than 24 hours</td>
    <td>Fill form for pass date</td>
    <td>Warning appears indicating booking must be at least 24 hours in advance</td>
    <td> No reservation is made, and the user remains on the form</td>
  </tr>
</table>

#### Deleting a Reservation

<table>
  <tr>
    <th>User Choice</th>
    <th>Expected Action</th>
    <th>Result Correct Input</th>
    <th>Result Incorrect Input</th>
  </tr>
  <tr>
    <td>Navigate to reservations section</td>
    <td>Access the comments feature</td>
    <td>Displays the current comments and an input form to add new comments</td>
    <td>No comments found message</td>
  </tr>
  <tr>
    <td> Click on 'Cancel' for a reservation</td>
    <td>Confirm cancellation prompt</td>
    <td>Displays the current reservations associated with the user</td>
    <td> If no reservation section is blank</td>
  </tr>
  <tr>
    <td>View added comment</td>
    <td>Refresh or navigate back to comments section </td>
    <td>A success message confirming that the reservation has been cancelled appears</td>
    <td>Error message appears if the reservation does not exist</td>
  </tr>
</table>

## Automated Testing
#### [Menu](#features)

The Machos Takeaway project utilizes Django's built-in testing framework to ensure that all key functionalities work as expected. Below are the details of the tests implemented for various components of the application.

### Tests Overview
#### [Menu](#features)

- **Reservation Tests**:
  - **`test_make_reservation`**: Verifies that a logged-in user can successfully create a reservation and receives a success message.
  - **`test_reservation_with_short_notice`**: Checks that a user cannot make a reservation less than 24 hours in advance, displaying an appropriate warning message.
  - **`test_cancel_reservation`**: Confirms that users can cancel their own reservations and receive a success message.
  - **`test_cancel_nonexistent_reservation`**: Tests that attempting to cancel a non-existent reservation results in the appropriate error handling.

- **Menu Tests**:
  - **`test_menu_view_status_code`**: Ensures that the menu view loads successfully with a status code of 200.
  - **`test_menu_view_template`**: Checks that the correct template is used to display the menu.
  - **`test_menu_view_context`**: Verifies that the context contains the expected menu items.

- **Main Page Tests**:
  - **`test_main_page_loads`**: Tests that the main page loads successfully with a status code of 200.
  - **`test_main_page_template_used`**: Ensures that the correct template is used when rendering the main page.
  - **`test_main_page_context`**: Checks that the context of the main page contains the expected number of approved comments.

- **JavaScript Tests**:
  - **Alert Functionality**: 
    - The JavaScript tests verify that auto-closing alert messages disappear after a specified time and can be smoothly faded out.
    - Tests utilize **Jest** and **@testing-library/jest-dom** to ensure DOM manipulation occurs as expected.

  ![Allerttestjs](/screenshots/allerttestjs.png)

### Running the Tests

   To run all tests in the Django project, use the following command:

    python manage.py test


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