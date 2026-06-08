from __future__ import annotations

from .common import make_scenarios

PROCESS_NAMES = ['Production Order Release', 'Quality Inspection', 'Machine Maintenance', 'Material Requirement Planning', 'Supplier Nonconformance', 'Engineering Change Request', 'Batch Record Review', 'Tool Calibration', 'Work Order Scheduling', 'Safety Permit Approval', 'Scrap Disposal', 'Packaging Line Setup', 'Product Recall Handling', 'Prototype Build', 'Capacity Planning', 'Component Traceability', 'Finished Goods Transfer', 'Shift Handover', 'Preventive Maintenance', 'Deviation Investigation']
DATA_OBJECTS = ['Work Order', 'Inspection Record', 'Maintenance Log', 'Batch Record', 'Change Request', 'Safety Checklist']
DATA_STORES = ['Manufacturing Execution System', 'ERP Inventory', 'Quality Management System', 'Maintenance System']

SCENARIOS = make_scenarios("manufacturing", PROCESS_NAMES, DATA_OBJECTS, DATA_STORES)
