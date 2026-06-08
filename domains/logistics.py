from __future__ import annotations

from .common import make_scenarios

PROCESS_NAMES = ['Freight Booking', 'Warehouse Receiving', 'Order Fulfillment', 'Last Mile Delivery', 'Customs Clearance', 'Return Merchandise Authorization', 'Fleet Maintenance', 'Route Optimization', 'Cold Chain Shipment', 'Supplier Pickup Scheduling', 'Inventory Cycle Count', 'Damaged Goods Claim', 'Cross Dock Transfer', 'Container Release', 'Hazardous Material Handling', 'Proof Of Delivery Capture', 'Carrier Invoice Audit', 'Shipment Tracking Exception', 'Yard Appointment', 'Emergency Replenishment']
DATA_OBJECTS = ['Bill Of Lading', 'Packing List', 'Delivery Note', 'Customs Declaration', 'Route Plan', 'Damage Report']
DATA_STORES = ['Warehouse Management System', 'Transportation Management System', 'Fleet System', 'Customs Portal']

SCENARIOS = make_scenarios("logistics", PROCESS_NAMES, DATA_OBJECTS, DATA_STORES)
