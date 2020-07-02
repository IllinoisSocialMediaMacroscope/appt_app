from flask_login import UserMixin

from db import get_db


class User(UserMixin):

    def __init__(self, id_, fname, lname, email, phone, date):
        self.id = id_
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone
        self.date = date

    @staticmethod
    def get(user_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM USERS WHERE id = ?", (user_id,))
        user_record = cur.fetchone()
        if not user_record:
            return None

        user = User(id_=user_record['id'], fname=user_record['fname'], lname=user_record['lname'],
                    email=user_record['email'], phone=user_record['phone'], date=user_record['date'])

        return user

    @staticmethod
    def search(fname, lname):
        conn = get_db()
        cur = conn.cursor()

        # get the current user id
        cur.execute("SELECT * FROM USERS WHERE fname = (?) AND lname = (?) ", (fname, lname))
        user_record = cur.fetchone()
        if not user_record:
            return None

        user = User(id_=user_record['id'], fname=user_record['fname'], lname=user_record['lname'],
                    email=user_record['email'], phone=user_record['phone'], date=user_record['date'])

        return user

    @staticmethod
    def create(fname, lname, email, phone, date):
        conn = get_db()
        cur = conn.cursor()

        cur.execute("INSERT INTO USERS (fname, lname, email, phone, date) VALUES (?,?,?,?,?)", (fname, lname, email,
                                                                                                phone, date), )
        conn.commit()
        user = User(id_=cur.lastrowid, fname=fname, lname=lname,
                    email=email, phone=phone, date=date)

        return user