# FoodOnline - Multi-Vendor Restaurant Marketplace

FoodOnline is a full-fledged Multi-Vendor Restaurant Marketplace built using Python and Django. The platform allows vendors to list their restaurants and food items, while customers can order food based on their location and preferences. This project offers comprehensive functionalities such as dynamic tax modules, location-based search, and payment gateway integrations.

## Table of Contents
- [Installation](#installation)
- [Features](#features)
- [Technologies](#technologies)
- [How to Run](#how-to-run)
- [Project Structure](#project-structure)

## Features

### Vendor Dashboard
- Vendor registration and authentication.
- Admin approval for vendors.
- Vendor-specific dashboards to manage orders, food items, and more.
- Custom restaurant profile form with validation.

### Customer Features
- Location-based search to find nearby restaurants.
- Cart functionalities with AJAX requests, no page refresh needed.
- Place orders, generate order numbers, and handle after-order functionalities.
- Integration with PayPal, Payme and Click for seamless payments.
- Dynamic business hours and tax modules.
- Smart and basic search functionalities for finding food and restaurants.

### Database and User Management
- Custom user model to cater to both vendors and customers.
- PostgreSQL database configuration for robust data management.
- Email verification and token-based authentication.
- Django signals to handle user-related activities.
- Many-to-many relationships for handling vendor and food item associations.

### Miscellaneous Features
- Google Autocomplete field for better search experience.
- Dynamic tax module integrated into the cart and checkout process.
- Marketplace functionality with multiple vendors.
- Mobile-responsive layout for a seamless experience on all devices.

## Technologies Used
- **Django**: Web framework for building the backend.
- **PostgreSQL**: Database management system.
- **AJAX**: For seamless frontend interactions.
- **Paypal, Payme & Click**: Payment gateway integration.
- **Google Autocomplete**: For restaurant search.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Sardorbek-Zayniyev/foodOnline.git


2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run database migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```

The app will be available at `http://127.0.0.1:8000/`.

## Project Structure

The project follows a modular structure, with each app dedicated to specific functionality:

- `accounts/`: Handles user authentication and registration.
- `orders/`: Manages the cart and order processes.
- `vendors/`: Manages vendor details and restaurant profiles.
- `customers/`: Contains customer-specific features and profiles.
- `foodmenu/`: Manages food items and menu-related functionalities.
- `templates/`: Contains all the HTML templates used in the project.
- `static/`: Stores all static files like CSS, JavaScript, and images.