class Category:

    def __init__(self, cat):
        self.name = cat
        self.ledger = []

    def __str__(self):
        size = 30
        total_str = f'Total: {self.get_balance()}'
        half_title = '*' * int((len('*' * size) - len(self.name)) / 2)
        title = f'{half_title}{self.name}{half_title}'
        lines = ''

        for n in self.ledger:
            lines += self.construct_linee(n['amount'], n['description'])

        return f'{title}\n{lines}{total_str}'

    def construct_linee(self, amount, description):
        limit_description = description[0:23]
        formated_amount = str("%.2f" % amount)
        return f'{limit_description.ljust(23)}{formated_amount.rjust(7)}\n'

    def deposit(self, amount, description=''):
        cash_register = {'amount': amount, 'description': description}

        self.ledger.append(cash_register)
        return cash_register

    def transfer(self, amount, category):
        can_withdraw = self.check_funds(amount)
        cash_register = {'amount': amount,
                         'description': f"Transfer from {self.name}"}

        if can_withdraw is True:
            category.deposit(
                cash_register["amount"], cash_register["description"])
            self.withdraw(amount, f"Transfer to {category.name}")
            return True

        return False

    def withdraw(self, amount, description=''):
        can_withdraw = self.check_funds(amount)

        if can_withdraw is True:
            cash_register = {'amount': -amount, 'description': description}

            self.ledger.append(cash_register)
            return True

        return False

    def get_balance(self):
        total = 0

        for value in self.ledger:
            total += value["amount"]

        return total

    def check_funds(self, amount):
        if (self.get_balance() - amount) < 0:
            return False
        return True


def create_spend_chart(categories):
    pct = 100
    title = 'Percentage spent by category'
    line = ''

    # construct chart
    while pct >= 0:
        line = f'{line +  str(pct).rjust(3)}| '

        line += construct_pct_lines(categories, pct)

        line += '\n'
        pct -= 10

    # end of chart construct

    names = construct_name_chart(categories)

    return f'{title}\n{line}{names}'


def construct_pct_lines(categories, pct):
    lista = list(construct_dash(categories).replace('-', "X").strip())
    lista.pop(0)
    lista.pop()
    total_withdraw = calc_total_withdraw(categories)

    for category in categories:
        if pct <= calc_pct(calc_withdraw(category), total_withdraw):
            if categories.index(category) == 0:
                lista[0] = 'o'
            else:
                lista[categories.index(category)] = '  o'

    return "".join(lista).replace('X',' ')


def construct_name_chart(categories):
    max_name_size = 0

    for n in categories:
        if max_name_size < len(n.name):
            max_name_size = len(n.name)

    names_arr = []
    for n in categories:
        names_arr.append(n.name.ljust(max_name_size))

    cont = 0
    names = ''

    while cont < max_name_size:
        names += '\n'.ljust(4)
        for n in names_arr:
            names += n[cont].rjust(3)
        cont += 1

    return f'{construct_dash(categories)}\n{names[1:]}'


def construct_dash(categories):
    linedash = ''
    dash = '-' * ((len(categories) * 3) + 1)
    linedash += dash.rjust(len(dash)+4)

    return linedash


def calc_total_withdraw(categories):
    total = 0
    for cat in categories:
        for n in cat.ledger:
            if n['amount'] < 0:
                total += (n['amount'] * -1)

    return total


def calc_withdraw(category):
    total = 0

    for n in category.ledger:
        if n['amount'] < 0:
            total += (n['amount'] * -1)

    return total


def calc_pct(num, total):
    return int((num / total) * 100)
