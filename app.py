import random
import json

with open('questions.json', 'r') as file:
    questions = json.load(file)

number_of_tickets_to_generate = 500
questions_per_ticket = 5
required_filled_positions = 15
rows = 3
columns = 9

numbers_per_ticket = required_filled_positions - questions_per_ticket
tickets = []


def generate_ticket(questions):
    ticket = [[0 for i in range(columns)] for j in range(rows)]
    count = 0
    questions = set(questions)
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
    return ticket


def generate_tickets(q, n):
    all_unique_tickets = False
    while all_unique_tickets == False:
        print(f"Trying to generate {n} unique tickets")

        for i in range(n):
            tickets.append(generate_ticket(q))
        
        unique_list = list(set(tuple(tuple(sub_sub_list) for sub_sub_list in sub_list) for sub_list in tickets))
        if len(unique_list) == n:
            all_unique_tickets = True

    print(f"Successfully generated {len(unique_list)} unique tickets")
    
    with open("tickets.json","w") as file:
        json.dump(tickets, file)


generate_tickets(q=questions,n=number_of_tickets_to_generate)
