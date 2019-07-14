from flask import render_template, Blueprint, request, redirect, url_for
from flask_wtf import Form
from flask_table import Table, Col, LinkCol, DatetimeCol
from wtforms import TextField, IntegerField, SubmitField
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from services.igniter import ignite

home_api = Blueprint('home_api', __name__, template_folder='templates')
db = TinyDB('db.json')
table = db.table('fireworks')
scheduler = BackgroundScheduler()
scheduler.start()

class ConfigForm(Form):
    name = TextField("Firework")
    channel = IntegerField("Channel")
    length_seconds = IntegerField("Time in Seconds")
    submit = SubmitField('Submit')

class FireworksTable(Table):
    name = Col('Firework')
    channel = Col('Channel')
    length_seconds = Col('Time in Seconds')
    edit_link = LinkCol('Edit', '.edit_config', url_kwargs=dict(id='channel'))
    delete_link = LinkCol('Delete', '.delete_config', url_kwargs=dict(id='channel'))

class FireworksScheduleTable(Table):
    name = Col('Firework')
    channel = Col('Channel')
    run_date = DatetimeCol('Scheduled to Fire', datetime_format='long')

@home_api.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@home_api.route('/control', methods=['GET'])
def control():
    return render_template('control.html')

@home_api.route('/show/config/edit/<int:id>', methods=['GET'])
def edit_config(id):
   print("got id", id)
   Firework = Query()
   f = table.get(Firework.channel == id)
   form = ConfigForm()
   form.channel.data = f['channel']
   form.name.data = f['name']
   form.length_seconds.data = f['length_seconds']
   return render_template('config.html', form=form, method='POST', ft=url_for('.update_config', id=id))

@home_api.route('/show/config/delete/<int:id>', methods=['GET'])
def delete_config(id):
   Firework = Query()
   table.remove(Firework.channel == id)
   return redirect(url_for('.show_list'))

@home_api.route('/show/config/update/<int:id>', methods=['POST'])
def update_config(id):
   form = ConfigForm()
   Firework = Query()
   table.update({'channel': form.channel.data, 'name': form.name.data, 'length_seconds': form.length_seconds.data}, Firework.channel==id)
   return redirect(url_for(".show_list"))

@home_api.route('/show/config', methods=['GET', 'POST'])
def show_config():
   form = ConfigForm()
   
   if request.method == 'POST':
      if form.validate() == False:
         return render_template('config.html', form = form, method='POST', ft=url_for('.show_config'))
      else:
         table.insert({'channel': form.channel.data, 'name': form.name.data, 'length_seconds': form.length_seconds.data})
         return redirect(url_for(".show_list"))
   elif request.method == 'GET':
      return render_template('config.html', form = form, method='POST', ft=url_for('.show_config'))

@home_api.route('/show/list', methods=['GET'])
def show_list():
   fireworks = table.all()
   for f in fireworks:
      f['edit_link'] = url_for(".edit_config", id=f['channel'])
      f['delete_link'] = url_for(".delete_config", id=f['channel'])
   return render_template('config_list.html', table=FireworksTable(fireworks))

@home_api.route('/show/run', methods=['GET'])
def show_run():
   fireworks = table.all()
   total_seconds = 5
   for f in fireworks:
      run_date=datetime.now() + timedelta(seconds=total_seconds)
      f['run_date'] = run_date
      total_seconds = total_seconds + f['length_seconds']
      schedule_job(f['channel'], f['name'], f['run_date'])

   return render_template('show_schedule.html', table=FireworksScheduleTable(fireworks))

def schedule_job(channel, name, run_date):
      scheduler.add_job(lambda: open_channel(channel, name), 'date', run_date=run_date, id=str(channel))

def open_channel(channel, name):
   print("Running channel", channel, "for firework named", name)
   ignite(str(channel-1))
