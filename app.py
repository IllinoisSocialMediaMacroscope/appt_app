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

     return render_template('appointments.html', available_slots=available_slots)

@app.route('/submit', methods=['POST'])
def submit_appointment():
     return

@app.route('/cancel', methods=['POST'])
def cancel_appointment():
     return


#3. RUN THESE INDIVIDUALLY, THEN COMMENT OUT

#claim appt; receive these values from session; here, hard-coded for demo
# id_person = "Jane Smith"
# id_appt = 2
# 
# id_person = "John Smith"
# id_appt = 2
# 
#FAILS BECAUSE APPT HAS BEEN CLAIMED TWICE
# id_person = "Jill Smith"
# id_appt = 2
# 
# id_person = "Jill Smith"
# id_appt = 3
# 
#FAILS BECAUSE JOHN SMITH IS ALREADY IN USER_APPOINTMENTS
# id_person = "John Smith"
# id_appt = 3
# 
# cur.execute("SELECT id FROM USERS WHERE fname = (?)", (id_person.split(' ')[0],) )
# user_id = cur.fetchone()
# 
# cur.execute("SELECT id FROM APPOINTMENTS WHERE id = (?)", (id_appt,) )
# appt_id = cur.fetchone()
# 
# # 
# # #4. INSERT IF MAX 2 NOT REACHED PER APPOINTMENT ID; expecting message because 3 is in there twice
# # 
# cur.execute('''
# 	SELECT COUNT(appointment) as count_appt
# 	FROM USER_APPOINTMENTS
# 	WHERE appointment = (?)''', (appt_id['id'],) )
# 	
# count_appt = cur.fetchone()
# 
# cur.execute('''
# 	SELECT user
# 	FROM USER_APPOINTMENTS
# 	WHERE user = (?)''', (user_id['id'],) )
# 
# check_user = cur.fetchone()
# 
# if( (check_user is None)  and  (count_appt['count_appt']) < 2 ):	
# 	cur.execute("INSERT INTO USER_APPOINTMENTS (user, appointment) VALUES (?,?)", (user_id['id'], appt_id['id']) )
# 	conn.commit() 
# else: 
# 	print('Action not allowed. User already claimed a slot or slot is full.')
# 
# 
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


# 7. GIVE UP CLAIMED APPTS

# id_person = 2
# id_claimed = 2
# 
# cur.execute("DELETE FROM USER_APPOINTMENTS WHERE user = (?)", (id_person,))
# 
# conn.commit() 
# 
# #show unclaimed appt in the appointments table
# cur.execute("SELECT * FROM APPOINTMENTS WHERE id = (?)", (id_claimed,))
# 
# results = cur.fetchall()
# 
# for row in results:
# 	print(row['id'], row['Date'], row['Time'], row['Location'])




