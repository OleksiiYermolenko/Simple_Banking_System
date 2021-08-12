import sqlite3
import sys
import random
from random import sample
from functools import reduce


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
try:
    cur.execute('''CREATE TABLE card(
               id INTEGER PRIMARY KEY,
               number text,
               pin text,
               balance INTEGER DEFAULT 0
               )''')
except sqlite3.OperationalError:
    var = None

"""SQL explanations
"""

# cur.execute('''SELECT * FROM card''')
# rows = cur.fetchall()
# for row in rows:
#     print(row)


class Menu:

    def __init__(self):
        self.out_money = None
        self.account = None
        self.pin = None
        self.number = None
        self.num_to = None
        self.accounts = {}
        self.choices_main = {
            "1": self.create_account,
            "2": self.log_in,
            "0": self.exit,
        }

        self.choices_sub = {
            "1": self.balance,
            "2": self.add_income,
            "3": self.do_transfer,
            "4": self.close_aсcount,
            "5": self.log_out,
            "0": self.exit,
        }

    @staticmethod
    def display_main():
        print("""
                1. Create an account
                2. Log into account
                0. Exit
                """)

    @staticmethod
    def display_sub():
        print("""
                1. Balance
                2. Add income
                3. Do transfer
                4. Close account
                5. Log out
                0. Exit
                """)

    def run_main(self):
        while True:
            self.display_main()
            choice = input()
            action = self.choices_main.get(choice)
            if action == '2':
                self.run_sub()
            elif action:
                action()

            else:
                print("{0} is not a valid choice".format(choice))

    def run_sub(self):
        while True:
            self.display_sub()
            choice = input()
            action = self.choices_sub.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def create_account(self):  # OK
        self.account = ''.join(sample("0123456789", 10))
        self.pin = ''.join(sample("0123456789", 4))
        self.number = "400000" + str(self.account)

        if self.luhn(self.number) == 0:
            self.accounts[self.account] = self.pin
            print('Your card has been created')
            print('Your card number:')
            print(self.number)
            print('Your card PIN:')
            print(self.pin)
            cur.execute('INSERT INTO card(number, pin) VALUES (?, ?)', (self.number, self.pin))
            conn.commit()
            print("1 record inserted, ID:", cur.lastrowid)
        else:
            self.create_account()

    @staticmethod
    def luhn(number):  # OK
        lookup = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)
        account = reduce(str.__add__, filter(str.isdigit, number))
        evens = sum(int(i) for i in account[-1::-2])
        odds = sum(lookup[int(i)] for i in account[-2::-2])
        return (evens + odds) % 10

    def log_in(self):
        sql = 'SELECT pin FROM card where  number = ?'
        self.number = str(input('Enter your card number:'))
        self.pin = str(input('Enter your PIN:'))
        cur = conn.cursor()
        rows = cur.execute(sql, (self.number,))

        for row in rows:
            if self.pin == str(row[0]):
                print('You have successfully logged in!')
                self.run_sub()

        print('Wrong card number or PIN!')
        return self.run_main()

    def add_outcome(self, number, out_money):
        sql = 'SELECT balance FROM card where  number =?'
        cur = conn.cursor()
        cur.execute(sql, (self.number,))
        rows = cur.fetchall()
        for row in rows:
            out_money = row[0] - out_money
            print(out_money)
            cur.execute('UPDATE card SET balance = ? WHERE number = ?', (out_money, number,))
            conn.commit()
        # self.balance()

    def add_income(self):
        add_money = int(input("add '"))
        self.add_income_count(self.number, add_money)

    def add_income_count(self, number, add_money):
        sql = 'SELECT balance FROM card where  number =?'
        cur = conn.cursor()
        cur.execute(sql, (number,))
        rows = cur.fetchall()
        # add_money = int(input("add '"))

        if int(add_money) > 0:
            for row in rows:
                add_money += row[0]
                print(add_money)

            cur.execute('UPDATE card SET balance = ? WHERE number = ?', (add_money, number,))
            conn.commit()
        else:
            self.add_income_count
        print('Income was added!')
        # self.balance()

    def do_transfer(self):
        print('Transfer')
        print('Enter card number:')
        num_to = input()
        print(self.check_exist(num_to))

        if self.luhn(num_to) != 0:
            print('Probably you made a mistake in the card number. Please try again!')
            self.run_sub()

        elif self.check_exist(num_to) is None:
            print('Such a card does not exist')
            self.run_sub()


        transfer_money = int(input('Enter how much money you want to transfer: '))

        cur = conn.cursor()
        cur.execute('SELECT number FROM card where  number =?', (self.number,))
        rows = cur.fetchall()
        for row in rows:
            if row[0] == str(num_to):
                print("You can't transfer money to the same account!")
            elif transfer_money > int(self.count_balance()):
                print('Not enough money!')
            else:
                self.add_outcome(self.number, transfer_money)
                self.add_income_count(num_to, transfer_money)

    def check_exist(self, number):
        cur = conn.cursor()
        cur.execute('SELECT number FROM card where  number =?', (number,))
        rows = cur.fetchall()
        for row in rows:
            return row[0]



    def close_aсcount(self):  # OK
        cur = conn.cursor()
        cur.execute('DELETE FROM card where  number =?', (self.number,))
        conn.commit()
        print('The account has been closed!')

    def log_out(self):  # OK
        print('You have successfully logged out!')
        return self.run_main()

    def count_balance(self):  # OK
        cur = conn.cursor()
        cur.execute('SELECT balance FROM card where  number =?', (self.number,))
        rows = cur.fetchall()
        for row in rows:
            return row[0]

    def balance(self):  # OK
        print('Balance: ', self.count_balance())

    @staticmethod
    def exit():  # OK
        print("Bye!")
        sys.exit(0)


if __name__ == "__main__":
    Menu().run_main()



