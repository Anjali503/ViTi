from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64
import mysql.connector

app = Flask(__name__)

# Categories for input
categories = ["Food", "Transport", "Personal Care", "Household Supplies", "Miscellaneous"]

# MySQL Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="shubhangi14",
    database="personal_finance_db"  # Replace with your actual database name
)

cursor = db.cursor()

# Create a table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS budget_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reg_number VARCHAR(255),
    name VARCHAR(255),
    month VARCHAR(255),
    daily_budget FLOAT,
    actual_spend FLOAT,
    total_daily_budget FLOAT,
    total_actual_spent_day FLOAT,
    daily_savings FLOAT
)''')

def get_days_in_month(month):
    if month in ["April", "June", "September", "November"]:
        return 30
    elif month == "February":
        return 28  # Adjust for leap years if needed
    else:
        return 31

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Capture data from the form
    reg_number = request.form['regNo']
    name = request.form['name']
    month = request.form['month']
    
    daily_budget_by_category = [float(request.form.get(f"daily_budget_{i}")) for i in range(len(categories))]
    actual_spend_by_category = [float(request.form.get(f"actual_spend_{i}")) for i in range(len(categories))]
    
    # Get daily and total spending
    total_daily_budget = sum(daily_budget_by_category)
    total_actual_spent_day = sum(actual_spend_by_category)
    
    # Daily savings or overexpenditure
    difference = total_actual_spent_day - total_daily_budget
    daily_savings = max(-difference, 0)  # Only show positive savings

    # Remaining days and suggested spending per category
    days_in_month = get_days_in_month(month)
    remaining_days = days_in_month - 1  # Assuming data is for the first day
    remaining_budget = total_daily_budget * remaining_days - total_actual_spent_day
    
    if remaining_days > 0:
        suggested_spend_per_category = [
            (remaining_budget / remaining_days) * (daily / total_daily_budget)
            for daily in daily_budget_by_category
        ]
    else:
        suggested_spend_per_category = [0] * len(categories)
    
    # Store the data in MySQL database
    cursor.execute('''
        INSERT INTO budget_data (reg_number, name, month, daily_budget, actual_spend, total_daily_budget, total_actual_spent_day, daily_savings)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (reg_number, name, month, total_daily_budget, total_actual_spent_day, total_daily_budget, total_actual_spent_day, daily_savings))
    
    db.commit()  # Save the changes to the database

    # Generate the bar chart
    x = range(len(categories))
    plt.figure(figsize=(10, 5))
    plt.bar(x, daily_budget_by_category, width=0.4, label='Ideal Daily Budget', align='center', color='lightblue')
    plt.bar(x, actual_spend_by_category, width=0.4, label='Actual Spend', align='edge', color='salmon')
    plt.xlabel('Categories')
    plt.ylabel('Amount Spent')
    plt.title(f'Ideal Daily Budget vs Actual Spending - {month.capitalize()} 1')
    plt.xticks(x, categories, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    # Save the plot to a string buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()

    # Pass values back to the template for rendering
    return render_template('result.html', daily_budget_by_category=daily_budget_by_category,
                           total_actual_spent_day=total_actual_spent_day,
                           daily_savings=daily_savings,
                           suggested_spend_per_category=suggested_spend_per_category,
                           chart_url=chart_url)

if __name__ == '_main_':
    app.run(debug=True)