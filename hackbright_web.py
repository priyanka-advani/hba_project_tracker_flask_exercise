"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template('student_search.html')


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    projects_grades_rows = hackbright.get_grades_by_github(github)

    return render_template('student_info.html', 
                            first=first, last=last, github=github,
                            projects_grades_rows=projects_grades_rows)

    # return "{acct} is the GitHub account for {first} {last}".format(
    #     acct=github, first=first, last=last)


@app.route("/student-add")
def student_add():
    """Add a student."""

    return render_template('student_add.html')


@app.route("/student-add-success", methods=['POST'])
def student_add_success():

    github = request.form.get('github')
    last_name = request.form.get('lastname')
    first_name = request.form.get('firstname')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template('student_add_success.html', github=github)


@app.route("/project")
def show_project():

    project_title = request.args.get('title')
    title, description, maxgrade = hackbright.get_project_by_title(project_title)
    grades_list = hackbright.get_grades_by_title(project_title)
    
    # firstname, lastname, github = hackbright.get_student_by_github(student_github)




    return render_template("project_info.html",title=title, 
                           description=description,maxgrade=maxgrade,
                           grades_list=grades_list)


@app.route("/")
def home_page():
    students_list = hackbright.show_all_student()
    projects_list = hackbright.show_all_project()

    return render_template("home-page.html", studentlist= students_list, projectlist=projects_list )
    


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
