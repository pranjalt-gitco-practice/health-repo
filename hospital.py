"""Simple in-memory hospital admission and billing demonstration."""

from dataclasses import dataclass
import math


@dataclass
class Bill:
    """Breakdown of a patient's hospital charges."""

    stay_days: int
    daily_rate: float
    treatment_charge: float

    @property
    def total(self) -> float:
        """Return the total amount due."""
        return self.stay_days * self.daily_rate + self.treatment_charge


@dataclass
class Patient:
    """Basic details maintained for one admitted patient."""

    patient_id: str
    name: str
    age: int
    diagnosis: str
    doctor: str | None = None
    bill: Bill | None = None


class Hospital:
    """Manage patient admissions, doctors, bills, and reports in memory."""

    def __init__(self) -> None:
        self._patients: list[Patient] = []

    def admit(self, name: str, age: int, diagnosis: str) -> Patient:
        """Admit a patient and return their newly created record."""
        name = name.strip()
        diagnosis = diagnosis.strip()
        if not name:
            raise ValueError("Patient name cannot be empty.")
        if not isinstance(age, int) or isinstance(age, bool) or not 0 <= age <= 130:
            raise ValueError("Patient age must be a whole number from 0 to 130.")
        if not diagnosis:
            raise ValueError("Diagnosis cannot be empty.")

        patient = Patient(
            patient_id=f"P{len(self._patients) + 1:03d}",
            name=name,
            age=age,
            diagnosis=diagnosis,
        )
        self._patients.append(patient)
        return patient

    def assign_doctor(self, patient_id: str, doctor: str) -> None:
        """Assign a doctor to an admitted patient."""
        patient = self._find_patient(patient_id)
        doctor = doctor.strip()
        if not doctor:
            raise ValueError("Doctor name cannot be empty.")
        patient.doctor = doctor

    def generate_bill(
        self,
        patient_id: str,
        stay_days: int,
        daily_rate: float = 100.0,
        treatment_charge: float = 0.0,
    ) -> Bill:
        """Create and save a bill from stay length and provided charges."""
        patient = self._find_patient(patient_id)
        if not isinstance(stay_days, int) or isinstance(stay_days, bool) or stay_days < 1:
            raise ValueError("Stay must be at least one whole day.")
        if (
            not math.isfinite(daily_rate)
            or not math.isfinite(treatment_charge)
            or daily_rate < 0
            or treatment_charge < 0
        ):
            raise ValueError("Charges must be finite, non-negative amounts.")

        bill = Bill(stay_days, float(daily_rate), float(treatment_charge))
        patient.bill = bill
        return bill

    def summary_report(self, patient_id: str) -> str:
        """Return a readable report for one admitted patient."""
        patient = self._find_patient(patient_id)
        doctor = patient.doctor or "Not assigned"
        bill_total = f"{patient.bill.total:.2f}" if patient.bill else "Not generated"
        return (
            f"Patient summary\n"
            f"ID: {patient.patient_id}\n"
            f"Name: {patient.name}\n"
            f"Age: {patient.age}\n"
            f"Diagnosis: {patient.diagnosis}\n"
            f"Doctor: {doctor}\n"
            f"Bill total: {bill_total}"
        )

    def list_patients(self) -> list[Patient]:
        """Return all admitted patients in admission order."""
        return list(self._patients)

    def _find_patient(self, patient_id: str) -> Patient:
        for patient in self._patients:
            if patient.patient_id == patient_id:
                return patient
        raise ValueError(f"No patient found with ID {patient_id!r}.")


def main() -> None:
    """Run a single-patient demonstration through the requested workflow."""
    hospital = Hospital()
    print("Hospital patient admission demo (use fictional data only).")

    try:
        patient = hospital.admit(
            input("Patient name: "),
            int(input("Patient age: ")),
            input("Diagnosis: "),
        )
        hospital.assign_doctor(patient.patient_id, input("Doctor name: "))
        bill = hospital.generate_bill(
            patient.patient_id,
            int(input("Stay length in days: ")),
            float(input("Daily rate: ")),
            float(input("Treatment charge: ")),
        )
    except (ValueError, EOFError) as error:
        print(f"Could not complete admission: {error}")
        return

    print(f"\nBill total: {bill.total:.2f}\n")
    print(hospital.summary_report(patient.patient_id))
    print("\nPatient list:")
    for admitted_patient in hospital.list_patients():
        print(f"{admitted_patient.patient_id}: {admitted_patient.name}")


if __name__ == "__main__":
    main()
