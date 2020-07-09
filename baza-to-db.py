import sqlite3
import codecs
import os
import pathlib

def parse_question(file_name):
    file = codecs.open(file_name, 'r', 'windows-1250') # or utf-8
    
    answer_line = file.readline().replace('X', '').rstrip()
    title = file.readline().rstrip()
    correct_answers = []
    answers = []

    for index, achar in enumerate(answer_line):
        if (achar == '1'):
            correct_answers.append(index)
    
    for index, answer in enumerate(file):
        answer = answer.rstrip()
        answers.append([answer, False])

    for answer in correct_answers:
        flagged_answer = answers[answer]
        flagged_answer[1] = True
        answers[answer] = flagged_answer
    
    file.close()
    return title, answers


def baza_to_db():  
    directory = pathlib.Path().absolute()  
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    c.execute('CREATE TABLE "Questions" ("question_id" INTEGER NOT NULL, "title" TEXT, PRIMARY KEY("question_id"))')
    c.execute('CREATE TABLE "Answers"   ("question_id" INTEGER, "answer_text" TEXT, "is_correct" INTEGER, FOREIGN KEY("question_id") REFERENCES "Questions"("question_id"))')
  
    for index, file in enumerate(os.listdir(directory), 1):
        if file.endswith('.txt'):
            title, answers = parse_question(file)
    
            params = (index, title)
            c.execute('INSERT INTO questions VALUES(?, ?)', params)
            for answer in answers:
                params = (index, answer[0], answer[1])
                c.execute('insert into answers values(?, ?, ?)', params)
            conn.commit();

    conn.close()

baza_to_db()