from __future__ import annotations

from .common import make_scenarios

PROCESS_NAMES = ['Patient Registration', 'Appointment Scheduling', 'Lab Test Ordering', 'Prescription Refill', 'Insurance Eligibility Check', 'Emergency Triage', 'Surgery Preparation', 'Discharge Planning', 'Referral Management', 'Medical Records Release', 'Chronic Care Follow Up', 'Vaccination Campaign', 'Telehealth Consultation', 'Prior Authorization', 'Radiology Exam Processing', 'Patient Billing', 'Clinical Trial Enrollment', 'Home Care Coordination', 'Medication Reconciliation', 'Incident Safety Review']
DATA_OBJECTS = ['Patient Chart', 'Lab Order', 'Insurance Card', 'Prescription', 'Consent Form', 'Discharge Summary']
DATA_STORES = ['Electronic Health Record', 'Scheduling System', 'Pharmacy System', 'Claims Platform']

SCENARIOS = make_scenarios("healthcare", PROCESS_NAMES, DATA_OBJECTS, DATA_STORES)
