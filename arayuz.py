from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from hospital_system import ReservationSystem

# -----------------------------------------------------------------------------
# Sistem ve Örnek Veriler ------------------------------------------------------
# -----------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------
# Yardımcı Fonksiyonlar --------------------------------------------------------
# -----------------------------------------------------------------------------

def fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


def refresh_appointments() -> None:
    appt_list.delete(0, tk.END)
    for app in sorted(rs.appointments, key=lambda a: a.date_time):
        appt_list.insert(tk.END, f"{fmt(app.date_time)} | {app.doctor.name} | {app.patient.name}")


def refresh_availability(*_args) -> None:
    availability_list.delete(0, tk.END)
    doc_name = doctor_var.get()
    doc = rs.doctors.get(doc_name)
    if not doc:
        return
    slots = sorted(doc._available_slots)  # noqa: SLF001
    if not slots:
        availability_list.insert(tk.END, "Müsaitlik yok")
        return
    for dt in slots:
        availability_list.insert(tk.END, fmt(dt))


def fill_datetime(_event) -> None:
    sel = availability_list.curselection()
    if not sel:
        return
    ts = availability_list.get(sel[0])
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


def cancel_selected() -> None:
    sel = appt_list.curselection()
    if not sel:
        return
    line = appt_list.get(sel[0])
    try:
        ts, doctor_name, patient_name = [part.strip() for part in line.split("|")]
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")
    except ValueError:
        return

    matching = [p for p in rs.patients.values() if p.name == patient_name]
    if not matching:
        return
    tc = matching[0].tc
    try:
        rs.randevu_iptal(tc, dt)
    except ValueError as e:
        messagebox.showerror("İptal Hatası", str(e))
        return

    refresh_appointments()
    refresh_availability()

# -----------------------------------------------------------------------------
# Tkinter Arayüz ---------------------------------------------------------------
# -----------------------------------------------------------------------------
root = tk.Tk()
root.title("Hastane Randevu Sistemi")
root.resizable(False, False)

main = ttk.Frame(root, padding=10)
main.grid(row=0, column=0)

# ---------------- Hasta Bilgileri ----------------
patient_frame = ttk.LabelFrame(main, text="Hasta", padding=10)
patient_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

patient_name_var = tk.StringVar()
patient_tc_var = tk.StringVar()

ttk.Label(patient_frame, text="İsim:").grid(row=0, column=0, sticky="e")
name_entry = ttk.Entry(patient_frame, textvariable=patient_name_var, width=25)
name_entry.grid(row=0, column=1, sticky="w")

ttk.Label(patient_frame, text="TC:").grid(row=1, column=0, sticky="e")


def validate_tc(proposed: str) -> bool:
    """Sadece rakam ve en fazla 11 hane."""
    return (proposed.isdigit() and len(proposed) <= 11) or proposed == ""

vcmd = (root.register(validate_tc), "%P")


tc_entry = ttk.Entry(
    patient_frame,
    textvariable=patient_tc_var,
    width=25,
    validate="key",
    validatecommand=vcmd,
)
tc_entry.grid(row=1, column=1, sticky="w")

# ---------------- Randevu Bilgileri ----------------
appointment_frame = ttk.LabelFrame(main, text="Randevu", padding=10)
appointment_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

doctor_var = tk.StringVar(value=list(rs.doctors.keys())[0])

ttk.Label(appointment_frame, text="Doktor:").grid(row=0, column=0, sticky="e")

doctor_menu = ttk.OptionMenu(
    appointment_frame, doctor_var, doctor_var.get(), *rs.doctors.keys()
)

doctor_menu.grid(row=0, column=1, sticky="w")

doctor_var.trace_add("write", refresh_availability)

# Müsaitlik listesi
availability_list = tk.Listbox(appointment_frame, height=8, width=25)
availability_list.grid(row=1, column=0, columnspan=2, pady=4)
availability_list.bind("<<ListboxSelect>>", fill_datetime)

# Tarih alanı
datetime_var = tk.StringVar()

ttk.Label(appointment_frame, text="Tarih:").grid(row=2, column=0, sticky="e")

datetime_entry = ttk.Entry(
    appointment_frame, textvariable=datetime_var, width=25, state="readonly"
)
datetime_entry.grid(row=2, column=1, sticky="w")

# Butonlar
btn_frame = ttk.Frame(appointment_frame)
btn_frame.grid(row=3, column=0, columnspan=2, pady=5)

book_btn = ttk.Button(btn_frame, text="Randevu Al", command=book_appointment)
book_btn.grid(row=0, column=0, padx=5)

cancel_btn = ttk.Button(btn_frame, text="Randevu İptal", command=cancel_selected)
cancel_btn.grid(row=0, column=1, padx=5)

# ---------------- Aktif Randevular ----------------
list_frame = ttk.LabelFrame(main, text="Aktif Randevular", padding=10)
list_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

appt_list = tk.Listbox(list_frame, width=50)
appt_list.pack()

# İlk yükleme
refresh_appointments()
refresh_availability()

root.mainloop()
