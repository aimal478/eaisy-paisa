# Install required packages (if not already installed)
!pip install ipywidgets pandas --quiet

# Imports
import pandas as pd
from IPython.display import display, clear_output
import ipywidgets as widgets
from datetime import datetime

# Create or load CSV
file_name = 'easypaisa_daily_record.csv'

# Load existing data or create new DataFrame
try:
    df = pd.read_csv(file_name)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Date', 'Total Sale', 'Total Expense', 'Profit'])

# Widgets for input
date_picker = widgets.DatePicker(description='Date', value=datetime.today().date())
sale_input = widgets.FloatText(description='Sale Rs', value=0.0)
expense_input = widgets.FloatText(description='Expense Rs', value=0.0)
submit_btn = widgets.Button(description='Add Record', button_style='success')
output = widgets.Output()

# Function to add record
def on_submit_clicked(b):
    with output:
        clear_output()
        date_val = date_picker.value.strftime('%Y-%m-%d')
        sale = sale_input.value
        expense = expense_input.value
        profit = sale - expense

        new_row = {'Date': date_val, 'Total Sale': sale, 'Total Expense': expense, 'Profit': profit}
        global df
        df = df.append(new_row, ignore_index=True)
        df.to_csv(file_name, index=False)
        print("✅ Record Added Successfully!")
        display(df.tail())

submit_btn.on_click(on_submit_clicked)

# Show widgets
display(widgets.VBox([date_picker, sale_input, expense_input, submit_btn, output]))
