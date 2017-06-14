"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def home_page():
    students_list = hackbright.show_all_student()
    projects_list = hackbright.show_all_project()

    return render_template("home-page.html", studentlist= students_list, projectlist=projects_list )
    

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
    description = request.form.get('lastname')
    first_name = request.form.get('maxgrade')

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




@app.route("/project-add")
def project_add():
    """Add a student."""

    return render_template('project_add.html')


@app.route("/project-add", methods=['POST'])
def project_add_success():

    title = request.form.get('title')
    description = request.form.get('description')
    maxgrade = request.form.get('maxgrade')

    hackbright.make_new_project(title, description, maxgrade)

    return render_template('project_add_success.html', title=title)



@app.route("/assign-grade")
def assign_grade():
    students_list = hackbright.show_all_student()
    projects_list = hackbright.show_all_project()

    return render_template("assign_grade.html", studentlist= students_list,
                            projectlist=projects_list)
    
@app.route("/assign-grade", methods=["POST"])
def grade_assigned():

    github = request.form.get('student')

    title = request.form.get('project')

    new_grade = request.form.get('grade')

    project_grade = hackbright.get_grade_by_github_title(github, title)
   
    print github, title,project_grade

    if project_grade:
        hackbright.update_grade(github, title, new_grade)

    else:
        hackbright.assign_grade(github, title, new_grade)

    return render_template("grade_assigned.html")




if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
