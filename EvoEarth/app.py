from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

#creating flask app
app = Flask(__name__)
app.secret_key='HelloWorld!'
#creating database to store the students details
def database():
    mydb = sqlite3.connect("Student.db")
    cur = mydb.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ts (
            user_id INTEGER UNIQUE,
            password TEXT,
            name TEXT,
            age INTEGER,
            skills TEXT
        )
    """)
    mydb.commit()
    mydb.close()

# creating a random id generator
def id_generator():
    mydb = sqlite3.connect('Student.db')
    c = mydb.cursor()
    while True:
        new_id = random.randint(10000, 99999)
        c.execute('SELECT * FROM ts WHERE user_id = ?', (new_id,))
        existing = c.fetchone()
        if existing is None:
            mydb.close()
            return new_id

# creating access root of the page
@app.route('/')
def index():
    return render_template('index.html')

# creating about page access
@app.route('/about')
def about():
    return render_template('about.html')

#creating login page access
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def user_login():
    name=request.form.get('username')
    password=request.form.get('password')

    mydb=sqlite3.connect('Student.db')
    c=mydb.cursor()
    c.execute("Select * from ts where name = ? and password = ?",(name,password))
    user=c.fetchone()
    mydb.close()
    if user:
        session['username'] = name
        return redirect('/students')
    else:
        return 'Invalid username or password' 


# creating backend of sign page
@app.route("/sign_up")
def submit_form():
    return render_template("sign_up.html") 
@app.route('/submit', methods=['GET', 'POST'])
def submit():  
    name = request.form.get('name')
    password=request.form.get('password')
    age = request.form.get('age')
    skills = ' | '.join(request.form.getlist('skills'))
    user_id = id_generator()
    mydb = sqlite3.connect('Student.db')
    cur = mydb.cursor()
    cur.execute("INSERT INTO ts (user_id,password, name, age, skills) VALUES (?, ?, ?, ?, ?)", (user_id, password, name, age, skills))
    mydb.commit()
    mydb.close()
    return "Data Recieved.."

# creating backend for viewing student details  
@app.route('/students')
def view_students():
    mydb = sqlite3.connect('Student.db')
    c = mydb.cursor()
    c.execute("SELECT * FROM ts")
    students = c.fetchall()
    mydb.close()
    return render_template('students.html', students=students)

# creating updating page like changing student details using id number and deleting the student details
@app.route("/update-form")
def update_form():
    return render_template("update.html")
@app.route('/update', methods=['POST'])
def update_student():
    ID=request.form['ID']
    newName=request.form['newName']
    newAge=request.form['newAge']
    newSkills = ' | '.join(request.form.getlist('newSkills'))
    
    mydb=sqlite3.connect('Student.db')
    c=mydb.cursor()
    if newName:
        c.execute("update ts set name = ? where user_id =?",(newName,ID))
    if newAge:
        c.execute("update ts set age = ? where user_id = ?",(newAge,ID))
    if newSkills:
        c.execute("update ts set skills = ? where user_id = ?",(newSkills,ID))

    mydb.commit()
    mydb.close()
    return "Student Record updated successfully..."


@app.route('/delete',methods=['POST'])
def delete_student():
    student_id = request.form['Id']

    #delete
    mydb=sqlite3.connect("Student.db")
    c=mydb.cursor()
    c.execute("Delete from ts where user_id = ?",(student_id,))
    mydb.commit()
    mydb.close()
    return "Deleted successfuly..."


if __name__ == '__main__':
    database()
    app.run(debug=True)

