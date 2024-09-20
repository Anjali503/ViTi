def main():
    # User Login Input
    reg_number = input("Enter your registration number: ")
    name = input("Enter your name: ")

    # Initialize data structure to hold daily budgets and spends for each month
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    days_in_month = 31  # Assume 31 days for simplicity (you can adjust for each month later)
    budget_data = {month: {"daily_budget": 0, "daily_spends": {day: [0]*5 for day in range(1, days_in_month+1)}} for month in months}

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

        # Budget Input for each day
        ideal_monthly_budget = float(input("Enter your ideal monthly budget: "))
        daily_budget = float(input("Enter your ideal daily budget: "))
        budget_data[month]["daily_budget"] = daily_budget
        total_monthly_budget = daily_budget * days_in_month

        # Track total spent and cumulative savings/overboard amounts
        total_spent_month = 0
        cumulative_savings = 0

        for day in range(1, days_in_month+1):  # Loop through each day of the month
            print(f"\n--- {month} {day} ---")

            # User inputs the actual spending for each category for the day
            for i, category in enumerate(categories):
                actual_spend = float(input(f"Enter your actual spending for {category} on day {day}: "))
                budget_data[month]["daily_spends"][day][i] = actual_spend

            # Calculate total spent for the day
            total_spent_day = sum(budget_data[month]["daily_spends"][day])
            total_spent_month += total_spent_day

            # Determine if the user is overboard or saved for the day
            savings_or_overboard = daily_budget - total_spent_day
            cumulative_savings += savings_or_overboard

            # Suggest daily budget adjustment for the rest of the month
            days_remaining = days_in_month - day
            if days_remaining > 0:
                # Adjust the daily budget for remaining days to stay within the overall budget
                suggested_budget_remaining = (total_monthly_budget - total_spent_month) / days_remaining
            else:
                suggested_budget_remaining = 0

            # Show summary for the current day
            print(f"\n--- Day {day} Summary ---")
            print(f"Total spent today: {total_spent_day:.2f} / Daily budget: {daily_budget:.2f}")
            if savings_or_overboard > 0:
                print(f"You saved {savings_or_overboard:.2f} today.")
            else:
                print(f"You exceeded the daily budget by {-savings_or_overboard:.2f} today.")

            print(f"Cumulative savings/overboard up to today: {cumulative_savings:.2f}")
            print(f"Suggested daily budget for the next {days_remaining} days: {suggested_budget_remaining:.2f}")

            # Show comparison by category
            for i, category in enumerate(categories):
                actual_spend = budget_data[month]["daily_spends"][day][i]
                print(f"{category}: Actual: {actual_spend:.2f}")

        # Display summary for the entire month
        print(f"\n--- Budget Summary for {month} ---")
        print(f"Total spent: {total_spent_month:.2f}")
        print(f"Total monthly budget: {total_monthly_budget:.2f}")

        if total_spent_month > total_monthly_budget:
            print(f"You exceeded your monthly budget by: {total_spent_month - total_monthly_budget:.2f}")
        else:
            print(f"You are within your monthly budget. You saved: {total_monthly_budget - total_spent_month:.2f}")

if __name__ == "__main__":
    main()