import smtplib
from email.mime.text import MIMEText
from task1 import MyLinkedList


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


def get_iterator(database, mail):
    database = list(database)
    for i in range(0, len(database)):
        if database[i]['mail'] == mail:
            return i


def send_emails_to_student(database, mail, password):
    database = list(database)
    send_email('Your test is graded',
               ('Your test is graded. Your mark is ', database[get_iterator(database, mail)]['mark']), '',
               mail, password)


users = []
file = open('students.txt')
line = file.readline()
iterator = 0
while line != '':
    data = line.split(',')
    task_list = MyLinkedList()
    task_iterator = 4
    homework_list = MyLinkedList()
    homework_iterator = task_iterator + 3
    while task_iterator < homework_iterator:
        task_list.append(data[task_iterator])
        task_iterator += 1
    if data[len(data)-1].strip() == 'GRADED' or data[len(data)-1].strip() == 'MAILED' or data[len(data)-1].strip() == 'MAILED_FINAL':
        while homework_iterator < len(data) - 2:
            homework_list.append(data[homework_iterator])
            homework_iterator += 1
        user = {
            "email": data[0].strip(),
            "name": data[1].strip(),
            "surname": data[2].strip(),
            "project": data[3].strip(),
            "lists": task_list,
            "homeworks": homework_list,
            "mark": data[len(data)-2].strip(),
            "status": data[len(data)-1].strip(),
        }
        users.append(user)
    else:
        while homework_iterator < len(data) - 1:
            homework_list.append(data[homework_iterator])
            homework_iterator += 1
        user = {
            "email": data[0].strip(),
            "name": data[1].strip(),
            "surname": data[2].strip(),
            "project": data[3].strip(),
            "lists": task_list,
            "homeworks": homework_list,
            "status": data[len(data) - 1].strip(),
        }
        users.append(user)
    iterator += 1
    line = file.readline()
for student in range(0, len(users)):
    try:
        if 'status' in users[student]:
            if users[student]['status'] != 'GRADED' and users[student]['status'] != 'MAILED_FINAL' and users[student]['status'] != 'None':
                raise ValueError('')
        else:
            raise ValueError('')
    except ValueError:
        grade_list = []
        grade_list = mark_project(grade_list, users[student]['project'])
        grade_list = grade_lists(grade_list, users[student]['lists'])
        grade_list = grade_homework(grade_list, users[student]['homeworks'])
        hom_avg = homework_average(users[student]['homeworks'])
        if hom_avg > 0.6:
            grade_list = list_correction(task_list)
            if hom_avg > 0.7:
                grade_list = list_correction(task_list)
                if hom_avg > 0.8:
                    grade_list = list_correction(task_list)
        if users[student]['project'] == '-1' or users[student]['lists'].__contains__('-1') or users[student]['homeworks'].__contains__('-1'):
            if users[student]['status'] == 'None':
                pass
        else:
            grade_avg = grade_average(grade_list)
            if points < 2:
                users[student]['mark'] = str(2)
            elif points < 3.5:
                users[student]['mark'] = str(3)
            elif points < 4:
                users[student]['mark'] = str(3.5)
            elif points < 4.5:
                users[student]['mark'] = str(4)
            elif points < 5:
                users[student]['mark'] = str(4.5)
            else:
                users[student]['mark'] = str(5)
            users[student]['status'] = 'GRADED'
            send_emails_to_student(users, users[student]['mail'], '')
            users[student]['status'] = 'MAILED_FINAL'

with open('students.txt', 'w') as file_writer:
    for student in range(0, len(users)):
        line = users[student]['email'] + ',' + users[student]['name'] + ',' + users[student]['surname'] + ',' + \
               users[student]['project']
        line += users[student]['lists'].__str__() + ',' + users[student]['homeworks'].__str__()
        if len(users[student]['mark']) > 0:
            line += ',' + users[student]['mark']
        if len(users[student]['status']) > 0:
            line += ',' + users[student]['status']
        line += '\n'
        file_writer.write(line)


def add_student(mail, name, surname, project, tasks, homeworks, database):
    d = list(database)
    for i in range(0, len(d)):
        if d[i]['mail'] == mail:
            print('Can not create this user. This email is occupied.')
            return d
    d[len(d)] = {
        "email": mail.strip(),
        "name": name.strip(),
        "surname": surname.strip(),
        "project": project.strip(),
        "lists": tasks,
        "homeworks": homeworks
    }
    return d


def delete_student(mail, database):
    d = list(database)
    for i in range(0, len(d)):
        if d[i]['mail'] == mail:
            d.pop(i)
            return d
    return d

def homework_average(homework_list):
    list = homework_list.getDataFromList()
    number_of_elements = countElementsOtherThan('-1')
    sum = 0
    for i in range(0, len(list)):
        if list[i] != '-1':
            sum += float(list[i])
    return sum / number_of_elements
def list_correction(task_list, grade_list):
    min = task_list.getMinElement('-1')
    for i in range(0, len(grade_list)):
        if min.data == grade_list[i]:
            b = True
            while b:
                new_grade = input('Input new grade')
                if new_grade == '2' or new_grade == '3' or new_grade == '3.5' or new_grade == '4' or new_grade == '4.5' or new_grade == '5':
                    if float(new_grade) > float(grade_list[i]) :
                        grade_list[i] = new_grade
                        b = False
                    else:
                        print('Grade is not corrected')
                else:
                    print('Inputed grade is not in the correct format')
    return grade_list

def mark_project(grade_list, points):
    if points < 20:
        grade_list[len(grade_list)] = str(2)
    elif points <= 24:
        grade_list[len(grade_list)] = str(3)
    elif points <= 28:
        grade_list[len(grade_list)] = str(3.5)
    elif points <= 32:
        grade_list[len(grade_list)] = str(4)
    elif points <= 36:
        grade_list[len(grade_list)] = str(4.5)
    else:
        grade_list[len(grade_list)] = str(5)
    return grade_list

def mark_list(grade_list, points):
    if points < 10:
        grade_list[len(grade_list)] = str(2)
    elif points <= 12:
        grade_list[len(grade_list)] = str(3)
    elif points <= 14:
        grade_list[len(grade_list)] = str(3.5)
    elif points <= 16:
        grade_list[len(grade_list)] = str(4)
    elif points <= 18:
        grade_list[len(grade_list)] = str(4.5)
    else:
        grade_list[len(grade_list)] = str(5)
    return grade_list

def mark_homework(grade_list, points):
    if points < 50:
        grade_list[len(grade_list)] = str(2)
    elif points <= 60:
        grade_list[len(grade_list)] = str(3)
    elif points <= 70:
        grade_list[len(grade_list)] = str(3.5)
    elif points <= 80:
        grade_list[len(grade_list)] = str(4)
    elif points <= 90:
        grade_list[len(grade_list)] = str(4.5)
    else:
        grade_list[len(grade_list)] = str(5)
    return grade_list

def grade_lists(grade_list, task_list):
    list = task_list.getDataFromList()
    for i in range(0, len(list)):
        if list[i] != '-1':
            grade_list = mark_list(grade_list, int(list[i]))
    return grade_list

def grade_homework(grade_list, homework_list):
    list = homework_list.getDataFromList()
    for i in range(0, len(list)):
        if list[i] != '-1':
            grade_list = mark_homework(grade_list, int(list[i]))
    return grade_list

def grade_average(grade_list):
    d = list(grade_list)
    sum = 0
    for i in range(0, len(d)):
        sum += d[i]
    return sum / len(d)