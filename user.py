from bson.objectid import ObjectId
from flask_login import UserMixin

from db import get_db


class User(UserMixin):

    def __init__(self, id_, netid, fname, lname, email, uin, phone):
        self.id = id_
        self.netid = netid
        self.fname = fname
        self.lname = lname
        self.email = email
        self.uin = uin
        self.phone = phone

    @staticmethod
    def get(user_id):
        db = get_db()
        user_record = db.users.find_one({"_id": ObjectId(user_id)})
        if not user_record:
            return None

        user = User(id_=user_record['_id'], netid=user_record['netid'], fname=user_record['fname'],
                    lname=user_record['lname'], email=user_record['email'], uin=user_record['uin'],
                    phone=user_record['phone'])
        print(user_record)
        return user

    @staticmethod
    def search(netid):
        db = get_db()
        user_record = db.users.find_one({"netid": netid})
        if not user_record:
            return None

        user = User(id_=user_record['_id'], netid=user_record['netid'], fname=user_record['fname'],
                    lname=user_record['lname'], email=user_record['email'], uin=user_record['uin'],
                    phone=user_record['phone'])

        return user

    @staticmethod
    def create(netid, fname, lname, email, uin, phone):
        db = get_db()
        result = db.users.insert_one({
            "netid": netid,
            "fname": fname,
            "lname": lname,
            "email": email,
            "uin": uin,
            "phone": phone
        })

        user = User(id_=result.inserted_id, netid=netid, fname=fname, lname=lname, email=email, uin=uin, phone=phone)

        return user
