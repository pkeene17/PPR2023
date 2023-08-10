batchFiller.py is a python script designed to populate batch numbers of payments using acipayments inc

assumptions:
you're using the custom report generated from acipayments
the data file you're writting to is Online Payment Logs from sharepoint's event-permitting-app/checklogs folder
both files must be CSVs

How to generate the custom report:
Tab: General
	Transaction Type: Settled Transactions(Details)
Tab: Advance Filters
	Select Field: Transaction Types
	Select Operator: Is
	Select Value: Payments
Tab: Output Columns
	Batch Close Date
	Batch #
	Settlement Date
	Transaction Date & Time
	Account Type
	Confirmation #
	First Name
	Last/Business Name
	Base Payment Amount
	Consumer Fee
	Total Amount
You can add more but these are the essentials

When you run it use Transaction time as the date filter, then choose the start and end dates you want.
Generally, you want to start a few days before the posting date of the first batch youre looking for

You'll get much better results if you use a narrow (2-4 days) date range. 
Larger ranges will still work (and you may have to for some batches), but you will have to do more manual validation

You will need to edit the "folder" variable if you're not Paul and not running on the desktop
You shouldn't need to touch anything else
