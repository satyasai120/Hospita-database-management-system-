import sqlite3

# Connect to database (auto creates file)
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    specialization TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER,
    patient_id INTEGER,
    appointment_date TEXT,
    diagnosis TEXT,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
)
""")

conn.commit()

# Functions
def add_doctor():
    name = input("Doctor Name: ")
    spec = input("Specialization: ")
    phone = input("Phone: ")

    cursor.execute(
        "INSERT INTO doctors (name, specialization, phone) VALUES (?, ?, ?)",
        (name, spec, phone)
    )
    conn.commit()
    print("✅ Doctor added successfully")

def add_patient():
    name = input("Patient Name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    phone = input("Phone: ")

    cursor.execute(
        "INSERT INTO patients (name, age, gender, phone) VALUES (?, ?, ?, ?)",
        (name, age, gender, phone)
    )
    conn.commit()
    print("✅ Patient registered successfully")

def book_appointment():
    doctor_id = int(input("Doctor ID: "))
    patient_id = int(input("Patient ID: "))
    date = input("Appointment Date (YYYY-MM-DD): ")

    cursor.execute(
        "INSERT INTO appointments (doctor_id, patient_id, appointment_date) VALUES (?, ?, ?)",
        (doctor_id, patient_id, date)
    )
    conn.commit()
    print("✅ Appointment booked")

def view_appointments():
    cursor.execute("""
    SELECT a.appointment_id, d.name, p.name, a.appointment_date
    FROM appointments a
    JOIN doctors d ON a.doctor_id = d.doctor_id
    JOIN patients p ON a.patient_id = p.patient_id
    """)

    rows = cursor.fetchall()
    print("\nAppointments:")
    for row in rows:
        print(row)

# Menu
while True:
    print("\n--- Hospital Management System ---")
    print("1. Add Doctor")
    print("2. Add Patient")
    print("3. Book Appointment")
    print("4. View Appointments")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_doctor()
    elif choice == "2":
        add_patient()
    elif choice == "3":
        book_appointment()
    elif choice == "4":
        view_appointments()
    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("❌ Invalid choice")

conn.close()