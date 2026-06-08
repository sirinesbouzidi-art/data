from __future__ import annotations

from .common import make_scenarios

PROCESS_NAMES = ['New SIM Activation', 'Broadband Installation', 'Service Outage Resolution', 'Number Porting', 'Plan Upgrade', 'Roaming Enablement', 'Device Financing', 'Network Capacity Upgrade', 'Customer Complaint Handling', 'Prepaid Recharge Failure', 'Enterprise Circuit Provisioning', 'Fraudulent Usage Review', 'Router Replacement', 'Billing Dispute', 'Field Technician Dispatch', 'Voicemail Setup', 'IoT Device Onboarding', 'Fiber Feasibility Check', 'Service Cancellation', 'Signal Quality Optimization']
DATA_OBJECTS = ['Service Order', 'Customer Contract', 'Network Ticket', 'SIM Profile', 'Porting Form', 'Usage Record']
DATA_STORES = ['CRM', 'Billing Platform', 'Network Inventory', 'Provisioning System']

SCENARIOS = make_scenarios("telecom", PROCESS_NAMES, DATA_OBJECTS, DATA_STORES)
