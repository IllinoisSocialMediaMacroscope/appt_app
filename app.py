import os

from flask import Flask, render_template, request, g, abort, redirect, url_for
from flask_login import (
     LoginManager,
     login_user,
     login_required,
     logout_user,
     current_user
)
from oic import rndstr
from oic.oic import Client
from oic.oic.message import AuthorizationResponse, RegistrationResponse, ClaimsRequest, Claims
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.utils.http_util import Redirect

from db import get_db
from user import User

app = Flask(__name__)
app.secret_key = os.urandom(24)

# OIDC setting
app.config.from_pyfile('config.py', silent=True)

# create oidc client
client = Client(client_authn_method=CLIENT_AUTHN_METHOD)

# get authentication provider details by hitting the issuer URL
provider_info = client.provider_config(app.config["ISSUER_URL"])

# store registration details
info = {
     "client_id": app.config["CLIENT_ID"],
     "client_secret": app.config["CLIENT_SECRET"],
     "redirect_uris": app.config["REDIRECT_URIS"]
}
client_reg = RegistrationResponse(**info)
client.store_registration_info(client_reg)

session = dict()

# LOGIN management setting
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
     return User.get(user_id)


@app.teardown_appcontext
def close_connection(exception):
     conn = getattr(g, '_database', None)
     if conn is not None:
          conn.close()


@app.route('/login')
def login():
     session['state'] = rndstr()
     session['nonce'] = rndstr()

     # setup claim request
     claims_request = ClaimsRequest(
          userinfo = Claims(uiucedu_uin={"essential": True})
     )

     args = {
          "client_id": client.client_id,
          "response_type": "code",
          "scope": app.config["SCOPES"],
          "nonce": session["nonce"],
          "redirect_uri":client.registration_response["redirect_uris"][0],
          "state":session["state"],
          "claims":claims_request
     }

     auth_req = client.construct_AuthorizationRequest(request_args=args)
     login_url = auth_req.request(client.authorization_endpoint)

     return Redirect(login_url)


@app.route('/callback')
def callback():
     response = request.environ["QUERY_STRING"]

     authentication_response = client.parse_response(AuthorizationResponse, info=response, sformat="urlencoded")

     code = authentication_response["code"]
     assert authentication_response["state"] == session["state"]

     args = {
          "code": code
     }

     token_response = client.do_access_token_request(state=authentication_response["state"], request_args=args,
                                                     authn_method="client_secret_basic")

     user_info = client.do_user_info_request(state=authentication_response["state"])

     # see if that user is in local database or not
     user = User.search(user_info["given_name"], user_info["family_name"])

     # create that user in local db if that person is not there;
     if not user:
          user = User.create(fname=user_info["given_name"],
                             lname=user_info["family_name"],
                             email=user_info["email"],
                             phone=999, date="NA")

     # login that user
     login_user(user)

     return redirect(url_for("homepage"))


@app.route('/logout')
@login_required
def logout():
     logout_user()
     return redirect(url_for("homepage"))


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

     if current_user.is_authenticated:
          user = "Hello! " + current_user.fname + " " + current_user.lname
     else:
          user = None

     return render_template('appointments.html', locations=locations, times=times, user=user)


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


@app.route('/my-appointment', methods=['GET'])
def list_my_appointment():
     if current_user.is_authenticated:
          conn = get_db()
          cur = conn.cursor()

          # get the appointment id;
          cur.execute("SELECT appointment FROM USER_APPOINTMENTS WHERE user = (?)", (current_user.id,))
          appt_id_claimed = cur.fetchone()

          if appt_id_claimed:
               cur.execute(
                    "SELECT a.id, a.date, a.time, l.name as location FROM APPOINTMENTS a INNER JOIN LOCATIONS l ON "
                    "a.location = l.id WHERE a.id = (?)", (appt_id_claimed['appointment'],))
               results = cur.fetchall()
               cur.close()

               claimed_slot = {
                    "id": results[0]['id'],
                    "date": results[0]['date'],
                    "time": results[0]['time'],
                    "location": results[0]['location']}
          else:
               cur.close()
               claimed_slot = {}

          return {"claimed_slot": claimed_slot}

     else:
          abort(403, 'User not Authorized! Please login first.')


@app.route('/submit', methods=['POST'])
def submit_appointment():
     if current_user.is_authenticated:
          if request.get_json() and request.get_json()['appt_id']:
               appt = request.get_json()['appt_id']
          else:
               abort(400, 'Apppointment Id is a required field!')

          conn = get_db()
          cur = conn.cursor()

          # get the appt id
          cur.execute("SELECT id FROM APPOINTMENTS WHERE id = (?)", (appt,))
          appt_id = cur.fetchone()
          if not appt_id:
               abort(404, 'Cannot the selected appointment in the APPOINTMENTS database table.')

          # INSERT IF MAX 25 NOT REACHED PER APPOINTMENT ID
          cur.execute('''
             SELECT COUNT(appointment) as count_appt
             FROM USER_APPOINTMENTS
             WHERE appointment = (?)''', (appt_id['id'],))

          count_appt = cur.fetchone()

          cur.execute('''
             SELECT user
             FROM USER_APPOINTMENTS
             WHERE user = (?)''', (current_user.id,))

          check_user = cur.fetchone()

          if ((check_user is None) and (count_appt['count_appt']) < 25):
               cur.execute("INSERT INTO USER_APPOINTMENTS (user, appointment) VALUES (?,?)",
                           (current_user.id, appt_id['id']))
               conn.commit()

               cur.execute(
                    "SELECT a.id, a.date, a.time, l.name as location FROM APPOINTMENTS a INNER JOIN LOCATIONS l ON "
                    "a.location = l.id WHERE a.id = (?)", (appt_id['id'],))
               results = cur.fetchall()

               claimed_slot = {
                    "id": results[0]['id'],
                    "date": results[0]['date'],
                    "time": results[0]['time'],
                    "location": results[0]['location']}

               cur.close()

               return {"claimed_slot": claimed_slot}

          else:
               cur.close()
               abort(403, 'Action not allowed. User already claimed a slot or slot is full.')

     else:
          abort(403, 'User not Authorized! Please login first.')


@app.route('/cancel', methods=['DELETE'])
def cancel_appointment():
     if current_user.is_authenticated:

          conn = get_db()
          cur = conn.cursor()

          # get user's appointment id and delete
          cur.execute("SELECT appointment FROM USER_APPOINTMENTS WHERE user = (?)", (current_user.id,))
          appt_id_claimed = cur.fetchone()
          if appt_id_claimed:
               cur.execute("DELETE FROM USER_APPOINTMENTS WHERE user = (?)", (current_user.id,))
               conn.commit()

               cur.execute(
                    "SELECT a.id, a.date, a.time, l.name as location FROM APPOINTMENTS a INNER JOIN LOCATIONS l ON "
                    "a.location = l.id WHERE a.id = (?)", (appt_id_claimed['appointment'],))
               results = cur.fetchall()
               cur.close()

               unclaimed_slot = {
                    "id": results[0]['id'],
                    "date": results[0]['date'],
                    "time": results[0]['time'],
                    "location": results[0]['location']}

               return {"unclaimed_slot": unclaimed_slot}
          else:
               cur.close()
               abort(403, 'Action not allowed. This user currently has no appointment!')

     else:
          abort(403, 'User not Authorized! Please login first.')
