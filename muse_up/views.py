from flask import Blueprint, render_template
from .models import Event
from datetime import datetime

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    EventStatus = Event.status
    currentdatetime = datetime.now()
    Allevents = Event.query.all()
    return render_template('index.html', Allevents=Allevents, currentdatetime=currentdatetime, EventStatus=EventStatus)