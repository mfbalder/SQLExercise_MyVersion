from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
	return render_template("get_github.html")

@app.route("/student")
def get_student():
	hackbright_app.connect_to_db()
	student_github = request.args.get("github")
	student_info = hackbright_app.get_student_by_github(student_github)
	dict_of_grades = hackbright_app.show_grades(student_github)
	html = render_template('student_info.html', first_name=student_info["first_name"], last_name=student_info["last_name"],
		github=student_info["github"], projects_and_grades = dict_of_grades)
	# print dict_of_grades
	return html

@app.route("/projects")
def project_info():
	project = request.args.get("project")
	students_and_gradesdict = hackbright_app.get_students_and_grades(project)
	return render_template("display_studentgrades.html", students_and_grades = students_and_gradesdict, project = project) 

@app.route("/new_student")
def new_student():
	return render_template("new_student.html")

@app.route("/add_student")
def add_student():
	hackbright_app.connect_to_db()
	github = request.args.get("github")
	first_name = request.args.get("first_name")
	last_name = request.args.get("last_name")
	try:
		check_student = hackbright_app.get_student_by_github(github)
		message = "%s %s already exists in the system" % (first_name, last_name)
	except:
		hackbright_app.make_new_student(first_name, last_name, github)
		message = "%s %s has been successfully added" % (first_name, last_name)
	return render_template("student_added.html", message = message)


	


if __name__ == "__main__":
	app.run(debug=True)