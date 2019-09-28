from flask import Flask, render_template, request, url_for, redirect, flash
from Employee import Employee
import sqlite3

app = Flask(__name__)
app.secret_key = 'don tell anybody'


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        if request.form['first'] and request.form['last'] and request.form['pay']:
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            first = request.form['first']
            last = request.form['last']
            pay = request.form['pay']
            emp = Employee(first, last, pay)
            with conn:
                c.execute("INSERT INTO employee VALUES (?,?,?)", (emp.first, emp.last, emp.pay))
                flash("Employee {} {} has been added to database".format(emp.first, emp.last))
            return redirect('show')
        else:
            flash("You haven't provide all valuses")
            return redirect('home')
    return render_template("home.html")

@app.route('/find', methods=['POST', 'GET'])
def find():
    if request.method == 'POST':
        if 'findInput' in request.form:
            input = request.form['findInput']
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            with conn:
                c.execute("SELECT * FROM employee WHERE last = '{}'".format(input))
                flash("There is no any {} employee".format(input))
            query = c.fetchall()
            return render_template('show.html', query=query)

@app.route('/show')
def show():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    with conn:
        c.execute("SELECT * FROM employee")
        query = c.fetchall()
        c.execute("SELECT Count(*) from employee")
        amountofemployee = c.fetchall()
    return render_template('show.html', query=query, amountofemployee = amountofemployee)


@app.route('/remove', methods=['POST'])
def remove():
    if request.method == 'POST':
        lastname = request.form['lastremove']
        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        c.execute("SELECT last from employee WHERE last ='{}'".format(lastname))
        #check if the list form query is empty
        if not c.fetchall():
            flash("Ther is no any {} employee".format(lastname))
            c.execute("SELECT * FROM employee")
            query = c.fetchall()
            return render_template('show.html', query=query)
        else:
            with conn:
                c.execute("DELETE FROM employee WHERE last ='{}'".format(lastname))
            c.execute("SELECT * FROM employee")
            query = c.fetchall()
            flash("Employee {} has been removed".format(lastname))
            return render_template('show.html', query=query)


@app.route('/sort', methods=['POST'])
def sort():
    if request.method == 'POST':
        if 'sort-by-last-up' in request.form:
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            with conn:
                # no case carre
                c.execute("SELECT * FROM employee ORDER BY last COLLATE NOCASE")
            query = c.fetchall()
            return render_template('show.html', query=query)
        elif 'sort-by-last-down' in request.form:
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            with conn:
                # no case carre
                c.execute("SELECT * FROM employee ORDER BY last COLLATE NOCASE DESC")
            query = c.fetchall()
            return render_template('show.html', query=query)


@app.route('/sortbyname', methods=['POST'])
def sortbyname():
    if request.method == 'POST':
        if 'sort-by-name-up' in request.form:
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            with conn:
                # no case carre
                c.execute("SELECT * FROM employee ORDER BY first COLLATE NOCASE DESC")
            query = c.fetchall()
            return render_template('show.html', query=query)
        elif 'sort-by-name-down' in request.form:
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            with conn:
                # no case carre
                c.execute("SELECT * FROM employee ORDER BY first COLLATE NOCASE")
            query = c.fetchall()
            return render_template('show.html', query=query)


@app.route('/sortbysalary', methods=['POST'])
def sortbysalary():
    if request.method == 'POST':
        if 'sort-up-salary' in request.form:
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            with conn:
                # no case carre
                c.execute("SELECT * FROM employee ORDER BY pay COLLATE NOCASE DESC")
            query = c.fetchall()
            return render_template('show.html', query=query)
        elif 'sort-down-salary' in request.form:
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            with conn:
                # no case carre
                c.execute("SELECT * FROM employee ORDER BY pay COLLATE NOCASE")
            query = c.fetchall()
            return render_template('show.html', query=query)


@app.route('/set', methods=['POST'])
def set():
    if request.method == 'POST':
        if request.form['first'] and request.form['last'] and request.form['pay']:
            first = request.form['first']
            last = request.form['last']
            pay = request.form['pay']
            emp = Employee(first, last, pay)
            conn = sqlite3.connect('employees.db')
            c = conn.cursor()
            c.execute("SELECT * FROM employee WHERE first='{}' AND last='{}'".format(first, last))
            if not c.fetchall():
                flash("There is no any {} {} employee".format(first, last))
            else:
                with conn:
                    c.execute(
                        """UPDATE employee SET pay = '{}' WHERE first = '{}' AND last ='{}'""".format(emp.pay,
                                                                                                      emp.first,
                                                                                                      emp.last))
                c.execute('SELECT * FROM employee')
                flash("{} {}'s salary has been changed".format(emp.first, emp.last))
            c.execute('SELECT * FROM employee')
            query = c.fetchall()
            return render_template('show.html', query=query)
        else:
            flash("You haven't provide all valuses")
            return redirect('show')


if __name__ == '__name__':
    app.run(DEBUG=True)
