from application import db
from application.models import User, Position, Department
import datetime

db.create_all()

pos1 = Position(position_name='Private Coder', about='The lowest rank in enterprise hierarchy')
db.session.add(pos1)

pos2 = Position(position_name='Head of department', about='This rank empowers you to kick your slaves')
db.session.add(pos2)

dpt1 = Department(department_name='Hydra Zero Research',
                    head_id=1,
                    parental_department_id=3,
                    about='Some crazy things')
db.session.add(dpt1)

dpt2 = Department(department_name='Election Department',
                    head_id=2,
                    parental_department_id=3,                    
                    about='Make America Great Again!')
db.session.add(dpt2)

dpt3 = Department(department_name='Technical Department',
                    head_id=5,
                    about='-')
db.session.add(dpt3)


# usr1 = User(name_first='Rufus',
#                 name_second='Sixsmith',
#                 department_id=1,
#                 position_id=2,
#                 email='rufus.hydra.zero@q.uk',
#                 tel='+380001234567',
#                 birth_date=datetime.datetime.utcnow()
#                                 )
# db.session.add(usr1)

# usr2 = User(name_first='Donald',
#                 name_second='Trump',
#                 department_id=2,
#                 position_id=2,
#                 email='pussy.grabber@us.gov',
#                 tel='+380001234569',
#                 birth_date=datetime.datetime.utcnow()
#                                 )
# db.session.add(usr2)

# usr3 = User(name_first='Brett',
#                 name_second='Cannon',
#                 department_id=1,
#                 position_id=1,
#                 email='tall.canadian@py.ca',
#                 tel='+380001232469',
#                 birth_date=datetime.datetime.utcnow()
#                                 )
# db.session.add(usr3)

# usr4 = User(name_first='Lorne',
#                 name_second='Malvo',
#                 department_id=2,
#                 position_id=1,
#                 email='fargoslayer@us.com',
#                 tel='+380001632469',
#                 birth_date=datetime.datetime.utcnow()
#                                 )
# db.session.add(usr4)

# usr5 = User(name_first='Elon',
#                 name_second='Musk',
#                 department_id=3,
#                 position_id=2,
#                 email='mars2020@us.com',
#                 tel='+380011632469',
#                 birth_date=datetime.datetime.utcnow()
#                                 )
# db.session.add(usr5)

try:
    db.session.commit()
except TypeError:
    db.session.rollback()
