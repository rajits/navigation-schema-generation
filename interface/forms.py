from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class InputForm(Form):
    name_of_app = TextField('name_of_app', validators = [Required()])
  # remember_me = BooleanField('remember_me', default = False)
    destinations = TextField('destinations')
    tabs = TextField('tabs')
