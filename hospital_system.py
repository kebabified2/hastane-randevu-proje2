from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Set


class Patient:
    """Hasta bilgisi ve randevu geçmişini tutar."""

    def __init__(self, name: str, tc: str) -> None:
        self.name: str = name
        self.tc: str = tc
        self.history: List[Appointment] = []

    def add_appointment(self, appointment: "Appointment") -> None:
        self.history.append(appointment)

    def __repr__(self) -> str:  # pragma: no cover
        return f"Patient({self.name}, TC={self.tc})"


class Doctor:
    """Doktor bilgisi ve müsaitlik durumunu yönetir."""

    def __init__(self, name: str, speciality: str) -> None:
        self.name: str = name
        self.speciality: str = speciality
        self._available_slots: Set[datetime] = set()

    # ---- Müsaitlik Yönetimi -------------------------------------------------
    def add_availability(self, date_time: datetime) -> None:
        self._available_slots.add(date_time)

    def remove_availability(self, date_time: datetime) -> None:
        self._available_slots.discard(date_time)

    def is_available(self, date_time: datetime) -> bool:
        return date_time in self._available_slots

    # ------------------------------------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover
        return f"Dr. {self.name} ({self.speciality})"


class Appointment:
    """Hasta ile Doktor arasındaki randevuyu temsil eder."""

    def __init__(self, patient: Patient, doctor: Doctor, date_time: datetime):
        self.patient: Patient = patient
        self.doctor: Doctor = doctor
        self.date_time: datetime = date_time

    def __repr__(self) -> str:  # pragma: no cover
        ts = self.date_time.strftime("%Y-%m-%d %H:%M")
        return f"{ts} | {self.doctor} ↔ {self.patient.name}"


class ReservationSystem:
    """Hasta, Doktor ve Randevuların tutulduğu ana yönetim sınıfı."""

    def __init__(self) -> None:
        self.patients: Dict[str, Patient] = {}
        self.doctors: Dict[str, Doctor] = {}
        self.appointments: List[Appointment] = []

    # ---- Kayıt İşlemleri ----------------------------------------------------
    def add_patient(self, name: str, tc: str) -> Patient:
        if tc not in self.patients:
            self.patients[tc] = Patient(name, tc)
        return self.patients[tc]

    def add_doctor(self, name: str, speciality: str) -> Doctor:
        if name not in self.doctors:
            self.doctors[name] = Doctor(name, speciality)
        return self.doctors[name]

    # ---- Randevu İşlemleri --------------------------------------------------
    def randevu_al(self, tc: str, doctor_name: str, date_time: datetime) -> Appointment:
        """Yeni randevu oluşturur."""
        if tc not in self.patients:
            raise ValueError("Hasta sistemde bulunamadı.")
        if doctor_name not in self.doctors:
            raise ValueError("Doktor sistemde bulunamadı.")

        patient = self.patients[tc]
        doctor = self.doctors[doctor_name]

        if not doctor.is_available(date_time):
            raise ValueError("Seçilen tarihte doktor müsait değil.")

        # Çakışma kontrolü
        for app in self.appointments:
            if app.date_time == date_time and (
                app.patient.tc == tc or app.doctor.name == doctor_name
            ):
                raise ValueError("Seçilen saat dolu.")

        appointment = Appointment(patient, doctor, date_time)
        self.appointments.append(appointment)

        patient.add_appointment(appointment)
        doctor.remove_availability(date_time)
        return appointment

    def randevu_iptal(self, tc: str, date_time: datetime) -> Appointment:
        """Belirtilen hastaya ait randevuyu iptal eder."""
        for app in self.appointments:
            if app.patient.tc == tc and app.date_time == date_time:
                self.appointments.remove(app)
                app.doctor.add_availability(date_time)
                app.patient.history.remove(app)
                return app
        raise ValueError("Randevu bulunamadı.")

    def list_appointments(self) -> None:
        for a in sorted(self.appointments, key=lambda x: x.date_time):
            print(a)

# Basit kullanım örneği (python hospital_system.py) ---------------------------

if __name__ == "__main__":
    rs = ReservationSystem()

    # ---------------- Doktor 1: Ahmet Yılmaz --------------------------------
    ahmet = rs.add_doctor("Ahmet Yılmaz", "Kardiyoloji")
    ahmet_slots = [
        datetime(2025, 5, 1, 10, 0),  # mevcut
        datetime(2025, 5, 1, 11, 0),
        datetime(2025, 5, 3, 10, 0),
        datetime(2025, 5, 3, 11, 0),
        datetime(2025, 5, 4, 10, 0),
        # iki yeni slot ↓
        datetime(2025, 5, 5, 10, 0),
        datetime(2025, 5, 6, 10, 0),
    ]
    for slot in ahmet_slots:
        ahmet.add_availability(slot)

    # ---------------- Doktor 2: Mehmet Kara ----------------------------------
    mehmet = rs.add_doctor("Mehmet Kara", "Dermatoloji")
    mehmet_slots = [
        datetime(2025, 5, 2, 9, 0),
        datetime(2025, 5, 2, 10, 0),
        datetime(2025, 5, 4, 9, 0),
        datetime(2025, 5, 4, 10, 0),
        datetime(2025, 5, 5, 9, 0),
        # iki yeni slot ↓
        datetime(2025, 5, 6, 9, 0),
        datetime(2025, 5, 7, 9, 0),
    ]
    for slot in mehmet_slots:
        mehmet.add_availability(slot)

    # ---------------- Doktor 3: Aylin Şahin ----------------------------------
    aylin = rs.add_doctor("Aylin Şahin", "Nöroloji")
    aylin_slots = [
        datetime(2025, 5, 1, 14, 0),
        datetime(2025, 5, 3, 14, 0),
        datetime(2025, 5, 3, 15, 0),
        datetime(2025, 5, 4, 14, 0),
        # iki yeni slot ↓
        datetime(2025, 5, 5, 14, 0),
        datetime(2025, 5, 6, 14, 0),
    ]
    for slot in aylin_slots:
        aylin.add_availability(slot)

    # ---------------- Örnek Hasta ve Randevu ---------------------------------
    hasta = rs.add_patient("Ayşe Demir", "12345678901")
    rs.randevu_al(hasta.tc, ahmet.name, ahmet_slots[0])

    # Durum çıktısı
    print("--- Aktif Randevular ---")
    rs.list_appointments()
