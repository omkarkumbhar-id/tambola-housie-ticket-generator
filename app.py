import random
import json
import operator

with open('questions.json', 'r') as file:
    questions = json.load(file)

number_of_tickets_to_generate = 1000
questions_per_ticket = 5
required_filled_positions = 15
rows = 3
columns = 9

numbers_per_ticket = required_filled_positions - questions_per_ticket
tickets = []
number_of_non_filled_positions_in_a_row = columns - (required_filled_positions/3)

def generate_ticket(all_questions):
    non_zero_ticket = False
    five_in_a_row = False
    while non_zero_ticket == False or five_in_a_row == False:
        non_zero_ticket = True
        five_in_a_row = True
        ticket = [[0 for i in range(columns)] for j in range(rows)]
        count = 0
        questions = set(all_questions)
        numbers = set()
        while count < required_filled_positions:
            row = random.randint(0, rows-1)
            col = random.randint(0, columns-1)
            if ticket[row][col] == 0:
                if count < numbers_per_ticket:
                    number = random.randint(col * 10 + 1, (col + 1) * 10)
                    if number not in numbers:
                        ticket[row][col] = number
                        numbers.add(number)
                        count += 1
                else:
                    question = random.choice(list(questions))
                    ticket[row][col] = question
                    questions.remove(question)
                    count += 1
        if count == required_filled_positions:
            for i in range(0, columns):
                non_zero = False
                for j in range(0, rows):
                    if ticket[j][i] != 0:
                        non_zero = True
                if non_zero == False:
                    print(f"ticket had a column with all zeroes. Recreating the ticket\n{ticket}\n")
                    non_zero_ticket = False
        if count == required_filled_positions:
            for row in ticket:
                if operator.countOf(row, 0) != number_of_non_filled_positions_in_a_row:
                    print(f"ticket had a row with more or less number of filled postions than expected. Recreating the ticket\n{ticket}\n")
                    five_in_a_row = False
        if non_zero_ticket == True and five_in_a_row == True:
            for i in range(0,columns):
                column_numbers = []
                for j in range(0,rows):
                    number = ticket[j][i]
                    if type(number) == type(91) and number != 0:
                        column_numbers.append(number)
                column_numbers.sort(reverse=True)
                for j in range(0,rows):
                    number = ticket[j][i]
                    if type(number) == type(91) and number != 0:
                        ticket[j][i] = column_numbers.pop()
            print("Ticket Generated Successfully")
    return ticket


def generate_tickets(q, n):
    all_unique_tickets = False
    while all_unique_tickets == False:
        print(f"Trying to generate {n} unique tickets")

        for i in range(n):
            tickets.append(generate_ticket(q))

        unique_list = list(set(tuple(tuple(sub_sub_list)
                           for sub_sub_list in sub_list) for sub_list in tickets))
        if len(unique_list) == n:
            all_unique_tickets = True

    print(f"Successfully generated {len(unique_list)} unique tickets")

    with open("tickets.json", "w") as file:
        json.dump(tickets, file)


generate_tickets(q=questions,n=number_of_tickets_to_generate)
