from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from hospital_system import ReservationSystem


# ---------------------- Sistem ----------------------
rs = ReservationSystem()

# ---------------- Doktor 1: Ahmet Yılmaz ------------------------------------
ahmet = rs.add_doctor("Ahmet Yılmaz", "Kardiyoloji")
for dt in [
    datetime(2025, 5, 1, 10, 0),
    datetime(2025, 5, 1, 11, 0),
    datetime(2025, 5, 3, 10, 0),
    datetime(2025, 5, 3, 11, 0),
    datetime(2025, 5, 4, 10, 0),
    datetime(2025, 5, 5, 10, 0),
    datetime(2025, 5, 6, 10, 0),
]:
    ahmet.add_availability(dt)

# ---------------- Doktor 2: Mehmet Kara -------------------------------------
mehmet = rs.add_doctor("Mehmet Kara", "Dermatoloji")
for dt in [
    datetime(2025, 5, 2, 9, 0),
    datetime(2025, 5, 2, 10, 0),
    datetime(2025, 5, 4, 9, 0),
    datetime(2025, 5, 4, 10, 0),
    datetime(2025, 5, 5, 9, 0),
    datetime(2025, 5, 6, 9, 0),
    datetime(2025, 5, 7, 9, 0),
]:
    mehmet.add_availability(dt)

# ---------------- Doktor 3: Aylin Şahin -------------------------------------
aylin = rs.add_doctor("Aylin Şahin", "Nöroloji")
for dt in [
    datetime(2025, 5, 1, 14, 0),
    datetime(2025, 5, 3, 14, 0),
    datetime(2025, 5, 3, 15, 0),
    datetime(2025, 5, 4, 14, 0),
    datetime(2025, 5, 5, 14, 0),
    datetime(2025, 5, 6, 14, 0),
]:
    aylin.add_availability(dt)


# ---------------------- Yardımcı ----------------------
def fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


# ---------------------- Tk Arayüz ----------------------
root = tk.Tk()
root.title("Hastane Randevu Sistemi")
root.geometry("660x600")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TEntry", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))
style.configure("TCombobox", font=("Segoe UI", 10))
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))

main = ttk.Frame(root, padding=10)
main.pack(fill="both", expand=True)

# ---------------- Hasta Bilgileri ----------------
patient_frame = ttk.LabelFrame(main, text="Hasta", padding=10)
patient_frame.pack(fill="x", padx=5, pady=5)

patient_name_var = tk.StringVar()
patient_tc_var = tk.StringVar()

ttk.Label(patient_frame, text="İsim").grid(row=0, column=0, sticky="e", pady=2, padx=2)
ttk.Entry(patient_frame, textvariable=patient_name_var, width=30).grid(
    row=0, column=1, sticky="w", pady=2, padx=2
)

ttk.Label(patient_frame, text="TC").grid(row=1, column=0, sticky="e", pady=2, padx=2)


def validate_tc(proposed: str) -> bool:
    return (proposed.isdigit() and len(proposed) <= 11) or proposed == ""


vcmd = (root.register(validate_tc), "%P")
ttk.Entry(
    patient_frame,
    textvariable=patient_tc_var,
    validate="key",
    validatecommand=vcmd,
    width=30,
).grid(row=1, column=1, sticky="w", pady=2, padx=2)

# ---------------- Randevu Bilgileri ----------------
appointment_frame = ttk.LabelFrame(main, text="Randevu", padding=10)
appointment_frame.pack(fill="x", padx=5, pady=5)

doctor_var = tk.StringVar(value=list(rs.doctors.keys())[0])

ttk.Label(appointment_frame, text="Doktor").grid(
    row=0, column=0, sticky="e", pady=2, padx=2
)
doctor_cb = ttk.Combobox(
    appointment_frame,
    textvariable=doctor_var,
    values=list(rs.doctors.keys()),
    state="readonly",
    width=28,
)
doctor_cb.grid(row=0, column=1, sticky="w", pady=2, padx=2)

# Müsaitlik Listesi
availability_lb = tk.Listbox(appointment_frame, height=6, width=35, exportselection=False)
availability_lb.grid(row=1, column=0, columnspan=2, pady=4, padx=2, sticky="nsew")

datetime_var = tk.StringVar()

ttk.Label(appointment_frame, text="Tarih").grid(
    row=2, column=0, sticky="e", pady=2, padx=2
)
ttk.Entry(
    appointment_frame, textvariable=datetime_var, state="readonly", width=30
).grid(row=2, column=1, sticky="w", pady=2, padx=2)

# Butonlar
btn_container = ttk.Frame(appointment_frame)
btn_container.grid(row=3, column=0, columnspan=2, pady=5)

book_btn = ttk.Button(btn_container, text="Randevu Al")
book_btn.grid(row=0, column=0, padx=5)

cancel_btn = ttk.Button(btn_container, text="Randevu İptal")
cancel_btn.grid(row=0, column=1, padx=5)

# ---------------- Aktif Randevular ----------------
list_frame = ttk.LabelFrame(main, text="Aktif Randevular", padding=10)
list_frame.pack(fill="both", expand=True, padx=5, pady=5)

appt_tree = ttk.Treeview(
    list_frame,
    columns=("dt", "doc", "pat"),
    show="headings",
    height=10,
    selectmode="browse",
)
appt_tree.heading("dt", text="Tarih")
appt_tree.heading("doc", text="Doktor")
appt_tree.heading("pat", text="Hasta")
appt_tree.column("dt", width=160, anchor="center")
appt_tree.column("doc", width=160, anchor="w")
appt_tree.column("pat", width=160, anchor="w")
appt_tree.pack(fill="both", expand=True)

appointments_by_iid: dict[str, object] = {}


# ---------------- Fonksiyonlar ----------------
def refresh_appointments() -> None:
    for row in appt_tree.get_children():
        appt_tree.delete(row)
    appointments_by_iid.clear()
    for app in sorted(rs.appointments, key=lambda a: a.date_time):
        iid = str(id(app))
        appt_tree.insert(
            "", "end", iid=iid, values=(fmt(app.date_time), app.doctor.name, app.patient.name)
        )
        appointments_by_iid[iid] = app


def refresh_availability(*_args) -> None:
    availability_lb.delete(0, tk.END)
    doc = rs.doctors.get(doctor_var.get())
    if not doc:
        return
    slots = sorted(doc._available_slots)  # noqa: SLF001
    if not slots:
        availability_lb.insert(tk.END, "Müsaitlik yok")
        return
    for dt in slots:
        availability_lb.insert(tk.END, fmt(dt))


def fill_datetime(_event) -> None:
    sel = availability_lb.curselection()
    if not sel:
        return
    ts = availability_lb.get(sel[0])
    if ts == "Müsaitlik yok":
        return
    datetime_var.set(ts)


def book_appointment() -> None:
    name = patient_name_var.get().strip()
    tc = patient_tc_var.get().strip()
    doctor_name = doctor_var.get().strip()
    dt_str = datetime_var.get().strip()

    if not (name and tc and doctor_name and dt_str):
        messagebox.showwarning("Eksik Bilgi", "Tüm alanları doldurun.")
        return

    if len(tc) != 11:
        messagebox.showwarning("TC Hatası", "TC 11 haneli olmalı.")
        return

    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showerror("Tarih Hatası", "Tarih formatı YYYY-MM-DD HH:MM olmalı.")
        return

    rs.add_patient(name, tc)
    try:
        rs.randevu_al(tc, doctor_name, dt)
    except ValueError as e:
        messagebox.showerror("Randevu Hatası", str(e))
        return

    refresh_appointments()
    refresh_availability()
    datetime_var.set("")


def cancel_selected() -> None:
    selected = appt_tree.selection()
    if not selected:
        return
    iid = selected[0]
    app = appointments_by_iid.get(iid)
    if not app:
        return
    try:
        rs.randevu_iptal(app.patient.tc, app.date_time)
    except ValueError as e:
        messagebox.showerror("İptal Hatası", str(e))
        return

    refresh_appointments()
    refresh_availability()


# ---------------- Bağlantılar ----------------
doctor_cb.bind("<<ComboboxSelected>>", refresh_availability)
availability_lb.bind("<<ListboxSelect>>", fill_datetime)
book_btn.configure(command=book_appointment)
cancel_btn.configure(command=cancel_selected)

# ---------------- İlk Yükleme ----------------
refresh_appointments()
refresh_availability()

root.mainloop()
