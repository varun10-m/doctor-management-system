# Doctor Appointment Management System

A web-based application built using Flask and MySQL to manage doctor appointments efficiently. This system allows patients to book appointments, doctors to manage their schedules, and provides a seamless experience for both parties.

---

## Features

### **Patient Features**
- Register and log in to the system.
- Book appointments with doctors.
- View and manage previous appointments.
- Logout functionality.

### **Doctor Features**
- Log in to the system.
- View assigned appointments.
- Approve or reject appointments.

### **Admin Features (Future Enhancement)**
- Manage users and doctors.
- View all appointments.

---

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS
- **Database**: MySQL
- **Session Management**: Flask Sessions
- **Cross-Origin Resource Sharing**: Flask-CORS

---

## Installation and Setup

Follow these steps to set up the project on your local machine:

### **1. Clone the Repository**
```bash
git clone https://github.com/varun10-m/doctor-management-system.git
cd doctor-management-system
```

### **2. Install Dependencies**
Make sure you have Python installed. Then, install the required Python packages:
```bash
pip install flask flask-cors mysql-connector-python
```

### **3. Set Up the Database**
1. Install MySQL and create a database named `doctor_appointments`.
2. Import the SQL schema (if provided) to set up the required tables.
3. Update the database credentials in `app.py`:
   ```python
   conn = mysql.connector.connect(
       host="localhost",
       user="your_mysql_username",
       password="your_mysql_password",
       database="doctor_appointments",
       port=3306
   )
   ```

### **4. Run the Application**
Start the Flask development server:
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5000`.

---

## Project Structure

```
doctor-management-system/
│
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── index.html         # Home page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── appointment.html   # Appointment booking page
│   └── ...                # Other templates
├── static/                # Static files (CSS, JS, images)
│   └── style.css          # Stylesheet
└── README.md              # Project documentation
```

---

## Screenshots

### **Login Page**
![Login Page](static/images/Screenshot%202025-05-13%20111702.png)

### **Appointment Booking**
![Appointment Booking](static/images/Screenshot%202025-05-13%20111721.png)

---

## Future Enhancements
- Add an admin panel for managing users and doctors.
- Implement email notifications for appointment updates.
- Improve the UI using a frontend framework like Bootstrap.
- Add password hashing for better security.

---

## Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact
For any inquiries or feedback, please contact:
- **Name**: Varun
- **GitHub**: [varun10-m](https://github.com/varun10-m)
