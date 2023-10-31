from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import CreateForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

Eventbp = Blueprint('events', __name__, url_prefix='/events')

@Eventbp.route('/<id>')
def details(id):
    Event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    form = CommentForm()    
    return render_template('events/details.html', events=Event, form=form)

@Eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = CreateForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(EventName=form.event_name.data,
                  EventIntro=form.event_introduction.data,
                  EventDescription=form.event_description.data,
                  EventMusician=form.event_musician.data,
                  EventCategory=form.event_category.data,
                  EventLocation=form.event_location.data,
                  EventDateTime=form.event_datetime.data,
                  EventCost=form.event_cost.data,
                  EventAvailability=form.event_availabilities.data,
                  Eventimage=db_file_path)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('events.create'))
  return render_template('events/create.html', form=form)

@Eventbp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event():
  print('Method type: ', request.method)
  event = Event.query.get_or_404(id)
  form = CreateForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    pass
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('events.edit'))
  return render_template('events/edit.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

@Eventbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(Commenttext=form.text.data, 
                        event=event,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('events.details', id=id))

@Eventbp.route('/cancel_event/<id>')
@login_required
def cancel_event(id):
    event = Event.query.get_or_404(id)
    event.status = False
    db.session.commit()
    return redirect(url_for('events/myevent.html'))

@Eventbp.route('/cancel_event/<id>')
@login_required
def cancel_event(id):
    event = Event.query.get_or_404(id)
    event.status = True
    db.session.commit()
    return redirect(url_for('events/myevent.html'))

@Eventbp.route('/myevents')
@login_required
def myevents():
    return render_template('events/myevents.html')