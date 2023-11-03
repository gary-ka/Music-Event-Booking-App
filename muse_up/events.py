from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, EventStatus, Booking
from .forms import CreateForm, CommentForm, EditForm, BookingForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user
from datetime import datetime


Eventbp = Blueprint('events', __name__, url_prefix='/events')

@Eventbp.route('/<id>')
def details(id):
    event= db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    form = CommentForm()    
    return render_template('events/details.html', event=event, form=form)

@Eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = CreateForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.event_name.data,
                  intro=form.event_introduction.data,
                  description=form.event_description.data,
                  musician=form.event_musician.data,
                  category=form.event_category.data,
                  location=form.event_location.data,
                  date=form.event_datetime.data,
                  price=form.event_cost.data,
                  availability=form.event_availabilities.data,
                  image=db_file_path,
                  status = EventStatus.OPEN,
                  user_id = current_user.id)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('events.myevents'))
  return render_template('events/create.html', form=form)

@Eventbp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
  print('Method type: ', request.method)
  event= db.session.query(Event).get_or_404(id)
  form = EditForm(event_name=event.name,
                    event_introduction=event.intro,
                    event_description=event.description,
                    event_musician=event.musician,
                    event_category=event.category,
                    event_location=event.location,
                    event_datetime=event.date,
                    event_cost=event.price,
                    event_availabilities=event.availability,
                    event_status = event.status,
                    event_photo=event.image)
  if form.validate_on_submit():
    event.name=form.event_name.data
    event.intro=form.event_introduction.data
    event.description=form.event_description.data
    event.musician=form.event_musician.data
    event.category=form.event_category.data
    event.location=form.event_location.data
    event.date=form.event_datetime.data
    event.price=form.event_cost.data
    event.availability=form.event_availabilities.data
    event.status = form.event_status.data
    event.user_id = current_user.id
    # commit to the database
    try:
      db.session.commit()  
      flash('Successfully edited event', 'success')
    except Exception as e:
      print("Error")
    #Always end with redirect when form is valid
    return redirect(url_for('events.edit_event', id=id))
  return render_template('events/edit.html', id=id, form=form)

def check_upload_file(form):
  #get file data from form  
  fp = form.event_photo.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

@Eventbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, 
                        event_id=id,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success') 
    # for debug use  
    # else:
    #   app=create_app()
    #   # Log the form validation errors to help identify the issue
    #   for field, errors in form.errors.items():
    #       for error in errors:
    #           app.logger.error(f"Validation error for field '{field}': {error}") 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('events.details', id=id))

@Eventbp.route('/cancel_event/<id>', methods=['GET','POST'])
@login_required
def cancel_event(id):
    event = Event.query.get_or_404(id)
    event.status = False
    db.session.commit()
    return redirect(url_for('events.myevent', id=id))

@Eventbp.route('/reopen_event/<id>')
@login_required
def reopen_event(id):
    event = Event.query.get_or_404(id)
    event.status = True
    db.session.commit()
    flash('Event has been Cancelled', 'Cancelled')
    return redirect(url_for('events/myevent.html'))

@Eventbp.route('/myevents')
@login_required
def myevents():
    EventStatus_enum = EventStatus
    currentdatetime = datetime.now()
    user_id = current_user.id
    myevents = Event.query.filter_by(user_id=user_id).all()
    return render_template('events/myevents.html', myevents=myevents, currentdatetime=currentdatetime, EventStatus_enum=EventStatus_enum)

@Eventbp.route('/book/<id>', methods=['GET','POST'])
@login_required
def book(id):
   form = BookingForm()
   if form.validate_on_submit():
      booking = Booking(num_tickets = form.booking_tickets.data,
                        card_name = form.booking_cardName.data,
                        card_num = form.booking_cardNo.data,
                        cvv = form.booking_cardCVV.data,
                        year = form.booking_cardYear.data,
                        month = form.Booking_cardMonth.data,
                        user_id = current_user.id,
                        event_id = id)
      db.session.add(booking) 
      db.session.commit()
      return redirect(url_for('events.mybookings'), form=form)
   return render_template('book.html', form=form)

@Eventbp.route('/mybookings')
@login_required
def mybookings():
   user_id = current_user.id
   bookings = Booking.query.filter_by(user_id=user_id).all()
   return render_template('history.html', bookings=bookings)
   
      







      
      