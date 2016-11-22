from flask_table import Table, Col

class EmployeeTable(Table):
        """Generating table view"""
        id = Col('#')
        name_first = Col('Name')
        name_second = Col('Surname')
        department_name = Col('Department')
        position_name = Col('Position')
        email = Col('Email')
        tel = Col('Tel')
        birth_date = Col('BD')

class PositionTable(Table):
        """Generating table view"""
        id = Col('#')
        position_name = Col('Position')
        about = Col('About')

class DepartmentTable(Table):
        """Generating table view"""
        id = Col('#')
        department_name = Col('Department')
        parental_department_name = Col('Parental Department')
        name_second = Col('Head of department')
        about = Col('About')