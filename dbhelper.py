import mysql.connector


class DbHelper:

    def __init__(self):
        try:
            self.conn = mysql.connector.Connect(host="localhost", user="root", password="", database="hi")
            self.mycursor = self.conn.cursor()
        except:
            print("Database error")
        else:
            print("Connected to Database")

    def search(self, email, password):
        self.mycursor.execute("SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}'".format(email, password))
        data = self.mycursor.fetchall()
        return data

    def register(self, name, email, password, question, answer):
        try:
            self.mycursor.execute("INSERT INTO users VALUES (NULL, '{}', '{}', '{}', '', '', '', '', '', '{}', '{}')".format(name, email, password, question, answer))
            self.conn.commit()
        except:
            return -1
        else:
            return 1

    def fetch_user(self, row_no):
        self.mycursor.execute("SELECT * FROM users WHERE id LIKE '{}'".format(row_no + 1))
        data = self.mycursor.fetchall()
        return data

    def update_dp(self, user_id, filename):
        try:
            self.mycursor.execute("UPDATE users SET dp = '{}' WHERE id = {}".format(filename, user_id))
            self.conn.commit()
            self.mycursor.execute("SELECT * FROM users WHERE id LIKE '{}'".format(user_id))
            data = self.mycursor.fetchall()
            return data
        except:
            return -1

    def count_users(self, call_function, user=None):
        if call_function == 'proposal':
            self.mycursor.execute("SELECT proposal_id FROM proposals WHERE romeo_id LIKE '{}' AND approval IS NULL".format(user))
        elif call_function == 'request':
            self.mycursor.execute("SELECT proposal_id FROM proposals WHERE juliet_id LIKE '{}' AND approval IS NULL".format(user))
        elif call_function == 'match':
            self.mycursor.execute("SELECT proposal_id FROM proposals WHERE (romeo_id LIKE '{}' OR juliet_id LIKE '{}') AND approval = 'yes'".format(user, user))
        else:
            self.mycursor.execute("SELECT id FROM users")
        data = self.mycursor.fetchall()
        return data

    def add_proposal(self, romeo_id, juliet_id):
        # check whether this romeo has already proposed this juliet
        self.mycursor.execute("SELECT * FROM proposals WHERE romeo_id = {} AND juliet_id = {}".format(romeo_id, juliet_id))
        data = self.mycursor.fetchall()
        if len(data) > 0:
            return 0
        else:
            try:
                self.mycursor.execute("INSERT INTO proposals VALUES (NULL,{},{},NULL)".format(romeo_id, juliet_id))
                self.conn.commit()
            except:
                return -1
            else:
                return 1

    def approvals(self, user_id, btn):
        if btn == 'Accept':
            self.mycursor.execute("UPDATE proposals SET approval = 'yes' WHERE proposal_id = {}".format(user_id))
            t = 2
        elif btn == 'Postpone':
            self.mycursor.execute("UPDATE proposals SET approval = 'not now' WHERE proposal_id = {}".format(user_id))
            t = 1
        else:
            self.mycursor.execute("DELETE FROM proposals WHERE proposal_id = {}".format(user_id))
            t = 0
        self.conn.commit()
        return t

    def fetch_one_data(self, data_type, user_id, row_no, counter=None):
        if data_type == 'proposal':
            self.mycursor.execute("SELECT * FROM proposals JOIN users ON proposals.juliet_id = id WHERE proposals.romeo_id = {} LIMIT {},1".format(user_id, row_no))
            data = self.mycursor.fetchall()
        elif data_type == 'request':
            self.mycursor.execute("SELECT * FROM proposals JOIN users ON proposals.romeo_id = id WHERE proposals.juliet_id = {} AND proposals.approval IS NULL LIMIT {},1".format(user_id, row_no))
            data = self.mycursor.fetchall()
        else:
            self.mycursor.execute("SELECT * FROM proposals JOIN users ON proposals.juliet_id = id WHERE proposals.romeo_id = {} AND approval = 'yes' LIMIT {},1".format(user_id, row_no))
            data = self.mycursor.fetchall()
            if len(data) == 0:
                self.mycursor.execute("SELECT * FROM proposals JOIN users ON proposals.romeo_id = id WHERE proposals.juliet_id = {} AND approval = 'yes' LIMIT {},1".format(user_id, counter))
                data = self.mycursor.fetchall()
        return data

    def edit_user_profile(self, user_id, age=None, gender=None, city=None, about=None, password=None):
        try:
            if password is None:
                self.mycursor.execute("UPDATE users SET age='{}',gender='{}', city='{}',bio='{}' WHERE id='{}'".format(age, gender, city, about, user_id))
            else:
                self.mycursor.execute("UPDATE users SET password='{}' WHERE id='{}'".format(password, user_id))
            self.conn.commit()
            self.mycursor.execute("SELECT * FROM users WHERE id LIKE '{}'".format(user_id))
            data = self.mycursor.fetchall()
        except:
            return -1
        else:
            return data
