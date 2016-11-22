from wtforms import Form, validators, TextField, TextAreaField, SelectField, DateTimeField
from wtforms.fields.html5 import EmailField

class AddUser(Form):

    name_first = TextField("Name", [validators.Length(min=2, max=25)])
    name_second = TextField("Surname", [validators.Length(min=2, max=25)])
    department_id = SelectField("Department", coerce=int)
    position_id = SelectField("Position", coerce=int)
    email = EmailField("Email address", [validators.DataRequired(), validators.Email()])
    tel = TextField("Tel", [validators.Length(13)])
    birth_date = DateTimeField("Birthday", format="%m/%d/%Y", validators=(validators.Optional(),))


class AddPosition(Form):

    position_name = TextField("Position", [validators.Length(min=2, max=25)])
    about = TextAreaField("About")

class AddDepartment(Form):

    department_name = TextField("Name", [validators.Length(min=2, max=25)])
    parental_department_id = SelectField("Parental Department", coerce=int)
    head_id = SelectField("Head", coerce=int)
    about = TextAreaField("About")

class DeleteHead(Form):
    head_id = SelectField("Head", [validators.DataRequired()], coerce=int)

class DeletePosition(Form):
    position_id = SelectField("Position", [validators.DataRequired()], coerce=int)