Food Waste Management System

This is a Flask based web application designed to reduce food waste by connecting food donors, NGOs, and administrators on a single platform. The system allows users to donate excess food, enables NGOs to view and collect donations, and provides administrators with tools to manage and monitor all activities.

The project is developed using Python with the Flask framework for backend development. It uses CSV files as a lightweight database system to store all application data including users, food donations, messages, and contact information.

Project Features

The system supports user registration and login with different roles such as donor, NGO, and administrator. Donors can submit food donation details including food item, quantity, location, and reason for waste.

NGOs can view available donations and mark them as picked up once the food is collected. The system automatically updates the status of each donation to ensure proper tracking.

A messaging feature is included to send notifications to NGOs when new users register or when donations are marked as picked up. A contact form is also available for users to send queries or feedback.

The system provides file upload functionality to allow users to upload food images and acknowledgment documents. After a successful pickup, the system generates a PDF acknowledgment slip automatically for record keeping.

Technologies Used

The project is built using Python as the main programming language. Flask is used for backend development and API creation. Flask CORS is used to handle cross origin requests. CSV files are used as the database system instead of a traditional database. The FPDF library is used for generating PDF acknowledgment slips. Werkzeug is used for secure file upload handling.

Project Structure

The project consists of a main Flask application file, a CSV folder that stores all data files, and an uploads folder used for storing images and documents.

Each CSV file is used for a specific purpose such as storing user information, food donation records, messages, contact form submissions, and lab test data.

How the System Works

Users first register and log in according to their roles. Donors submit food donation details through the system. NGOs can view available donations and request pickups.

Once a donation is marked as picked up, the system updates its status and sends notifications to relevant users. Uploaded files are stored securely and acknowledgment slips are generated in PDF format after successful pickup.

Purpose of the Project

The main purpose of this project is to reduce food waste by efficiently managing and distributing excess food. It helps connect donors and NGOs through a centralized digital platform and ensures proper tracking of food donations.

The project also helps in understanding real world backend development, database handling using CSV files, and REST API creation.

Future Improvements

This system can be improved by integrating a proper relational database like MySQL instead of CSV files. A frontend dashboard can also be added to improve user experience.

Other possible improvements include real time notifications, email alerts, and cloud deployment to make the system more scalable and production ready.
