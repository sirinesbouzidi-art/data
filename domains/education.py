from __future__ import annotations

from .common import make_scenarios

PROCESS_NAMES = ['Student Admission', 'Course Registration', 'Scholarship Review', 'Exam Scheduling', 'Grade Appeal', 'Library Account Setup', 'Internship Placement', 'Faculty Hiring', 'Curriculum Change Approval', 'Student Withdrawal', 'Transcript Request', 'Research Grant Review', 'Dormitory Assignment', 'Academic Probation Review', 'Online Class Setup', 'Tuition Payment Plan', 'Graduation Clearance', 'Special Accommodation Request', 'Alumni Event Registration', 'Study Abroad Application']
DATA_OBJECTS = ['Application Form', 'Enrollment Record', 'Transcript', 'Scholarship Essay', 'Exam Roster', 'Accommodation Plan']
DATA_STORES = ['Student Information System', 'Learning Management System', 'Admissions CRM', 'Finance Portal']

SCENARIOS = make_scenarios("education", PROCESS_NAMES, DATA_OBJECTS, DATA_STORES)
