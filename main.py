import budget
from budget import create_spend_chart


def main():
    food = budget.Category("Food")
    food.deposit(900, "deposit")
    
    entertainment = budget.Category("Entertainment")
    entertainment.deposit(900, "deposit")


    business = budget.Category("Business")
    business.deposit(900, "deposit")

    food.withdraw(105.55)
    entertainment.withdraw(33.40)
    business.withdraw(10.99)

    print(create_spend_chart([business, food, entertainment]))

if __name__ == "__main__":
    main()
