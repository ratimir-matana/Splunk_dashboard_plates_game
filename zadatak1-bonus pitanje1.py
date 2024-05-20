import csv
import itertools
import math


# Function to calculate factorial
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def build_equation(nums, ops, placeholder, rbracket):
    equation = f"{placeholder}{nums[0]}{rbracket}{ops[0]}{placeholder}{nums[1]}{rbracket}{ops[1]}{placeholder}{nums[2]}{rbracket}{'=='}{last_digit}"
    # Redoslijed - zagrade
    # a / ( )
    if ops[0] == '/':
        equation = f"{placeholder}{nums[0]}{rbracket}{ops[0]}({placeholder}{nums[1]}{rbracket}{ops[1]}{placeholder}{nums[2]}{rbracket}){'=='}{last_digit}"
    # ( ) / a
    if ops[1] == '/':
        equation = f"({placeholder}{nums[0]}{rbracket}{ops[0]}{placeholder}{nums[1]}{rbracket}){ops[1]}{placeholder}{nums[2]}{rbracket}{'=='}{last_digit}"
    # a * ( )
    if ops[0] == '*':
        equation = f"{placeholder}{nums[0]}{rbracket}{ops[0]}({placeholder}{nums[1]}{rbracket}{ops[1]}{placeholder}{nums[2]}{rbracket}){'=='}{last_digit}"
    # ( ) * a
    if ops[1] == '*':
        equation = f"({placeholder}{nums[0]}{rbracket}{ops[0]}{placeholder}{nums[1]}{rbracket}){ops[1]}{placeholder}{nums[2]}{rbracket}{'=='}{last_digit}"
    return equation


def build_equation_fact_exclamation(nums, ops, placeholder_fact):
    equation = f"{nums[0]}{placeholder_fact}{ops[0]}{nums[1]}{placeholder_fact}{ops[1]}{nums[2]}{placeholder_fact}{'=='}{last_digit}"
    # Redoslijed - zagrade
    # a / ( )
    if ops[0] == '/':
        equation = f"{nums[0]}{placeholder_fact}{ops[0]}({nums[1]}{placeholder_fact}{ops[1]}{nums[2]}{placeholder_fact}){'=='}{last_digit}"
    # ( ) / a
    if ops[1] == '/':
        equation = f"({nums[0]}{placeholder_fact}{ops[0]}{nums[1]}{placeholder_fact}){ops[1]}{nums[2]}{placeholder_fact}{'=='}{last_digit}"
    # a * ( )
    if ops[0] == '*':
        equation = f"{nums[0]}{placeholder_fact}{ops[0]}({nums[1]}{placeholder_fact}{ops[1]}{nums[2]}{placeholder_fact}){'=='}{last_digit}"
    # ( ) * a
    if ops[1] == '*':
        equation = f"({nums[0]}{placeholder_fact}{ops[0]}{nums[1]}{placeholder_fact}){ops[1]}{nums[2]}{placeholder_fact}{'=='}{last_digit}"
    return equation


# Function to generate equations
def generate_equations(plate_num, last_digit):
    total_num = 0
    operations = ['+', '-', '*', '/', 'sqrt']
    single_ops = ['!']
    equations = set()

    # Generate all possible equations
    for ops in itertools.product(operations, repeat=2):
        nums = (plate_num[0], plate_num[1], plate_num[2])
        for sop in itertools.product(single_ops, repeat=3):
            if '!' in sop:
                placeholder = 'math.factorial('
                rbracket = ')'
                equation = build_equation(nums, ops, placeholder, rbracket)
            try:
                result = eval(equation)
                if result:
                    if 'math.factorial' in equation:
                        placeholder = '!'
                        equation = build_equation_fact_exclamation(nums, ops, placeholder)
                    if '==' in equation:
                        equation = equation.replace('==', '=')
                    equations.add((plate_num + '-' + str(last_digit), result))
                    total_num += 1
                else:
                    equations.add((plate_num + '-' + str(last_digit), result))
            except:
                pass

    return list(equations), total_num


# Generate equations for all 3-digit combinations, generate all last digits combination
all_equations = []
for i in range(0, 1000):
    for j in range(0, 10):
        plate_num = "{:03d}".format(i)
        last_digit = int(j)
        equations, count = generate_equations(plate_num, last_digit)
        all_equations.extend(equations)


# Write equations to CSV
with open('equations2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["plate_num", "can_be_solved"])
    writer.writerows(all_equations)

print("Equations have been written to equations2.csv!")
