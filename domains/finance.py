from __future__ import annotations

from .common import make_scenarios

PROCESS_NAMES = ['Loan Approval', 'Invoice Processing', 'Expense Reimbursement', 'Vendor Payment', 'Budget Transfer', 'Credit Limit Review', 'Account Reconciliation', 'Purchase Order Approval', 'Tax Filing Preparation', 'Fraud Investigation', 'Refund Processing', 'Investment Account Opening', 'Mortgage Prequalification', 'Insurance Claim Payment', 'Collections Arrangement', 'Treasury Cash Forecast', 'Grant Disbursement', 'Subscription Billing', 'Financial Close', 'Audit Evidence Request']
DATA_OBJECTS = ['Invoice', 'Loan Application', 'Expense Receipt', 'Payment Batch', 'Budget Request', 'Audit Evidence']
DATA_STORES = ['Core Banking System', 'ERP Ledger', 'Payment Gateway', 'Risk Platform']

SCENARIOS = make_scenarios("finance", PROCESS_NAMES, DATA_OBJECTS, DATA_STORES)
