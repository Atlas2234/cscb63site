import sqlite3
from flask import Flask, render_template, request, g, redirect, url_for, session, escape

DATABASE='./assignment3.db'

#Function get_db() is taken from: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#Function query_db is taken from: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#Function make_dicts is taken from: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

app = Flask(__name__)

#Secret key for sessions, MUST HAVE!
app.secret_key=b'security'

#Function close_connection is taken from: https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# route to either welcome screen or incorrect login information screen
@app.route('/redirect')
def welcome():
    # if the user key is defined in the session then show the welcome screen
    if "user" in session:
        return render_template("redirect.html", position=session["login_position"])
    
    # if the user key is not defined in the session then show incorrect login information screen
    return render_template("reenter.html")


# route for authenticating the login information
# this route can be accessed with GET or POST
@app.route('/authenticate', methods=['GET', 'POST']) 
def authentication():
    # opens up the database and stores it in db
    db=get_db()
    # sets db to display queries in dictionaries
    db.row_factory = make_dicts

    # retrieves the user_id value from the form and stores it in utorid
    utorid=request.form['user_id']
    # retrieves the user_password value from the form and stores it in utorid
    password=request.form['user_password']
    
    # queries for utorid in the database for the Login table and stores the query into id_auth
    id_auth = query_db('select * from Login where utorid = ?', [utorid], one=True)
    # queries for password in the database for the Login table and stores the query into pass_auth
    pass_auth = query_db('select * from Login where password = ?', [password], one=True)


    # Checks if the method POST was used to access app route, will only happen when user submits the form
    if request.method=='POST':
        # If the id_auth query or the pass_auth query are none, then username or password is not in the database and direct the user to the wrong login information page
        if (id_auth is None) or (pass_auth is None):
            return render_template("reenter.html")
        # If the id_auth query or the pass_auth query are a value, then username or password is in the database and direct the user to the welcome page
        else:
             session["user"] = utorid
             get_position = query_db('select position from Login where utorid = ?', [utorid], one=True)
             #close the database
             db.close()
             session["login_position"] = get_position['position']

             return redirect(url_for('welcome')) #serves the same purpose as return render template except it redirects the user to the app route cotaining the function (in this case welcome) isntead of the html page.

# route the user to the account creation page
@app.route('/account')
def form():
    return render_template("account.html")

# route for creating an account
@app.route('/create_account')
def create_account():
    # opens the database and store it in db
    db=get_db()

    # gets the user_id name from the form and stores it in utorid
    utorid=request.args.get('user_id')
    # gets the user_password name and stores it in password
    password=request.args.get('user_password')
    # gets the user_name name and stores it in name
    name=request.args.get('user_name')
    #  gets the user_position name and stores it in position
    position=request.args.get('user_position')


    #Executes query
    cursor = db.cursor() #creates a cursor for db
    cursor.execute('INSERT INTO login (utorid, position, password, name) VALUES (?, ?, ?, ?)', [utorid, position,password, name]) #uses cursor to execute a sqlite query not involving searching

    db.commit() #commit the database
    #Executes query end


    return render_template("created.html")


#route for the main page, which is also the login screen, if user logged in already the session will be created and the user does not have to log in again. If the user logged out then the login page will be shown
@app.route('/')
def index():
    if "user" in session:
        return redirect(url_for('welcome'))
    
    return render_template("index.html")

#route to log out the user
@app.route('/logout')
def out():
    session.clear() #clears the session so that it is not remembered IMPORTANT!
    return redirect(url_for('index')) #redirects the user to the rout containing the function index.


@app.route('/main')
def landing():
    if "user" in session:
        return render_template("redirect.html", id = "#top-page")

    return render_template("index.html")
    

@app.route('/announcements')
def announcements():
    if "user" in session:
        return render_template("announcements.html", id = "#top-page")

    return render_template("index.html")

@app.route('/calendar')
def calendar():
    if "user" in session:
        return render_template("calendar.html", id = "#top-page")

    return render_template("index.html")

@app.route('/lecture')
def lecture():
    if "user" in session:
        return render_template("lecture.html", id = "#top-page")

    return render_template("index.html")

@app.route('/tutorial')
def tutorial():
    if "user" in session:
        return render_template("tutorial.html", id = "#top-page")

    return render_template("index.html")

@app.route('/assignment')
def assignment():
    if "user" in session:
        return render_template("assignment.html", id = "#top-page")

    return render_template("index.html")

@app.route('/test')
def test():
    if "user" in session:
        return render_template("test.html", id = "#top-page")

    return render_template("index.html")

@app.route('/grade')
def grade():
    if "user" in session:
        db=get_db()
        db.row_factory = make_dicts
        if session["login_position"] == 'student':
            students=[]
            for student in query_db('SELECT assessments, grade FROM grades WHERE utorid = ?', [session["user"]]):
                students.append(student)

            name=request.args.get('student_name')
            # gets the student_assessment from the form and stores it in assessment
            assessment=request.args.get('student_assessment')
            # gets the student_request  from the form and stores it in request
            reason=request.args.get('student_reason')

            

            if(assessment != None):
                id_auth = query_db('select * from Login where utorid = ?', [session["user"]], one=True)
                name_auth = query_db('select * from Login where utorid = ?', [name], one=True)
                assessment_auth = query_db('select * from Login where utorid = ?', [assessment], one=True)
                reason_auth = query_db('select * from Login where utorid = ?', [reason], one=True)

                if((id_auth is None) or (name_auth is None) or(assessment_auth is None) or (reason_auth is None)):
                    return render_template("student_grade.html", student = students)

                # #Executes query
                cursor = db.cursor() #creates a cursor for db
                cursor.execute('INSERT INTO regrade (utorid, name, assessments, reason) VALUES (?, ?, ?, ?)', [session["user"], name, assessment, reason]) #uses cursor to execute a sqlite query not involving searching

                db.commit() #commit the database
                
                db.close()
            return render_template("student_grade.html", student = students)

        else:
            # gets the student's username from the form and stores it in student_utorid
            student_utorid=request.args.get('student_utorid')
            # gets the student's name and stores it in student_name
            student_name=request.args.get('student_name')
            # gets what assessment to add from the form and stores it in student_assessment
            student_assessment=request.args.get('student_assessment')
            #  gets what grade to add from the form and stores it in add_student_grade
            add_student_grade=request.args.get('student_grade')

            # queries for utorid in the database for the Login table and stores the query into id_auth
            id_auth = query_db('SELECT * FROM Login WHERE utorid = ? AND position = \'student\'', [student_utorid], one=True)
            if((student_utorid != None) and (id_auth != None)):
                #Executes query
                cursor = db.cursor() #creates a cursor for db
                #uses cursor to execute a sqlite query not involving searching 
                cursor.execute('INSERT INTO grades (utorid, name, assessments, grade) VALUES (?, ?, ?, ?)', [student_utorid, student_name, student_assessment, add_student_grade]) 
                #Executes query end
                db.commit()
               
            instructors = []
            for instructor in query_db('SELECT * FROM grades'):
                instructors.append(instructor)

            db.close()
            return render_template("instructor_grade.html", instructor = instructors)
    return render_template("index.html") 
    

@app.route('/view-regrade')
def view_regrade():
    if "user" in session:
        db=get_db()
        db.row_factory = make_dicts
        if session["login_position"] == 'instructor':
            instructors=[]
            for instructor in query_db('SELECT * FROM regrade'):
                instructors.append(instructor)
            
            # gets the user_id name from the form and stores it in utorid
            utorid=request.args.get('user_id')
            # gets the student_assessment name from the form and stores it in assessment
            assessment=request.args.get('student_assessment')
            # gets the user_name name and stores it in name
            grade=request.args.get('student_grade')

            if(((utorid != None) or (assessment != None) or (grade != None)) and int(grade) <= 100):
                # #Executes query
                cursor = db.cursor() #creates a cursor for db
                cursor.execute('UPDATE grades SET grade = ? WHERE utorid = ? AND assessments = ?', [grade, utorid, assessment]) #uses cursor to execute a sqlite query not involving searching

                db.commit() #commit the database
                db.close()
        return render_template("instructor_regrade.html", instructor = instructors)
    
    return render_template("index.html")


@app.route('/add-feedback')
def add_feedback():

    if "user" in session:
    # opens the database and store it in db
        db=get_db()
        db.row_factory = make_dicts
        profs=[]
        for prof in query_db('SELECT utorid, name FROM login WHERE position = \'instructor\''):
            profs.append(prof)

        # gets the user_id name from the form and stores it in utorid
        utorid=request.args.get('instructor_utorid')
        # gets the student_feedback1 name and stores it in feedback1
        feedback1=request.args.get('student_feedback1')
        # gets the student_feedback2 name and stores it in feedback2
        feedback2=request.args.get('student_feedback2')
        #  gets the student_feedback3 name and stores it in feedback3
        feedback3=request.args.get('student_feedback3')
        #  gets the student_feedback4 name and stores it in feedback4
        feedback4=request.args.get('student_feedback4')

        if((utorid != None) and (utorid in profs)):
            #Executes query
            cursor = db.cursor() #creates a cursor for db
            cursor.execute('INSERT INTO anonfeedback (utorid, answer1, answer2, answer3, answer4) VALUES (?, ?, ?, ?, ?)', [utorid, feedback1, feedback2, feedback3, feedback4]) #uses cursor to execute a sqlite query not involving searching        db.commit() #commit the database
            #Executes query end
            db.commit()
            db.close()
        return render_template("feedback_student.html", prof=profs)
    return render_template("index.html")

@app.route('/view-feedback')
def view_feedback():
    if "user" in session:
        db=get_db()
        db.row_factory = make_dicts
        reviews=[]
        for review in query_db('SELECT answer1, answer2, answer3, answer4 FROM Anonfeedback WHERE utorid = ?', [session["user"]]):
            reviews.append(review)
        return render_template("feedback_instructor.html", review=reviews)
    return render_template("index.html")