import sqlite3

from flask import Flask, render_template, request, g

app = Flask(__name__)


def get_db():
     conn = g._database = sqlite3.connect('appt_tracker.db')
     conn.execute('''PRAGMA foreign_keys = 1''')
     conn.row_factory = sqlite3.Row

     return conn


@app.teardown_appcontext
def close_connection(exception):
     conn = getattr(g, '_database', None)
     if conn is not None:
          conn.close()


@app.route('/login')
def login():
     return render_template('login.html', )


@app.route('/logout')
def logout():
     return

@app.route('/', methods=['GET'])
def homepage():
     locations = ["Carle", "UIUC", "Peoria"]
     times = [
          "08:00 AM",
          "08:30 AM",
          "09:00 AM",
          "09:30 AM",
          "10:00 AM",
          "10:30 AM",
          "11:00 AM",
          "11:30 AM",
          "12:00 PM",
          "12:30 PM",
          "01:00 PM",
          "01:30 PM",
          "02:00 PM",
          "02:30 PM",
          "03:00 PM",
          "03:30 PM",
          "04:00 PM",
          "04:30 PM",
          "05:00 PM",
          "05:30 PM",
          "06:00 PM",
     ]
     return render_template('appointments.html', locations=locations, times=times)


@app.route('/list', methods=['GET'])
def list_available_appointments():
     query = '''SELECT a.id, a.date, a.time, l.name AS location
     FROM APPOINTMENTS a INNER JOIN LOCATIONS l
     ON a.location = l.id
     WHERE a.id NOT IN (
     	SELECT appointment
     	FROM USER_APPOINTMENTS
     	GROUP BY
     		appointment
     	HAVING COUNT(appointment) >= 25)'''

     location = request.args.get('location')
     if location:
          query += ' AND l.name = "' + location + '"'

     date = request.args.get('date')
     if date:
          query += ' AND a.date = "' + date + '"'

     time = request.args.get('time')
     if time:
          query += ' AND a.time = "' + time + '"'

     cur = get_db().cursor()
     cur.execute(query)

     results = cur.fetchall()
     cur.close()

     available_slots = [{
          "id": row['id'],
          "date": row['date'],
          "time": row['time'],
          "location": row['location']} for row in results
     ]

     return {"available_slots": available_slots}


@app.route('/submit', methods=['POST'])
def submit_appointment():
     # TODO: here need to get the current user name;
     # TODO: hard code jane smith single user
     person = "Jane Smith"
     if request.get_json() and request.get_json()['appt_id']:
          appt = request.get_json()['appt_id']
     else:
          # TODO populate the error message to frontend
          raise ValueError("Apppointment Id is a required field!")

     conn = get_db()
     cur = conn.cursor()

     # get the current user id
     cur.execute("SELECT id FROM USERS WHERE fname = (?)", (person.split(' ')[0],))
     # TODO error handling what if that user doesn't exist
     user_id = cur.fetchone()

     # get the appt id
     cur.execute("SELECT id FROM APPOINTMENTS WHERE id = (?)", (appt,))
     # TODO error handling what if that appointment id doesn't exist
     appt_id = cur.fetchone()

     # INSERT IF MAX 25 NOT REACHED PER APPOINTMENT ID
     cur.execute('''
     	SELECT COUNT(appointment) as count_appt
     	FROM USER_APPOINTMENTS
     	WHERE appointment = (?)''', (appt_id['id'],))

     count_appt = cur.fetchone()

     cur.execute('''
     	SELECT user
     	FROM USER_APPOINTMENTS
     	WHERE user = (?)''', (user_id['id'],))

     check_user = cur.fetchone()

     if ((check_user is None) and (count_appt['count_appt']) < 25):
          cur.execute("INSERT INTO USER_APPOINTMENTS (user, appointment) VALUES (?,?)", (user_id['id'], appt_id['id']))
          conn.commit()
     else:
          # TODO populate the error message to frontend
          cur.close()
          raise ValueError('Action not allowed. User already claimed a slot or slot is full.')

     cur.close()

     return {}


@app.route('/cancel', methods=['POST'])
def cancel_appointment():

     # TODO: here need to get the current user name;
     # TODO: hard code jane smith single user
     person = "Jane Smith"

     conn = get_db()
     cur = conn.cursor()

     cur.execute("SELECT * FROM USER_APPOINTMENTS")
     results = cur.fetchall()
     for row in results:
          print(row['user'], row['appointment'])

     # # get the current user id
     # cur.execute("SELECT id FROM USERS WHERE fname = (?)", (person.split(' ')[0],))
     # # TODO error handling what if that user doesn't exist
     # user_id = cur.fetchone()
     #
     # # get the appointment id;
     # cur.execute("SELECT appointment FROM USER_APPOINTMENTS WHERE user = (?)", (user_id['id'],))
     # appt_id_claimed = cur.fetchone()
     #
     # # delete that record in the database
     # # cur.execute("DELETE FROM USER_APPOINTMENTS WHERE user = (?)", (user_id['id'],))
     # # conn.commit()
     #
     # # show unclaimed appt in the appointments table
     # cur.execute("SELECT * FROM APPOINTMENTS WHERE id = (?)", (appt_id_claimed['id'],))
     # results = cur.fetchall()
     #
     # unclaimed_slot = {
     #      "id": results[0]['id'],
     #      "date": results[0]['date'],
     #      "time": results[0]['time'],
     #      "location": results[0]['location']}
     #
     # return {"unclaimed_slot": unclaimed_slot}

# TODO: this could be admin feature; see the current registered user and their timeslots
# #5. SHOW USERS_APPOINTMENTS TABLE DATA
# 
# cur.execute('''SELECT u.fname ||' '|| u.lname as Name, u.phone, l.name as Location, a.date, a.time
# FROM USERS u
# INNER JOIN USER_APPOINTMENTS ua ON u.id=ua.user
# INNER JOIN APPOINTMENTS a ON ua.appointment = a.id
# INNER JOIN LOCATIONS l ON a.location = l.id ''')
#
# results = cur.fetchall()
#
# claimed = [(row['Name'], row['phone'], row['Location'], row['date'], row['time']) for row in results]
#
# with open('scheduled_appts.csv', 'w', newline='') as f:
#      writer = csv.writer(f, delimiter=',')
#      writer.writerow(['name', 'phone', 'location', 'date', 'time'])
#      writer.writerows(claimed)
# 
#
