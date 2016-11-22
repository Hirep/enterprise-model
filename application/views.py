from flask import render_template, redirect, request
from application import tables
from application import app
from application import db
from application import models
from application import forms
import sqlalchemy.exc as Exc
from sqlalchemy import or_


@app.route('/')
def index():
    """doc"""
    return redirect('/employees')


@app.route('/employees')
def employees():
    """doc"""
    result = db.session.query(models.User.id,
                                models.User.name_first,
                                models.User.name_second,
                                models.Department.department_name,
                                models.Position.position_name,
                                models.User.email, models.User.tel,
                                models.User.birth_date) \
        .join(models.Department, models.Department.id == models.User.department_id, isouter=True) \
        .join(models.Position, models.Position.id == models.User.position_id, isouter=True)
    
    table = tables.EmployeeTable(result)
    return render_template('employees.html', table=table)


@app.route('/positions')
def positions():
    """doc"""
    result = db.session.query(models.Position)
    table = tables.PositionTable(result)
    return render_template('positions.html', table=table)


@app.route('/departments')
def departments():
    """doc"""
    
    # I couldn't handle this with ORM tools :( 
    result = db.engine.execute(" \
    SELECT d.id, d.department_name, j.department_name as parental_department_name, u.name_first, u.name_second, d.about \
    FROM departments d \
    LEFT JOIN departments j ON d.parental_department_id=j.id \
    JOIN users u ON d.head_id=u.id")

    table = tables.DepartmentTable(result)
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
    departments = db.session.query(models.Department).order_by(models.Department.id)
    positions = db.session.query(models.Position).order_by(models.Position.id)

    form = forms.AddUser(request.form)
    form.department_id.choices = [(dpt.id, dpt.department_name) for dpt in departments]
    form.position_id.choices = [(psn.id, psn.position_name) for psn in positions]
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
    departments = db.session.query(models.Department).order_by(models.Department.id)

    # select users who are NOT heads of departments
    users_available = db.session.query(models.User) \
            .join(models.Department, models.User.id == models.Department.head_id, isouter=True) \
            .filter(models.Department.head_id == None)

    form = forms.AddDepartment(request.form)
    form.parental_department_id.choices = [(dpt.id, dpt.department_name) for dpt in departments]
    form.head_id.choices = [(user.id, user.name_first +" "+ user.name_second) for user in users_available]

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

    departments = db.session.query(models.Department).order_by(models.Department.id)
    positions = db.session.query(models.Position).order_by(models.Position.id)

    if request.method == "GET":
        form = forms.AddUser(obj=user)
        form.department_id.choices = [(dpt.id, dpt.department_name) for dpt in departments]
        form.department_id.default = user.department_id
        form.position_id.choices = [(psn.id, psn.position_name) for psn in positions]
        form.position_id.default = user.position_id        
        return render_template('add_employee.html', form=form, id=id)

    if request.method == "POST":
        form = forms.AddUser(request.form)
        form.department_id.choices = [(dpt.id, dpt.department_name) for dpt in departments]
        form.position_id.choices = [(psn.id, psn.position_name) for psn in positions]
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

    departments = db.session.query(models.Department).filter(models.Department.id != id).order_by(models.Department.id)

    users_available = db.session.query(models.User) \
            .join(models.Department, models.User.id == models.Department.head_id, isouter=True) \
            .filter(or_(models.Department.head_id == None, models.Department.head_id == department.head_id))

    if request.method == "GET":
        form = forms.AddDepartment(obj=department)
        form.parental_department_id.choices = [(dpt.id, dpt.department_name) for dpt in departments]
        
        form.head_id.choices = [(user.id, user.name_first +" "+ user.name_second) for user in users_available]
        form.head_id.default = department.head_id
        return render_template('add_department.html', form=form, id=id)

    if request.method == "POST":
        form = forms.AddDepartment(request.form)
        form.parental_department_id.choices = [(dpt.id, dpt.department_name) for dpt in departments]
        form.head_id.choices = [(user.id, user.name_first +" "+ user.name_second) for user in users_available]
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
    
    # select users that are not heads of depts
    users_available = db.session.query(models.User) \
            .join(models.Department, models.User.id == models.Department.head_id, isouter=True) \
            .filter(models.Department.head_id == None)
    
    if request.method == "POST":
        form = forms.DeleteHead(request.form)
        form.head_id.choices = [(user.id, user.name_first +" "+ user.name_second) for user in users_available]
        if form.validate():
            try:
                # new head on duty
                department = list(db.session.query(models.Department).filter_by(head_id=id))[0]
                department.head_id = form.head_id.data

                # send new head to rule department
                usr = db.session.query(models.User).get(form.head_id.data)
                usr.department_id = department.id
                db.session.commit()
            except (Exc.IntegrityError, Exc.OperationalError) as err:
                db.session.rollback()
                return render_template('creation_failure.html', error=err)

    head = list(db.session.query(models.Department).filter_by(head_id=id))
    if head:
        form = forms.DeleteHead()
        form.head_id.choices = [(user.id, user.name_first +" "+ user.name_second) for user in users_available]
        return render_template("delete_head.html", form=form, department=head[0].department_name, id=id)
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
    
    # select list of positions available to substitute deleted
    positions = [(psn.id, psn.position_name) for psn in db.session.query(models.Position).filter(models.Position.id != id)]

    if request.method == "POST":
        print("Here2")
        
        form = forms.DeletePosition(request.form)
        form.position_id.choices = list(positions)
        if form.validate():
            try:
                # substitute deleted position with selected
                for usr in db.session.query(models.User).filter_by(position_id=id):
                    usr.position_id = form.position_id.data
                
                db.session.delete(position)
                db.session.commit()
                return render_template("creation_success.html")
            except (Exc.IntegrityError, Exc.OperationalError) as err:
                db.session.rollback()
                return render_template('creation_failure.html', error=err)

    form = forms.AddUser(request.form)
    form.position_id.choices = positions
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
    
    if department.parental_department_id:
        try:
            # if parental dep exists -> transfer all employees there
            for usr in db.session.query(models.User).filter_by(department_id=id):
                usr.department_id = department.parental_department_id
            
            # apply transition rule on departments
            for dpt in db.session.query(models.Department).filter_by(parental_department_id=department.id):
                dpt.parental_department_id =  department.parental_department_id

            db.session.delete(department)
            db.session.commit()
            return render_template('creation_success.html')
        except (Exc.IntegrityError, Exc.OperationalError) as err:
            db.session.rollback()
            return render_template('creation_failure.html', error=err)
    else:
        try:
            # make 'unemployed' users whose parentless department was deleted 
            for usr in db.session.query(models.User).filter_by(department_id=id):
                usr.department_id = None
            db.session.delete(department)
            db.session.commit()
            return render_template('creation_success.html')
        except (Exc.IntegrityError, Exc.OperationalError) as err:
            db.session.rollback()
            return render_template('creation_failure.html', error=err)