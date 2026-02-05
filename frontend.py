import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()


# ---------------- FUNCTIONS ----------------

def add_doctor():
    name = d_name.get()
    spec = d_spec.get()

    if not name or not spec:
        messagebox.showerror("Error", "Fill all fields")
        return

    cursor.execute("INSERT INTO doctors(name, specialization) VALUES (?,?)", (name, spec))
    conn.commit()

    messagebox.showinfo("Success", "Doctor Added")
    d_name.delete(0, tk.END)
    d_spec.delete(0, tk.END)


def add_patient():
    name = p_name.get()
    age = p_age.get()

    cursor.execute("INSERT INTO patients(name, age) VALUES (?,?)", (name, age))
    conn.commit()

    messagebox.showinfo("Success", "Patient Added")
    p_name.delete(0, tk.END)
    p_age.delete(0, tk.END)


def book_appointment():
    pid = a_pid.get()
    did = a_did.get()
    date = a_date.get()

    cursor.execute(
        "INSERT INTO appointments(patient_id, doctor_id, date) VALUES (?,?,?)",
        (pid, did, date)
    )
    conn.commit()

    messagebox.showinfo("Success", "Appointment Booked")


def view_appointments():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("""
        SELECT a.id, p.name, d.name, a.date
        FROM appointments a
        JOIN patients p ON p.id = a.patient_id
        JOIN doctors d ON d.id = a.doctor_id
    """)

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)


# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("🏥 Hospital Management System")
root.geometry("800x500")
root.configure(bg="#f4f6f8")

style = ttk.Style()
style.theme_use("clam")


# ---------------- NOTEBOOK (Tabs) ----------------
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)


# =================================================
# TAB 1 → DOCTOR
# =================================================
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Add Doctor")

ttk.Label(tab1, text="Doctor Name").grid(row=0, column=0, pady=10, padx=10)
d_name = ttk.Entry(tab1, width=30)
d_name.grid(row=0, column=1)

ttk.Label(tab1, text="Specialization").grid(row=1, column=0, pady=10)
d_spec = ttk.Entry(tab1, width=30)
d_spec.grid(row=1, column=1)

ttk.Button(tab1, text="Add Doctor", command=add_doctor).grid(row=2, column=1, pady=20)


# =================================================
# TAB 2 → PATIENT
# =================================================
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Add Patient")

ttk.Label(tab2, text="Patient Name").grid(row=0, column=0, pady=10)
p_name = ttk.Entry(tab2, width=30)
p_name.grid(row=0, column=1)

ttk.Label(tab2, text="Age").grid(row=1, column=0, pady=10)
p_age = ttk.Entry(tab2, width=30)
p_age.grid(row=1, column=1)

ttk.Button(tab2, text="Add Patient", command=add_patient).grid(row=2, column=1, pady=20)


# =================================================
# TAB 3 → APPOINTMENT
# =================================================
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Book Appointment")

ttk.Label(tab3, text="Patient ID").grid(row=0, column=0, pady=10)
a_pid = ttk.Entry(tab3)
a_pid.grid(row=0, column=1)

ttk.Label(tab3, text="Doctor ID").grid(row=1, column=0)
a_did = ttk.Entry(tab3)
a_did.grid(row=1, column=1)

ttk.Label(tab3, text="Date (YYYY-MM-DD)").grid(row=2, column=0)
a_date = ttk.Entry(tab3)
a_date.grid(row=2, column=1)

ttk.Button(tab3, text="Book Appointment", command=book_appointment).grid(row=3, column=1, pady=20)


# =================================================
# TAB 4 → VIEW APPOINTMENTS
# =================================================
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="View Appointments")

ttk.Button(tab4, text="Refresh", command=view_appointments).pack(pady=5)

columns = ("ID", "Patient", "Doctor", "Date")

tree = ttk.Treeview(tab4, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True, padx=10, pady=10)


# ---------------- RUN ----------------
root.mainloop()
conn.close()