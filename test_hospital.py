"""Unit tests for the hospital admission demonstration."""

import unittest

from hospital import Hospital


class HospitalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.hospital = Hospital()
        self.patient = self.hospital.admit("Alex Example", 12, "Routine checkup")

    def test_admit_assigns_id_and_trims_fields(self) -> None:
        self.assertEqual(self.patient.patient_id, "P001")
        self.assertEqual(self.patient.name, "Alex Example")
        self.assertEqual(self.patient.diagnosis, "Routine checkup")

    def test_admit_rejects_empty_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "name cannot be empty"):
            self.hospital.admit("  ", 12, "Checkup")

    def test_admit_rejects_invalid_age(self) -> None:
        for age in (-1, 131, 12.5, True):
            with self.subTest(age=age):
                with self.assertRaisesRegex(ValueError, "age must be"):
                    self.hospital.admit("Alex Example", age, "Checkup")

    def test_assign_doctor(self) -> None:
        self.hospital.assign_doctor(self.patient.patient_id, "Dr. Rivera")
        self.assertEqual(self.patient.doctor, "Dr. Rivera")

    def test_assign_doctor_rejects_unknown_patient(self) -> None:
        with self.assertRaisesRegex(ValueError, "No patient found"):
            self.hospital.assign_doctor("P999", "Dr. Rivera")

    def test_generate_bill_and_report(self) -> None:
        bill = self.hospital.generate_bill(
            self.patient.patient_id,
            stay_days=3,
            daily_rate=125.0,
            treatment_charge=40.0,
        )
        self.hospital.assign_doctor(self.patient.patient_id, "Dr. Rivera")

        self.assertEqual(bill.total, 415.0)
        report = self.hospital.summary_report(self.patient.patient_id)
        self.assertIn("Doctor: Dr. Rivera", report)
        self.assertIn("Bill total: 415.00", report)

    def test_bill_rejects_invalid_stay_or_charges(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one"):
            self.hospital.generate_bill(self.patient.patient_id, 0)
        with self.assertRaisesRegex(ValueError, "finite, non-negative"):
            self.hospital.generate_bill(
                self.patient.patient_id, 1, treatment_charge=-1
            )
        with self.assertRaisesRegex(ValueError, "finite, non-negative"):
            self.hospital.generate_bill(
                self.patient.patient_id, 1, daily_rate=float("inf")
            )

    def test_patient_list_preserves_admission_order(self) -> None:
        second = self.hospital.admit("Jamie Example", 10, "Checkup")
        self.assertEqual(
            [patient.patient_id for patient in self.hospital.list_patients()],
            [self.patient.patient_id, second.patient_id],
        )


if __name__ == "__main__":
    unittest.main()
