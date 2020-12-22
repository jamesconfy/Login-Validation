import sqlite3
from flask_login import UserMixin

class DB(UserMixin):
    def __init__(self):
        self.conn = sqlite3.connect("./user_info.db")
        self.db = self.conn.cursor()
        self.db.execute("""CREATE TABLE IF NOT EXISTS new_personal_info(
            id INTEGER PRIMARY KEY NOT NULL,
            username text NOT NULL UNIQUE,
            password text NOT NULL,
            email text NOT NULL UNIQUE,
            first_name text NOT NULL,
            last_name text NOT NULL,
            dob text,
            address text,
            city text,
            state text,
            phone_number text
        )""")

    def CreateProfile(self, username, password, email, first_name, last_name, dob, address, city, state, phone_no):
        self.db.execute("INSERT INTO new_personal_info VALUES(:id, :username, :password, :email, :first_name, :last_name, :dob, :address, :city, :state, :phone_number)", {
            'id': None,
            'username': username,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'dob': dob,
            'address': address,
            'city': city,
            'state': state,
            'phone_number': phone_no
        })
        self.conn.commit()
        
    def GetByID(self, yid):
        self.db.execute("SELECT * FROM new_personal_info WHERE id = (?)", (yid,))
        return self.db.fetchone()

    def DeleteProfileByID(self, yid):
        self.db.execute("DELETE FROM new_personal_info WHERE id = (?)", (yid,))
        self.conn.commit()

    def Update(self, set_update, yid, set_value):
        self.db.execute("UPDATE new_personal_info SET " +set_update+" = (?) WHERE id = (?)", (set_value, yid))
        self.conn.commit()

    def UpdateAll(self, yid, username, email, first_name2, last_name2, dob2, address2, city2, state2, phone_no2):
        self.db.execute("UPDATE new_personal_info SET username = (?), email = (?), first_name = (?), last_name = (?), dob = (?), address = (?), city = (?), state = (?), phone_number = (?) WHERE id = (?)", (username, email, first_name2, last_name2, dob2, address2, city2, state2, phone_no2, yid))
        self.conn.commit()

    def DeleteProfileByName(self, first_name1, last_name1):
        self.db.execute("DELETE FROM new_personal_info WHERE first_name = (?) AND last_name = (?)", (first_name1, last_name1))
        self.conn.commit()

    def GetAll(self):
        self.db.execute("SELECT * FROM new_personal_info")
        return self.db.fetchall()

    def GetIDBy_Username_Password(self, username):
        self.db.execute("SELECT id FROM new_personal_info WHERE username = (?)", (username,))
        return self.db.fetchone()

    def GetPasswordByUsername(self, username):
        self.db.execute("SELECT password FROM new_personal_info WHERE username = (?)", (username,))
        return self.db.fetchone()

    def GetByUsername(self, username):
        self.db.execute("SELECT * FROM new_personal_info WHERE username = (?)", (username,))
        return self.db.fetchone()

    def GetByEmail(self, email):
        self.db.execute("SELECT * FROM new_personal_info WHERE email = (?)", (email,))
        return self.db.fetchone()

    def Close(self):
        self.conn.close()