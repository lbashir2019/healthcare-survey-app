import csv
import os

class User:
    def __init__(self, age, gender, income, expenses):
        self.age = age
        self.gender = gender
        self.income = income
        self.expenses = expenses

    def save_to_csv(self, filename):
        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write header if file does not exist
            if not file_exists:
                header = ["age", "gender", "income"] + list(self.expenses.keys())
                writer.writerow(header)
            # Write user data
            row = [self.age, self.gender, self.income] + [self.expenses.get(k, 0) for k in self.expenses.keys()]
            writer.writerow(row)
