Food Waste Management System

This is a Flask-based web application designed to reduce food waste by connecting food donors, NGOs, and administrators on a single platform. The system allows users to donate excess food, enables NGOs to view and pick up donations, and provides admins with tools to manage and monitor all activities.

The project uses Python (Flask) for backend development and CSV files as a lightweight database system to store all data including users, donations, messages, and contact information.

Project Features:

The system supports user registration and login with different roles such as donor, NGO, and admin. Donors can add food donation details including food item, quantity, location, and reason for waste. NGOs can view available donations and mark them as picked up once collected.

The system also includes a messaging feature where notifications are sent to NGOs when new users register or when donations are marked for pickup. A contact form is available for users to send queries or feedback.

File upload functionality is implemented to allow users to upload food images and acknowledgment documents. The system also generates PDF acknowledgment slips automatically after successful pickup of food donations.

All data is stored in CSV files which act as a simple database system. Separate files are maintained for users, donations, messages, contact forms, and lab test data.

Technologies Used:

Python is used as the main programming language. Flask is used for backend development and API creation. Flask-CORS is used for handling cross-origin requests. CSV files are used for data storage instead of a traditional database. FPDF library is used for generating PDF acknowledgment slips. Werkzeug is used for secure file uploads.

Project Structure:

The project contains the main Flask application file, a CSV folder to store all data files, and an uploads folder to store images and documents. Each CSV file is used for a specific purpose such as storing waste data, user information, messages, and contact form submissions.

How the System Works:

Users first register and log in based on their role. Donors submit food donation details through the system. NGOs can view available donations and request pickups. Once a donation is picked up, the system updates the status and sends notifications. The system also stores uploaded files and generates acknowledgment slips in PDF format.

Purpose of the Project:

The main objective of this project is to reduce food waste by efficiently managing excess food distribution. It helps connect donors and NGOs through a digital platform and ensures proper tracking of food donations. The project also helps in understanding real-world backend development, database handling using CSV, and REST API creation.

Future Improvements:

This system can be improved by integrating a proper database like MySQL instead of CSV files. A frontend dashboard can be added for better user experience. Real-time notifications and cloud deployment can also be implemented for scalability.
