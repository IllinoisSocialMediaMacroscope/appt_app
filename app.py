from flask import Flask
import sqlite3
import build
import pandas as pd
import csv

conn = sqlite3.connect('appt_tracker.db')  
conn.execute('''PRAGMA foreign_keys = 1''')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

app = Flask(__name__)

@app.route('/login')
def login():
     return

@app.route('/logout')
def logout():
     return

@app.route('/list', methods=['GET'])
def list_available_appointments():
     return ""

@app.route('/submit', methods=['POST'])
def submit_appointment():
     return

@app.route('/cancel', methods=['POST'])
def cancel_appointment():
     return

#1. RUN FIRST, THEN COMMENT OUT

#populate tables with toy data
# users_df = pd.read_csv (r'./users.csv')
# users_df.to_sql('USERS', conn, if_exists='append', index = False)
# 
# locations_df = pd.read_csv (r'./locations.csv')
# locations_df.to_sql('LOCATIONS', conn, if_exists='append', index = False)
# 
# appointments_df = pd.read_csv (r'./shifts.csv')
# appointments_df.to_sql('APPOINTMENTS', conn, if_exists='append', index = False)
# 
# conn.commit() 


#2. CONFIRM DATA HAVE BEEN INSERTED

# df = pd.read_sql_query("SELECT * FROM USERS", conn)
# print(df)
# df = pd.read_sql_query("SELECT * FROM LOCATIONS", conn)
# print(df)
# df = pd.read_sql_query("SELECT * FROM APPOINTMENTS", conn)
# print(df)


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
cur.execute('''SELECT u.fname ||' '|| u.lname as Name, u.phone, l.name as Location, a.date, a.time
FROM USERS u 
INNER JOIN USER_APPOINTMENTS ua ON u.id=ua.user 
INNER JOIN APPOINTMENTS a ON ua.appointment = a.id
INNER JOIN LOCATIONS l ON a.location = l.id ''')

results = cur.fetchall()

claimed = [(row['Name'], row['phone'], row['Location'], row['date'], row['time']) for row in results]

with open('scheduled_appts.csv', 'w', newline='') as f:
     writer = csv.writer(f, delimiter=',')
     writer.writerow(['name', 'phone', 'location', 'date', 'time'])
     writer.writerows(claimed)
# 
# 
# #6. SHOW ALL AVAILABLE APPTS; 9am at Carle is no longer available because it has already been claimed twice
# 
cur.execute('''
SELECT a.id, a.date, a.time, l.name AS location
FROM APPOINTMENTS a INNER JOIN LOCATIONS l
ON a.location = l.id
WHERE a.id NOT IN (
	SELECT appointment
	FROM USER_APPOINTMENTS
	GROUP BY
		appointment
	HAVING COUNT(appointment) >= 2)
''')
results = cur.fetchall()

available = [(row['id'], row['date'], row['time'], row['location']) for row in results]

with open('open_appts.csv', 'w', newline='') as f:
     writer = csv.writer(f, delimiter=',')
     writer.writerow(['id', 'date', 'time', 'location'])
     writer.writerows(available)

#7. GIVE UP CLAIMED APPTS

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


conn.close()


