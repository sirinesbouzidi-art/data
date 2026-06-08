from __future__ import annotations

from .common import make_scenarios

PROCESS_NAMES = ['Employee Onboarding', 'Candidate Screening', 'Leave Request Approval', 'Performance Review', 'Training Enrollment', 'Payroll Change Request', 'Employee Offboarding', 'Internal Transfer', 'Benefits Enrollment', 'Workplace Incident Report', 'Contract Renewal', 'Equipment Provisioning', 'Remote Work Approval', 'Promotion Review', 'Disciplinary Action', 'Recruitment Requisition', 'Timesheet Correction', 'Employee Data Update', 'Background Check', 'Exit Interview']
DATA_OBJECTS = ['Candidate Profile', 'Employment Contract', 'Leave Balance', 'Review Form', 'Training Certificate', 'Payroll Change Form']
DATA_STORES = ['HRIS', 'Applicant Tracking System', 'Payroll System', 'Learning Platform']

SCENARIOS = make_scenarios("hr", PROCESS_NAMES, DATA_OBJECTS, DATA_STORES)
