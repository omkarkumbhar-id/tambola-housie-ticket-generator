import random
import json

with open('questions.json', 'r') as file:
    questions = json.load(file)
    must_question = questions.pop()

number_of_tickets_to_generate = 1000
questions_per_ticket = 5
required_filled_positions = 15
rows = 3
columns = 9
number_start = [1,10,20,30,40,50,60,70,80]
number_end = [9,19,29,39,49,59,69,79,90]

numbers_per_ticket = required_filled_positions - questions_per_ticket
tickets = []
number_of_non_filled_positions_in_a_row = columns - (required_filled_positions/3)

def generate_ticket(all_questions):
    non_zero_ticket = False
    five_in_a_row = False
    non_cluttered = False
    while non_zero_ticket == False or five_in_a_row == False or non_cluttered == False:
        non_zero_ticket = True
        five_in_a_row = True
        non_cluttered = True
        ticket = [[0 for i in range(columns)] for j in range(rows)]
        count = 0
        questions = set(all_questions)
        numbers = set()
        while count < required_filled_positions:
            row = random.randint(0, rows-1)
            col = random.randint(0, columns-1)
            if ticket[row][col] == 0:
                if count < numbers_per_ticket:
                    number = random.randint(number_start[col], number_end[col])
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
                if row.count(0) != number_of_non_filled_positions_in_a_row:
                    print(f"ticket had a row with more or less number of filled postions than expected. Recreating the ticket\n{ticket}\n")
                    five_in_a_row = False
        if count == required_filled_positions:
            breakfast = 0
            lunch = 0
            dinner = 0
            for row in ticket:
                for b in range(0,3):
                    if row[b] != 0:
                        breakfast += 1
                for l in range(3,6):
                    if row[l] != 0:
                        lunch += 1
                for d in range(6,9):
                    if row[d] != 0:
                        dinner += 1
            if breakfast < 4 or breakfast > 6 or lunch < 4 or lunch > 6 or dinner < 4 or dinner > 6:
                print(f"got cluttered ticket. Recreating the ticket\n{ticket}\n")
                non_cluttered = False
        if non_zero_ticket == True and five_in_a_row == True and non_cluttered == True:
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
            must_question_position = random.randint(1,questions_per_ticket)
            current_question_position = 0
            for row in range(0,rows):
                for col in range(0,columns):
                    if type("") ==  type(ticket[row][col]):
                        current_question_position += 1
                        if current_question_position == must_question_position:
                            ticket[row][col] = must_question
                            break
                if current_question_position == must_question_position:
                    break
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
