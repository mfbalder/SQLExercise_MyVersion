from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
	"""Displays home page"""
	return render_template("get_github.html")


@app.route("/student")
def get_student():
	"""Gets the student's name and grades by their github account, displays them on a new page"""
	hackbright_app.connect_to_db()

	student_github = request.args.get("github")
	student_info = hackbright_app.get_student_by_github(student_github)
	dict_of_grades = hackbright_app.show_grades(student_github)

	html = render_template('student_info.html', 
		first_name=student_info["first_name"], 
		last_name=student_info["last_name"], 
		github=student_info["github"], 
		projects_and_grades = dict_of_grades)
	return html


def get_project_grades(project):
	"""Gets all students and their grades for a given project"""
	hackbright_app.connect_to_db()
	students_and_gradesdict = hackbright_app.get_students_and_grades(project)
	return students_and_gradesdict

# @app.route("/projects")   # /projects-page
# def project_info():
# 	"""Gets all students and their grades for a given project, displays them on a new page"""
# 	project = request.args.get("project")
# 	students_and_gradesdict = get_project_grades(project)
# 	print students_and_gradesdict
# 	return render_template("display_studentgrades.html", students_and_grades = students_and_gradesdict, project = project) 


@app.route("/project-info-ajax")
def project_info_ajax_form():
	return render_template("project_info_ajax.html")

@app.route("/project-snippet")
def project_info_snippet():
	project = request.args.get("project")
	students_and_gradesdict = get_project_grades(project)
	print students_and_gradesdict
	return render_template("display_studentgrades.html", project=project, students_and_grades=students_and_gradesdict)


@app.route("/new_student")
def new_student():
	"""when the user clicks Add New Student, displays a new page to enter student info"""
	return render_template("new_student.html")


@app.route("/add_student")
def add_student():
	"""when the user submits the new student form, checks the database to see if
		that github account if already in the database: if not, adds the user and 
		displays a new page with 'student added' message"""
	hackbright_app.connect_to_db()
	github = request.args.get("github")
	first_name = request.args.get("first_name")
	last_name = request.args.get("last_name")

	try:
		check_student = hackbright_app.get_student_by_github(github)
		message = "%s %s already exists in the system" % (first_name, last_name)
	except AttributeError:   # FIXME: too broad
		hackbright_app.make_new_student(first_name, last_name, github)
		message = "%s %s has been successfully added" % (first_name, last_name)

	return render_template("student_added.html", message = message)

# @app.route("/new_project")
# def new_project():
# 	hackbright_app.connect_to_db()



	


if __name__ == "__main__":
	app.run(debug=True)