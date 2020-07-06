# COVID19 test scheduling APP

## Database
### Database Structure
There are three tables in the database: 
1. USER table that holds user information. Once a user authenticate against shibboleth, if that user does not
 already exists in the USER table, it will be automatically created and synced
2. APPOINTMENT table that holds all the appointment time and location
3. LOCATION table that holds all the detail location and information of test sites.

### How to set up the SQL database
- RUN `scripts/build.py` to initiate the *schema* database
- RUN `scripts/toy_data.py` to generate availabe shifts, currently it is dated till the end of 2020
- RUN `scripts/input.py` to populate *shifts* and *locations* data into the database
- Move the generated `appt_tracker.db` to the *root* of `appt_app` folder

## FLASK App
### Configuration
- Make sure you do not share `config.py` since it has app specific setting credentials. 
- Run command to start flask app in your local machine: 
```
export FLASK_APP=app.py
export FLASK_ENV=development
python3 -m flask run --host=0.0.0.0
```
- You can access the app at `http://{your_local_IP}:5000`

### Shibboleth Client Registration
- You have to contact Shibboleth manager first to add your NetID to a whitelist that allows registration
- Find out your deployment machine's *public IP address*, record that and use it in the redirect URL
- Make sure you are on Campus network or VPN, and run below commands: 
```
curl --request POST -u username:password —url 'https://shibboleth.illinois.edu/idp/profile/oidc/register --header
 'content-type: application/json' --data '{"client_name”:”COVID19 test appointment scheduler dev”, ”redirect_uris": 
["http://{public_IP_address}:5000/callback”], "scope": "openid profile email phone offline_access"}'
```