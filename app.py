import csv
import random
import datetime
from faker import Faker

fake = Faker()

def generate_fake_data(num_accounts):
    subscription_plans = ["free", "basic", "full"]
    current_date = datetime.date.today()

    accounts = []
    for id in range(1000, 1000 + num_accounts):
        plan = random.choice(subscription_plans)
        username = fake.user_name()
        last_login_date = fake.date_between(start_date="-3y", end_date="today").strftime("%Y-%m-%d")
        
        if plan == "free":
            expire_date = (current_date + datetime.timedelta(days=random.randint(90, 365))).strftime("%Y-%m-%d")
        else:
            expire_date = (current_date + datetime.timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d")

        accounts.append([id, plan, username, last_login_date, expire_date])

    return accounts

def save_to_csv(filename, data):
    with open(filename, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["id", "plan", "username", "last_login_date", "expire_date"])
        csvwriter.writerows(data)

def load_accounts(filename):
    accounts = []
    with open(filename, mode="r") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) 
        for row in csvreader:
            accounts.append(row)
    return accounts

def print_total_accounts_per_plan(accounts):
    plan_counts = {"free": 0, "basic": 0, "full": 0}
    for account in accounts:
        plan = account[1]
        plan_counts[plan] += 1
    
    for plan, count in plan_counts.items():
        print(f"Total {plan} accounts: {count}")

def find_accounts_with_days_until_expiration(accounts, days):
    current_date = datetime.date.today()
    for account in accounts:
        plan = account[1]
        expire_date = datetime.datetime.strptime(account[4], "%Y-%m-%d").date()
        
        if (expire_date - current_date).days > days:
            print(f"{plan.capitalize()} account '{account[2]}' has more than {days} days until expiration.")

fake_accounts = generate_fake_data(1000)
save_to_csv("accounts.csv", fake_accounts)

accounts = load_accounts("accounts.csv")

while True:
    print("1. Print total accounts per plan")
    print("2. Find free accounts that have mora than 3 months to login")
    print("3. Find expired basic or full accounts")
    print("4. Quit")
    
    choice = input("Choose your action: ")
    
    if choice == "1":
        print_total_accounts_per_plan(accounts)
    elif choice == "2":
        find_accounts_with_days_until_expiration(accounts, 90)
    elif choice == "3":
        find_accounts_with_days_until_expiration(accounts, -1)
    elif choice == "4":
        break
    else:
        print("Wrong choice. Choose either 1, 2, 3, or 4.")
