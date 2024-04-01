from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

# Define the Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Employee {self.name}>'

# Routes
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    department = request.form['department']
    new_employee = Employee(name=name, email=email, phone=phone, department=department)
    db.session.add(new_employee)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.phone = request.form['phone']
        employee.department = request.form['department']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('update.html', employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_employee')
def add_employee_page():
    return render_template('add_employee.html')

if __name__ == '__main__':
    # Drop and recreate the tables to reflect schema changes
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
