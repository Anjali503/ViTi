import matplotlib.pyplot as plt

def display_bar_chart_day(categories, ideal_spend, actual_spend, month, day):
    # Create a bar chart comparing ideal vs actual spending for a specific day
    x = range(len(categories))
    
    plt.figure(figsize=(10, 5))
    plt.bar(x, ideal_spend, width=0.4, label='Ideal Spend', align='center', color='lightblue')
    plt.bar(x, actual_spend, width=0.4, label='Actual Spend', align='edge', color='salmon')
    
    plt.xlabel('Categories')
    plt.ylabel('Amount Spent')
    plt.title(f'Ideal vs Actual Spending - {month} {day}')
    plt.xticks(x, categories, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    
    # Show the bar chart
    plt.show()

def main():
    # User Login Input
    reg_number = input("Enter your registration number: ")
    name = input("Enter your name: ")

    # Initialize data structure to hold daily spends for each month
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    days_in_month = 30  # Assume 3 days for simplicity (you can adjust for each month later)
    budget_data = {month: {"daily_spends": {day: [0]*5 for day in range(1, days_in_month+1)},
                           "ideal_spend": [0]*5, "monthly_budget": 0} for month in months}

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

        # Take input for monthly budget
        monthly_budget = float(input(f"Enter your total budget for {month}: "))
        budget_data[month]["monthly_budget"] = monthly_budget

        # Ideal spending input for each category for the month
        ideal_spend_by_category = []
        for category in categories:
            ideal_spend = float(input(f"Enter your ideal spending for {category} in {month}: "))
            ideal_spend_by_category.append(ideal_spend)
        
        budget_data[month]["ideal_spend"] = ideal_spend_by_category

        # Track total spending for the month
        total_spent_month = 0

        # Loop through each day of the month and track actual spending
        for day in range(1, days_in_month+1):
            print(f"\n--- {month} {day} ---")

            # Actual spending input for each category for the day
            actual_spend_by_category = []
            for i, category in enumerate(categories):
                actual_spend = float(input(f"Enter your actual spending for {category} on day {day}: "))
                budget_data[month]["daily_spends"][day][i] = actual_spend
                actual_spend_by_category.append(actual_spend)

            # Calculate total actual spending for the day
            total_actual_spend_day = sum(actual_spend_by_category)
            total_ideal_spend_day = sum(ideal_spend_by_category)
            
            # Calculate savings or overboard for the day
            savings_or_overboard_day = total_ideal_spend_day - total_actual_spend_day
            total_spent_month += total_actual_spend_day

            if savings_or_overboard_day >= 0:
                print(f"Great! You saved {savings_or_overboard_day:.2f} today.")
            else:
                print(f"You went overboard by {-savings_or_overboard_day:.2f} today.")
                # Calculate how much money should be spent in each category for remaining days
                remaining_days = days_in_month - day
                remaining_budget = monthly_budget - total_spent_month
                
                if remaining_days > 0:
                    ideal_per_day = remaining_budget / remaining_days
                    suggested_spending = [ideal_per_day * (ideal / total_ideal_spend_day) for ideal in ideal_spend_by_category]
                    
                    print("\nTo stay within your monthly budget, you should aim to spend the following amounts on the remaining days:")
                    for i, category in enumerate(categories):
                        print(f"{category}: {suggested_spending[i]:.2f} per day")
            
            # Display bar chart comparing ideal and actual spending for the day
            display_bar_chart_day(categories, ideal_spend_by_category, actual_spend_by_category, month, day)
            
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