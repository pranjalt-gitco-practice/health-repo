# Health Repo: Hospital Application Demo

A simple Python command-line example that demonstrates how to:

1. Admit a patient.
2. Assign a doctor.
3. Generate a bill from stay length, daily rate, and treatment charge.
4. Print a summary report for the patient.
5. Print the list of admitted patients.

The application stores data in memory only; patient records are lost when it exits.
It is an educational demo, not a production medical or billing system. Use fictional
sample data only. Do not enter real patient information.

## Requirements

- Python 3.10 or newer
- No third-party packages

## Run

```bash
python hospital.py
```

Follow the prompts for fictional patient details.

## Run tests

```bash
python -m unittest -v
```