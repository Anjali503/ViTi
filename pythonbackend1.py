import matplotlib.pyplot as plt

def display_bar_chart_day(categories, ideal_spend, actual_spend, month, day):
    # Create a bar chart comparing ideal vs actual spending for a specific day
    x = range(len(categories))
    
    plt.figure(figsize=(10, 5))
    plt.bar(x, ideal_spend, width=0.4, label='Ideal Daily Budget', align='center', color='lightblue')
    plt.bar(x, actual_spend, width=0.4, label='Actual Spend', align='edge', color='salmon')
    
    plt.xlabel('Categories')
    plt.ylabel('Amount Spent')
    plt.title(f'Ideal Daily Budget vs Actual Spending - {month} {day}')
    plt.xticks(x, categories, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    
    # Show the bar chart
    plt.show()

def get_ideal_spending(categories):
    ideal_spend_by_category = []
    for category in categories:
        ideal_spend = float(input(f"Enter your ideal spending for {category}: "))
        ideal_spend_by_category.append(ideal_spend)
    return ideal_spend_by_category

def get_actual_spending(categories, day):
    actual_spend_by_category = []
    for category in categories:
        actual_spend = float(input(f"Enter your actual spending for {category} on day {day}: "))
        actual_spend_by_category.append(actual_spend)
    return actual_spend_by_category

def get_days_in_month(month):
    # Adjust this function for the actual days in each month
    if month in ["April", "June", "September", "November"]:
        return 30
    elif month == "February":
        return 28  # Placeholder for leap years
    else:
        return 31

def main():
    # User Login Input
    reg_number = input("Enter your registration number: ")
    name = input("Enter your name: ")

    # Initialize data structure to hold monthly budgets and spends
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    
    budget_data = {month: {"daily_spends": {}, "monthly_budget": 0, "ideal_spend_by_category": []} for month in months}

    # Categories for input
    categories = ["Food", "Transport", "Personal Care", "Household Supplies", "Miscellaneous"]

    # Ask the user to input the starting month
    while True:
        start_month = input("\nEnter the month from which you want to start budgeting (e.g., January): ")
        if start_month in months:
            start_index = months.index(start_month)
            break
        else:
            print("Invalid month. Please enter a valid month name.")

    # Loop through the months starting from the user-specified month
    for month in months[start_index:]:
        print(f"\n--- {month} ---")

        # Take input for the total monthly budget
        monthly_budget = float(input(f"Enter your total budget for {month}: "))
        budget_data[month]["monthly_budget"] = monthly_budget

        # Input the daily budget for each category
        daily_budget_by_category = []
        print(f"\nEnter your daily budget for each category for {month}:")
        for category in categories:
            daily_budget = float(input(f"Enter daily budget for {category}: "))
            daily_budget_by_category.append(daily_budget)
        
        # Calculate the total daily budget
        total_daily_budget = sum(daily_budget_by_category)
        print(f"\nTotal daily budget for {month}: {total_daily_budget:.2f}")

        # Calculate ideal spending for each category for the month
        ideal_spend_by_category = [daily * get_days_in_month(month) for daily in daily_budget_by_category]
        budget_data[month]["ideal_spend_by_category"] = ideal_spend_by_category

        # Track total spending for the month
        total_spent_month = 0
        days_in_month = get_days_in_month(month)  # Get actual number of days in the month

        # Loop through each day of the month and track actual spending
        for day in range(1, days_in_month + 1):
            print(f"\n--- {month} {day} ---")

            # Actual spending input for each category for the day
            actual_spend_by_category = get_actual_spending(categories, day)
            budget_data[month]["daily_spends"].setdefault(day, [0] * len(categories))
            budget_data[month]["daily_spends"][day] = actual_spend_by_category

            # Calculate total actual spending for the day
            total_actual_spent_day = sum(actual_spend_by_category)
            total_spent_month += total_actual_spent_day

            # Debugging output
            print(f"Total actual spent today: {total_actual_spent_day:.2f}")

            # Daily savings or overexpenditure
            difference = total_actual_spent_day - total_daily_budget
            if difference < 0:
                print(f"\nDaily savings for day {day}: {-difference:.2f}")
            else:
                print(f"\nOverexpenditure for day {day}: {difference:.2f}")

            # Calculate remaining budget and suggest daily spending for remaining days
            remaining_days = days_in_month - day
            remaining_budget = monthly_budget - total_spent_month

            if remaining_days > 0:
                if remaining_budget < 0:
                    print("Warning: You have already exceeded your budget.")
                else:
                    suggested_spend_per_category = [
                        (remaining_budget / remaining_days) * (ideal / sum(ideal_spend_by_category))
                        for ideal in ideal_spend_by_category
                    ]
                    
                    print(f"To stay within your monthly budget, aim to spend the following amounts on each remaining day:")
                    for i, category in enumerate(categories):
                        print(f"{category}: {max(suggested_spend_per_category[i], 0):.2f} per day")  # Ensure no negative values

            # Display bar chart comparing ideal and actual spending for the day
            display_bar_chart_day(categories, daily_budget_by_category, actual_spend_by_category, month, day)

        # Calculate total savings or overboard at the end of the month
        total_savings_or_overboard = monthly_budget - total_spent_month

        # Display summary for the month
        print(f"\n--- Budget Summary for {month} ---")
        print(f"Total spent: {total_spent_month:.2f}")
        print(f"Total monthly budget: {monthly_budget:.2f}")

        # Display whether the user saved or overspent for the month
        if total_savings_or_overboard >= 0:
            print(f"Great! You saved {total_savings_or_overboard:.2f} this month.")
        else:
            print(f"You went overboard by {-total_savings_or_overboard:.2f} this month.")

if _name_ == "_main_":
    main()