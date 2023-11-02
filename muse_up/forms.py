
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, DateTimeField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg', 'jfif'}

#Creates the 'Create Event' Form
class CreateForm(FlaskForm):
    event_name = StringField('Name your event', validators=[InputRequired('Enter Event Title'), Length(min = 1, max = 20)])
    event_photo = FileField('Destination Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    event_introduction = StringField('Introduce your event', validators=[InputRequired('Please enter event introduction'), Length(min = 1, max = 100)])
    event_musician = StringField('Musicians', validators = [InputRequired('Enter a musician'), Length(min = 1, max = 100)])
    event_description = TextAreaField('Describe your event', validators=[InputRequired('Enter event description'), Length(min = 1, max = 1000)])
    event_category = SelectField('Music Categories', validators=[InputRequired('Enter music category')], choices=[('text','Pop'), ('text','Classical'), ('text','Jazz'), ('text','Rock'), ('text','Country'), ('text','Hip Hop')])
    event_location = StringField('Location', validators = [InputRequired('Enter Location'), Length(min = 1, max = 100)])
    event_datetime = DateTimeField('Event Date and Time', format='%Y-%m-%dT%H:%M',validators = [InputRequired('Enter date and time')])
    event_cost = IntegerField('Ticket Cost')
    event_availabilities = IntegerField('Ticket Availabilities', validators = [InputRequired('Enter Ticket Availabilities')])
    event_submit = SubmitField("Create My Event")

# Form for Editing Events
class EditForm(FlaskForm):
    event_name = StringField('Name your event', validators=[InputRequired('Enter Event Title'), Length(min = 1, max = 20)])
    event_photo = FileField('Destination Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    event_introduction = StringField('Introduce your event', validators=[InputRequired('Please enter event introduction'), Length(min = 1, max = 100)])
    event_musician = StringField('Musicians', validators = [InputRequired('Enter a musician'), Length(min = 1, max = 100)])
    event_description = TextAreaField('Describe your event', validators=[InputRequired('Enter event description'), Length(min = 1, max = 1000)])
    event_category = SelectField('Music Categories', validators=[InputRequired('Enter music category')], choices=[('text','Pop'), ('text','Classical'), ('text','Jazz'), ('text','Rock'), ('text','Country'), ('text','Hip Hop')])
    event_location = StringField('Location', validators = [InputRequired('Enter Location'), Length(min = 1, max = 100)])
    event_datetime = DateTimeField('Event Date and Time', format='%Y-%m-%dT%H:%M',validators = [InputRequired('Enter date and time')])
    event_cost = IntegerField('Ticket Cost')
    event_availabilities = IntegerField('Ticket Availabilities', validators = [InputRequired('Enter Ticket Availabilities')])
    event_submit = SubmitField("Create My Event")


#Creates the 'Booking' Form
class BookingForm(FlaskForm):
    booking_tickets = IntegerField('Number of Tickets', validators=[InputRequired('Enter Number of Tickets')])
    booking_cardName = StringField('Card Nameholder', validators=[InputRequired('Enter Card Nameholder')])
    booking_cardNo = IntegerField('Card Number', validators=[InputRequired('Enter Card Number'), Length(min=12, max=12)])
    booking_cardCVV = IntegerField('Card CVV', validators = [InputRequired('Enter Card CVV'), Length(min=3,max=3)])
    Booking_cardMonth = SelectField('Expiry Month', validators=[InputRequired('Enter Card Expiry Month')], choices=[('text', 'January'), 
                                                                                                                    ('text', 'February'), 
                                                                                                                    ('text', 'March'), 
                                                                                                                    ('text', 'April'), 
                                                                                                                    ('text', 'May'), 
                                                                                                                    ('text', 'June'), 
                                                                                                                    ('text', 'July'), 
                                                                                                                    ('text', 'August'), 
                                                                                                                    ('text', 'September'), 
                                                                                                                    ('text', 'October'), 
                                                                                                                    ('text', 'November'), 
                                                                                                                    ('text', 'December')])
    booking_cardYear = IntegerField('Expiry Year', validators= [InputRequired('Enter Card Expiry Year'), Length(min=4, max= 4)])

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone = StringField("Contact Number", validators=[InputRequired(), Length(min=8, max=10)])
    address = StringField("Address", validators=[InputRequired()])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Post')