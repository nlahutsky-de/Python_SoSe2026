# Variant 4. Personal finance analyzer
## Team Members:
Natalie Christine Lahutsky, 0523641, Civil Systems Engineering

Seychelle Ann Dagus, 0508078, Civil Systems Engineering

Tilman Lindvogt, 608371, Humboldt University Economics

Konstantin Krüger, 398013, Produktionstechnik

## Description:
Our Peronal Finance Analyzer is a Python desktop application developed using Tkinter.
The project demonstrates object-oriented programming principles, data management, and graphical user interface (GUI) development using Python.
It helps users record and manage their financila transactions by tracking both income and expenses.

The application allows users to:
- Add, edit, and delete transactions
- Automatically categorize expenses based on keywords
- Assign custom categories manually
- View total income, expenses, and savings
- Display spending summaries by category
- Display financial summaries over time
- Visualize financial data through simple charts

## Project Structure

.
├── main.py             # Starts the application
├── gui.py              # Tkinter graphical user interface
├── logic.py            # Business logic and transaction management
├── models.py           # Transaction class
├── utils.py            # Functions for input validation
└── README.md

## Getting Started:
1. Download or clone the project.
2. Make sure the following files are in the same folder:
    - main.py
    - gui.py
    - logic.py
    - models.py

3. Run the application using main.py

## How to Use
1. Enter the transaction information:
    - Transaction Type (Income or Expense)
    - Description
    - Amount
    - Date
    - Category (or Auto-categorize)
2. Click **Add Transaction**
3. Select a transaction to edit or delete it.
4. View the **Categories Insights** Tab to see the Analytics on which category has the highest expense.
5. View the **Timeline Summary** Tab to see the monthly summary of the inflow, outflow, and net savings.

## Limitations/Bugs



## Future improvements
- Save and load data using CSV or JSON files
- Add a budgeting features
- Add search and filtering options
