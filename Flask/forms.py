from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class dns_service(FlaskForm):
      dns_name= StringField("DNS_Name", validators=[DataRequired(), Length(min=2, max=20)])
      
      
      
class record_list(FlaskForm):
      listing_record= TextAreaField("Record Set")
      submit=SubmitField("Back")
 

class dnscreate(FlaskForm):
      name= StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])
      value= StringField("Routing IP", validators=[DataRequired(), Length(min=2, max=20)])
      submit=SubmitField("Create")
      

class dnsdelete(FlaskForm):
      name= StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])
      value= StringField("Routing IP", validators=[DataRequired(), Length(min=2, max=20)])
      submit=SubmitField("Delete")
