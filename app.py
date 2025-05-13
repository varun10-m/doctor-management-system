from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions
CORS(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Your MySQL username
    password="MYsqlpass@123",  # Replace with your password
    database="doctor_appointments",  # Your MySQL database name
    port=3306
)
cursor = conn.cursor(dictionary=True)

# Home Page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Appointments Page (appointments.html)
@app.route('/appointment')
def appointments():
    if 'username' in session:
        return render_template('appointment.html')  # Render the appointments page
    return redirect('/login')  # Redirect to login page if not logged in

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user['username']
            return redirect('/appointment')  # Redirect to appointments page after login success
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            error = "Username already exists"
        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            success = "Registered successfully! You can login now."

    return render_template('register.html', error=error, success=success)

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

# Previous Appointments Page
@app.route('/previous_appointments')
def previous_appointments():
    if 'username' in session:
        patient_name = session['username']  # Use session username as patient_name
        # Include the description field in the query
        cursor.execute("""
            SELECT appointments.id, appointments.date, appointments.time, doctors.name AS doctor_name, appointments.status, appointments.description
            FROM appointments
            JOIN doctors ON appointments.doctor_id = doctors.id
            WHERE appointments.patient_name = %s
        """, (patient_name,))
        appointments = cursor.fetchall()
        return render_template('previous_appointments.html', appointments=appointments)
    return redirect('/login')  # Redirect to login page if not logged in

# Submit Appointment
@app.route('/submit_appointment', methods=['POST'])
def submit_appointment():
    if 'username' in session:
        patient_name = session['username']  # Use session username as patient_name
        doctor_id = request.form['doctor']  # doctor_id is now passed as an integer
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']  # New field for problem description

        # Validate the date format
        try:
            valid_date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD.", 400

        # Insert the appointment into the database
        cursor.execute(
            "INSERT INTO appointments (patient_name, doctor_id, date, time, description) VALUES (%s, %s, %s, %s, %s)",
            (patient_name, doctor_id, date, time, description)
        )
        conn.commit()
        return redirect('/appointment_success')  # Redirect to success page after submission
    return redirect('/login')  # Redirect to login page if not logged in

# Appointment Success Page
@app.route('/appointment_success')
def appointment_success():
    if 'username' in session:
        return render_template('appointment_success.html')  # Render success page
    return redirect('/login')  # Redirect to login page if not logged in

# Delete Appointment
@app.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    if 'username' in session:
        cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
        conn.commit()
        return redirect('/previous_appointments')  # Redirect after deletion
    return redirect('/login')  # Redirect to login if not logged in

# Doctor Login Page
@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Use the new doctor_login table
        cursor.execute("SELECT * FROM doctor_login WHERE username = %s AND password = %s", (username, password))
        doctor = cursor.fetchone()

        if doctor:
            session['doctor_username'] = doctor['username']
            return redirect('/doctor_dashboard')  # Redirect to doctor dashboard after login success
        else:
            error = "Invalid username or password"

    return render_template('doctor_login.html', error=error)

# Doctor Dashboard Page
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'doctor_username' in session:
        doctor_username = session['doctor_username']
        # Include the description field in the query
        cursor.execute("""
            SELECT appointments.id, appointments.patient_name, appointments.date, appointments.time, appointments.status, appointments.description
            FROM appointments
            JOIN doctor_login ON appointments.doctor_id = doctor_login.id
            WHERE doctor_login.username = %s
        """, (doctor_username,))
        appointments = cursor.fetchall()
        return render_template('doctor_dashboard.html', doctor_username=doctor_username, appointments=appointments)
    return redirect('/doctor_login')  # Redirect to doctor login if not logged in

# Grant Appointment
@app.route('/grant_appointment/<int:appointment_id>', methods=['POST'])
def grant_appointment(appointment_id):
    if 'doctor_username' in session:
        cursor.execute("UPDATE appointments SET status = 'Granted' WHERE id = %s", (appointment_id,))
        conn.commit()
        return redirect('/doctor_dashboard')  # Redirect back to the doctor dashboard
    return redirect('/doctor_login')  # Redirect to doctor login if not logged in

# Reject Appointment
@app.route('/reject_appointment/<int:appointment_id>', methods=['POST'])
def reject_appointment(appointment_id):
    if 'doctor_username' in session:
        cursor.execute("UPDATE appointments SET status = 'Rejected' WHERE id = %s", (appointment_id,))
        conn.commit()
        return redirect('/doctor_dashboard')  # Redirect back to the doctor dashboard
    return redirect('/doctor_login')  # Redirect to doctor login if not logged in

# Doctor Logout
@app.route('/doctor_logout')
def doctor_logout():
    session.pop('doctor_username', None)
    return redirect('/doctor_login')

# File Upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return 'File uploaded successfully'
    return render_template('upload.html')

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
