import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    student_info = {}
    student_info["first_name"], student_info["last_name"], student_info["github"] = row
    return student_info
    # return """\
    # Student: %s %s
    # Github account: %s"""%(row[0], row[1], row[2])

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students (first_name, last_name, github) VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student"

def get_project_by_title(project_title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    print """\
    Project: %s
    Description: %s
    Maximum Grade: %d""" % (row[0], row[1], row[2])

def make_new_project(project_title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (project_title, description, max_grade))
    CONN.commit()
    print "Successfully added project"

def get_grade_by_project(github, project_title):
    query = """SELECT Students.first_name, Students.last_name, Grades.project_title, Grades.grade FROM Students JOIN Grades ON
        (Students.github = Grades.student_github) WHERE Grades.student_github = ? AND Grades.project_title = ? """
    DB.execute(query, (github, project_title))
    row = DB.fetchone()
    if row is None:
        print "No record"
    else:
        print """\
    Student Name: %s %s
    Project: %s
    Grade: %d""" % (row[0], row[1], row[2], row[3])

def insert_grade(github, project_title, grade):
    query = """INSERT INTO Grades (student_github, project_title, grade) VALUES
        (?, ?, ?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    print "Successfully added grade"

def show_grades(github):
    query1 = """SELECT first_name, last_name FROM Students WHERE github = ?"""
    DB.execute(query1, (github,))
    first_name, last_name = DB.fetchone()

    query = """SELECT Students.first_name, Students.last_name, Grades.project_title, Grades.grade FROM
        Students JOIN Grades ON (Students.github=Grades.student_github) WHERE Students.github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchall()
    dict_of_grades = {}
    for item in row:
        first_name, last_name, project_title, grade = item
        dict_of_grades[project_title] = grade
    return dict_of_grades

def get_students_and_grades(project):
    """Gets all students and grades for a given project"""
    query = """SELECT Students.github, Students.first_name, Students.last_name, Grades.grade FROM Students JOIN Grades ON 
        (Students.github = Grades.student_github) WHERE Grades.project_title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchall()
    dict_of_students = {}
    for student in row:
        github, first_name, last_name, grade = student
        dict_of_students.setdefault(github, {})
        dict_of_students[github].setdefault("first_name", first_name)
        dict_of_students[github].setdefault("last_name", last_name)
        dict_of_students[github].setdefault("grade", grade)
    return dict_of_students



def parse_arguments(input_string):
    """Parses the user input in case arguments are within quotes"""
    new_list = []
    word = ""
    inquotes = False
    for char in input_string + " ":
        if char == '"' and inquotes == False:
            inquotes = True
        elif inquotes == True and char == '"':
            new_list.append(word)
            word = ""
            inquotes = False
        elif char == " " and inquotes == False:
            if word:
                new_list.append(word)
            word = ""
        else:
            word += char
    return new_list


def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        # tokens = input_string.split()
        tokens = parse_arguments(input_string)
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "get_grade_by_project":
            get_grade_by_project(*args)
        elif command == "insert_grade":
            insert_grade(*args)
        elif command == "show_grades":
            show_grades(*args)


    CONN.close()

if __name__ == "__main__":
    main()
