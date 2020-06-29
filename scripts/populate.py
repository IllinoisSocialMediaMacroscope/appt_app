import sqlite3
import pandas as pd

conn = sqlite3.connect('appt_tracker.db')
conn.execute('''PRAGMA foreign_keys = 1''')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# populate tables with toy data

users_df = pd.read_csv (r'./users.csv')
users_df.to_sql('USERS', conn, if_exists='append', index = False)

locations_df = pd.read_csv (r'./locations.csv')
locations_df.to_sql('LOCATIONS', conn, if_exists='append', index = False)

appointments_df = pd.read_csv (r'./shifts.csv')
appointments_df.to_sql('APPOINTMENTS', conn, if_exists='append', index = False)

user_appointments_df = pd.read_csv (r'./scheduled_appts.csv')
user_appointments_df.to_sql('USER_APPOINTMENTS', conn, if_exists='append', index = False)

conn.commit()

#2. CONFIRM DATA HAVE BEEN INSERTED

df = pd.read_sql_query("SELECT * FROM USERS", conn)
print(df)
df = pd.read_sql_query("SELECT * FROM LOCATIONS", conn)
print(df)
df = pd.read_sql_query("SELECT * FROM APPOINTMENTS", conn)
print(df)