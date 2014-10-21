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

if __name__ == "__main__":
	app.run(debug=True)