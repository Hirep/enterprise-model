from flask import render_template, redirect, request
from flask_table import Table, Col
from application import app
from application import db
from application import models
from application import forms
import sqlalchemy.exc as Exc


@app.route('/')
def index():
    """doc"""
    return redirect('/employees')


@app.route('/employees')
def employees():
    """doc"""

    class ItemTable(Table):
        """Generating table view"""
        id = Col('#')
        name_first = Col('Name')
        name_second = Col('Surname')
        department_name = Col('Department')
        position_name = Col('Position')
        email = Col('Email')
        tel = Col('Tel')
        birth_date = Col('BD')

    result = db.engine.execute(" \
    SELECT u.id, u.name_first, u.name_second, d.department_name, p.position_name, u.email, u.tel, u.birth_date  \
     FROM users u \
     LEFT JOIN departments d ON d.id=u.department_id \
     LEFT JOIN positions   p ON p.id=u.position_id")
    table = ItemTable(result)
    return render_template('employees.html', table=table)


@app.route('/positions')
def positions():
    """doc"""
    class ItemTable(Table):
        """Generating table view"""
        id = Col('#')
        position_name = Col('Position')
        about = Col('About')

    result = db.engine.execute("SELECT * FROM positions")

    table = ItemTable(result)
    return render_template('positions.html', table=table)


@app.route('/departments')
def departments():
    """doc"""
    class ItemTable(Table):
        """Generating table view"""
        id = Col('#')
        department_name = Col('Department')
        parental_department_name = Col('Parental Department')
        name_second = Col('Head of department')
        about = Col('About')

    result = db.engine.execute(" \
    SELECT d.id, d.department_name, j.department_name as parental_department_name, u.name_first, u.name_second, d.about \
    FROM departments d \
    LEFT JOIN departments j ON d.parental_department_id=j.id \
    JOIN users u ON d.head_id=u.id")

    table = ItemTable(result)
    return render_template('departments.html', table=table)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    """doc"""
    departments = db.engine.execute(
        "SELECT d.id, d.department_name FROM departments d ORDER BY d.id")
    positions = db.engine.execute(
        "SELECT p.id, p.position_name FROM positions p ORDER BY p.id")
    form = forms.AddUser(request.form)
    form.department_id.choices = list(departments)
    form.position_id.choices = list(positions)

    if request.method == "POST":
        if form.validate():
            user = models.User( name_first=form.name_first.data,
                                name_second=form.name_second.data,
                                department_id=form.department_id.data,
                                position_id=form.position_id.data,
                                email=form.email.data,
                                tel=form.tel.data,
                                birth_date=form.birth_date.data)
            try:
                db.session.add(user)
                db.session.commit()
                return render_template('creation_success.html')
            except Exc.IntegrityError as err:
                return render_template('creation_failure.html', error=err)
    return render_template('add_employee.html', form=form)


@app.route('/positions/add', methods=['GET', 'POST'])
def add_position():
    """doc"""
    form = forms.AddPosition(request.form)
    if request.method == "POST":
        if form.validate():
            position = models.Position(position_name=form.position_name.data, about=form.about.data)
            try:
                db.session.add(position)
                db.session.commit()
                return render_template('creation_success.html')
            except Exc.IntegrityError as err:
                return render_template('creation_failure.html', error=err)
    return render_template('add_position.html', form=form)


@app.route('/departments/add', methods=['GET', 'POST'])
def add_department():
    """doc"""
    departments = db.engine.execute(" \
    SELECT d.id, d.department_name FROM departments d ORDER BY d.id")

    # select users who are NOT heads of departments
    users_available = db.engine.execute(" \
    SELECT u.id, u.name_first, u.name_second \
    FROM users u \
    LEFT JOIN departments d ON u.id=d.head_id \
    WHERE d.head_id is null \
    ORDER BY u.id")

    form = forms.AddDepartment(request.form)
    form.parental_department_id.choices = list(departments)
    form.head_id.choices = [(user[0], user[1] + ' ' + user[2])
                            for user in users_available]

    if request.method == "POST":
        if form.validate():
            department = models.Department( department_name=form.department_name.data,
                                            parental_department_id=form.parental_department_id.data,
                                            head_id=form.head_id.data,
                                            about=form.about.data)
            try:
                db.session.add(department)
                db.session.commit()
                return render_template('creation_success.html')
            except Exc.IntegrityError as err:
                return render_template('creation_failure.html', error=err)

    return render_template('add_department.html', form=form)


@app.route('/employees/edit/<id>', methods=['GET', 'POST'])
def emloyee_edit(id):
    try:
        id = int(id)
    except ValueError:
        return render_template('404.html'), 404

    user = models.User.query.get(int(id))
    
    if not user:
        return render_template('404.html'), 404

    departments = db.engine.execute(
        "SELECT d.id, d.department_name FROM departments d ORDER BY d.id")
    positions = db.engine.execute(
        "SELECT p.id, p.position_name FROM positions p ORDER BY p.id")

    if request.method == "GET":
        form = forms.AddUser(obj=user)
        form.department_id.choices = list(departments)
        form.department_id.default = user.department_id
        form.position_id.choices = list(positions)
        form.position_id.default = user.position_id        
        return render_template('add_employee.html', form=form, id=id)

    if request.method == "POST":
        form = forms.AddUser(request.form)
        form.department_id.choices = list(departments)
        form.position_id.choices = list(positions)
        print(form.data)
        if form.validate():
            try:
                print("here")
                user.name_first = form.name_first.data
                user.name_second = form.name_second.data
                user.department_id = form.department_id.data
                user.position_id = form.position_id.data
                user.email = form.email.data
                user.tel = form.tel.data
                user.birth_date = form.birth_date.data
                db.session.commit()
                return render_template('creation_success.html')
            except (Exc.IntegrityError, Exc.OperationalError) as err:
                db.session.rollback()
                return render_template('creation_failure.html', error=err)


@app.route('/positions/edit/<id>', methods=['GET', 'POST'])
def position_edit(id):
    try:
        id = int(id)
    except ValueError:
        return render_template('404.html'), 404
        
    position = models.Position.query.get(int(id))
    
    if not position:
        return render_template('404.html'), 404

    if request.method == "GET":
        form = forms.AddPosition(obj=position)
        return render_template('add_position.html', form=form, id=id)

    if request.method == "POST":
        form = forms.AddPosition(request.form)
        if form.validate():
            try:
                position.position_name = form.position_name.data
                position.about = form.about.data
                db.session.commit()
                return render_template('creation_success.html')
            except Exc.IntegrityError as err:
                return render_template('creation_failure.html', error=err)
                        


@app.route('/departments/edit/<id>', methods=['GET', 'POST'])
def department_edit(id):
    try:
        id = int(id)
    except ValueError:
        return render_template('404.html'), 404

    department = models.Department.query.get(int(id))
    
    if not department:
        return render_template('404.html'), 404

    departments = db.engine.execute(
        "SELECT d.id, d.department_name FROM departments d WHERE d.id != :id ORDER BY d.id", id=id)
    users_available = db.engine.execute(" \
    SELECT u.id, u.name_first, u.name_second \
    FROM users u \
    LEFT JOIN departments d ON u.id=d.head_id \
    WHERE d.head_id is null OR d.head_id is :id \
    ORDER BY u.id", id=department.head_id)

    if request.method == "GET":
        form = forms.AddDepartment(obj=department)
        form.parental_department_id.choices = list(departments)
        
        form.head_id.choices = [(user[0], user[2])
                            for user in users_available]
        form.head_id.default = department.head_id
        return render_template('add_department.html', form=form, id=id)

    if request.method == "POST":
        form = forms.AddDepartment(request.form)
        form.parental_department_id.choices = list(departments)
        form.head_id.choices = [(user[0], user[2])
                            for user in users_available]
        if form.validate():
            try:
                department.department_name = form.department_name.data
                department.parental_department_id = form.parental_department_id.data
                department.head_id = form.head_id.data
                department.about = form.about.data
                db.session.commit()
                return render_template('creation_success.html')
            except (Exc.IntegrityError, Exc.OperationalError) as err:
                db.session.rollback()
                return render_template('creation_failure.html', error=err)



@app.route('/employees/delete/<id>', methods=["GET", "POST"])
def emloyee_delete(id):
    try:
        id = int(id)
    except ValueError:
        return render_template('404.html'), 404

    user = models.User.query.get(int(id))
    
    if not user:
        return render_template('404.html'), 404

    if request.method == "POST":
        users_available = db.engine.execute(" \
            SELECT u.id, u.name_first, u.name_second \
            FROM users u \
            LEFT JOIN departments d ON u.id=d.head_id \
            WHERE d.head_id is null \
            ORDER BY u.id")
        form = forms.DeleteHead(request.form)
        form.head_id.choices = [(user[0], user[1] +" "+ user[2]) for user in users_available]
        if form.validate():
            try:
                dep = db.engine.execute("SELECT * FROM departments WHERE departments.head_id= :id", id=id)
                dep = dep.fetchall()
                # get department_id where head is 'id'
                dep = dep[0][0]
                department = models.Department.query.get(dep)
                department.head_id = form.head_id.data
                db.session.commit()
            except (Exc.IntegrityError, Exc.OperationalError) as err:
                db.session.rollback()
                return render_template('creation_failure.html', error=err)

    head = db.engine.execute("SELECT * FROM departments WHERE departments.head_id= :id", id=id)
    head = head.fetchall()
    if head:
        users_available = db.engine.execute(" \
            SELECT u.id, u.name_first, u.name_second \
            FROM users u \
            LEFT JOIN departments d ON u.id=d.head_id \
            WHERE d.head_id is null \
            ORDER BY u.id")
        # get name of department
        department = head[0][1]
        form = forms.DeleteHead()
        form.head_id.choices = [(user[0], user[1] +" "+ user[2]) for user in users_available]
        return render_template("delete_head.html", form=form, department=department, id=id)
    else:
        try:
            db.session.delete(user)
            db.session.commit()
            return render_template('creation_success.html')
        except (Exc.IntegrityError, Exc.OperationalError) as err:
            db.session.rollback()
            return render_template('creation_failure.html', error=err)

    


@app.route('/positions/delete/<id>', methods=["GET", "POST"])
def position_delete(id):
    try:
        id = int(id)
    except ValueError:
        return render_template('404.html'), 404
    
    position = models.Position.query.get(int(id))

    if not position:        
        return render_template('404.html'), 404
    
    positions = db.engine.execute(
        "SELECT p.id, p.position_name FROM positions p WHERE p.id is not :id ORDER BY p.id", id=id)
    
    if request.method == "POST":
        print("Here2")
        
        form = forms.DeletePosition(request.form)
        form.position_id.choices = list(positions)
        if form.validate():
            try:
                users = db.engine.execute("UPDATE users \
                    SET position_id= :position_id \
                    WHERE position_id= :id", id=id, position_id=form.position_id.data 
                    )
                db.session.delete(position)
                db.session.commit()
                return render_template("creation_success.html")
            except (Exc.IntegrityError, Exc.OperationalError) as err:
                db.session.rollback()
                return render_template('creation_failure.html', error=err)


    positions = db.engine.execute(
        "SELECT p.id, p.position_name FROM positions p WHERE p.id is not :id ORDER BY p.id", id=id)
    form = forms.AddUser(request.form)
    form.position_id.choices = list(positions)
    return render_template("delete_position.html", form=form, position=position.position_name, id=id)
  

@app.route('/departments/delete/<id>')
def department_delete(id):
    try:
        id = int(id)
    except ValueError:
        return render_template('404.html'), 404

    department = models.Department.query.get(int(id))
    
    if not department:
        return render_template('404.html'), 404
    
    # if parental dep exists -> transfer all employees there
    if department.parental_department_id:
        try:
            users = db.engine.execute("UPDATE users \
                    SET department_id= :parental_id \
                    WHERE department_id= :id", id=id, parental_id=department.parental_department_id 
                    )
            db.session.delete(department)
            db.session.commit()
            return render_template('creation_success.html')
        except (Exc.IntegrityError, Exc.OperationalError) as err:
            db.session.rollback()
            return render_template('creation_failure.html', error=err)
    else:
        try:
            users = db.engine.execute("UPDATE users \
                SET department_id=NULL \
                WHERE department_id= :id", id=id 
                )
            db.session.delete(department)
            db.session.commit()
            return render_template('creation_success.html')
        except (Exc.IntegrityError, Exc.OperationalError) as err:
            db.session.rollback()
            return render_template('creation_failure.html', error=err)