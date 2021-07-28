from dbhelper import DbHelper
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
import shutil


class Hi:
    function = 1

    def __init__(self):
        # connect with the database
        self.db = DbHelper()
        self.user_data = None
        # load the login form gui
        self.load_gui_window(self.load_login_gui)

    def load_gui_window(self, gui_type, data=None):

        self.root = Tk()

        self.root.title("Hi")

        self.root.configure(background="#FF5357")

        self.root.minsize(500, 600)
        self.root.maxsize(500, 600)
        if data is None:
            gui_type()
        else:
            gui_type(data)
        self.root.mainloop()

    def load_new_gui(self, new_gui, data=None):
        self.root.destroy()
        if data is None:
            self.load_gui_window(new_gui)
        else:
            self.load_gui_window(new_gui, data)

    def header_menu(self):
        menu = Menu(self.root)
        self.root.configure(menu=menu)
        file_menu = Menu(menu)
        menu.add_cascade(label="Home", menu=file_menu)
        file_menu.add_command(label="My Profile", command=lambda: self.load_new_gui(self.load_user_profile_gui))
        file_menu.add_command(label="View Other Profiles", command=lambda: self.count_relation_users('other_profile'))
        file_menu.add_command(label="Logout", command=lambda: self.logout())

        help_menu = Menu(menu)
        menu.add_cascade(label="Proposal", menu=help_menu)
        help_menu.add_command(label="Unseen Proposals", command=lambda: self.count_relation_users('proposal'))
        help_menu.add_command(label="Unseen Request", command=lambda: self.count_relation_users('request'))
        help_menu.add_command(label="My Matches", command=lambda: self.count_relation_users('match'))

    def header_menu2(self):
        menu = Menu(self.root)
        self.root.configure(menu=menu)
        menu.add_command(label="Back to My Profile", command=lambda: self.load_new_gui(self.load_user_profile_gui))

    def load_register_gui(self):
        # Dropdown menu options
        options = ["What is your nic name?", "What is your pet name?", "What is your favourite colour?", "What is your favourite fruit?", "What is your favourite flower?", "What is your favourite animal?", "What is your favourite place?", "What is your favourite number?"]
        self.question = StringVar()
        self.question.set("Select The Special Question")

        self.label0 = Label(self.root, text="Register to proceed", bg="#FF5357", fg="#fff", font=("Times", 20, "italic")).pack(pady=(5, 10))

        self.frame1 = Frame(self.root, bg="#FF5357")
        self.frame1.pack(pady=(10, 10), anchor=W)
        self.label1 = Label(self.frame1, text="  Enter Your Name  ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)
        self.name_input = Entry(self.frame1)
        self.name_input.pack(side=LEFT, ipady=7, ipadx=92)

        self.frame2 = Frame(self.root, bg="#FF5357")
        self.frame2.pack(pady=(10, 10), anchor=W)
        self.label2 = Label(self.frame2, text="  Enter Your Email  ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)
        self.email_input = Entry(self.frame2)
        self.email_input.pack(side=LEFT, ipady=7, ipadx=92)

        self.frame3 = Frame(self.root, bg="#FF5357")
        self.frame3.pack(pady=(10, 10), anchor=W)
        self.label3 = Label(self.frame3, text="  Create Password (8-30) ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)
        self.password_input = Entry(self.frame3)
        self.password_input.pack(side=LEFT, ipady=7, ipadx=70)

        self.frame4 = Frame(self.root, bg="#FF5357")
        self.frame4.pack(pady=(10, 10), anchor=W)
        self.label4 = Label(self.frame4, text="  Re-enter Password ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)
        self.re_password_input = Entry(self.frame4)
        self.re_password_input.pack(side=LEFT, ipady=7, ipadx=70)

        self.frame5 = Frame(self.root, bg="#FF5357")
        self.frame5.pack(pady=(15, 5))
        # Create Dropdown menu
        drop = OptionMenu(self.frame5, self.question, *options)
        drop.configure(font=("Times", 15, "italic"))
        drop.pack()

        self.frame6 = Frame(self.root, bg="#FF5357")
        self.frame6.pack(pady=(0, 10))
        self.label5 = Label(self.frame6, text="Answer  ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)
        self.answer_input = Entry(self.frame6)
        self.answer_input.pack(side=LEFT, ipady=7, ipadx=80)

        self.registration = Button(self.root, text="Register", bg="#fff", width=40, height=2, command=lambda: self.reg_validation()).pack(pady=(20, 10))

        self.label6 = Label(self.root, text="Already a member?", bg="#FF5357", fg="#fff", font=("Times", 12)).pack(pady=(20, 5))

        self.login_btn = Button(self.root, text="Login", bg="#fff", width=20, command=lambda: self.load_new_gui(self.load_login_gui)).pack(pady=(10, 10))

    def logout(self):
        # Close session data
        self.user_data = None
        self.root.destroy()
        self.load_gui_window(self.load_login_gui)

    def reg_validation(self):

        # fetch name,email,password,question and answer provided by the user
        password = self.password_input.get()
        if len(password) < 8 or len(password) > 30:
            messagebox.showerror("Error", "Your password should be (8-30)")
        else:
            re_password = self.re_password_input.get()
            name = self.name_input.get()
            email = self.email_input.get()
            question = self.question.get()
            answer = self.answer_input.get()
            if re_password != password:
                messagebox.showerror("Error", "Your two input password and not same")
            elif len(name) < 1 or len(email) < 1 or len(answer) < 1 or len(question) == "Select The Special Question":
                messagebox.showerror("Error", "You have to input all information")
            else:
                response = self.db.register(name, email, re_password, question, answer)

                if response == 1:
                    self.name_input.delete(0, 'end')
                    self.email_input.delete(0, 'end')
                    self.password_input.delete(0, 'end')
                    self.re_password_input.delete(0, 'end')
                    self.answer_input.delete(0, 'end')
                    messagebox.showinfo("Register Massage", "Registration Successful")
                else:
                    messagebox.showerror("Register Massage", "Registration Failed")

    def login_validation(self):
        email = self.email_input.get()
        password = self.password_input.get()

        self.email_input.delete(0, 'end')
        self.password_input.delete(0, 'end')

        data = self.db.search(email, password)

        if len(data) == 1:
            messagebox.showinfo("Login Message", "You have logged in successfully")
            # set session data
            self.user_data = data[0]
            # load user profile gui
            self.root.destroy()
            self.load_gui_window(self.load_user_profile_gui)
        else:
            messagebox.showerror("Login Message", "Incorrect email/password")

    def load_login_gui(self):
        self.label1 = Label(self.root, text="Hi", bg="#FF5357", fg="#fff", font=("Times", 32, "bold")).pack(pady=(25, 15))

        self.label2 = Label(self.root, text="Login to proceed", bg="#FF5357", fg="#fff", font=("Times", 20, "italic")).pack(pady=(5, 10))

        self.label3 = Label(self.root, text="Enter Email", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(pady=(10, 5))

        self.email_input = Entry(self.root)
        self.email_input.pack(pady=(0, 10), ipady=7, ipadx=80)

        self.label4 = Label(self.root, text="Enter Password", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(pady=(10, 5))

        self.password_input = Entry(self.root, show="*")
        self.password_input.pack(pady=(0, 20), ipady=7, ipadx=80)

        self.login = Button(self.root, text="Login", bg="#fff", width=40, height=2, command=lambda: self.login_validation()).pack(pady=(20, 10))

        self.label5 = Label(self.root, text="Not a member?", bg="#FF5357", fg="#fff", font=("Times", 12)).pack(pady=(20, 5))

        self.reg = Button(self.root, text="Register", bg="#fff", width=20, command=lambda: self.load_new_gui(self.load_register_gui)).pack(pady=(10, 10))

    def change_dp(self):
        pathname = filedialog.askopenfilename(initialdir="/images", title="something")
        # extract filename from path
        filename = pathname.split("/")[-1]
        destination = "C:\\Users\\Abhrojyoti\\PycharmProjects\\Hi\\img\\" + str(filename)
        if filename.split(".")[-1] == 'jpg' or filename.split(".")[-1] == 'jpeg' or filename.split(".")[-1] == 'png':
            shutil.copyfile(pathname, destination)
            # update the dp inn the database
            response = self.db.update_dp(self.user_data[0], filename)
            if response == -1:
                messagebox.showerror("Error", "Some error occurred")
            else:
                messagebox.showinfo("Massage", "DP Updated")
                self.user_data = response[0]
                self.load_new_gui(self.load_user_profile_gui)
        else:
            messagebox.showerror("Error", "Incorrect file format")

    def load_user_profile_gui(self):
        self.header_menu()

        # load dp
        if self.user_data[7] == "":
            imageUrl = "img/avatar.jpg"
        else:
            imageUrl = "img/{}".format(self.user_data[7])

        load = Image.open(imageUrl)
        load = load.resize((200, 200), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        img = Label(image=render)
        img.image = render
        img.pack()

        self.bp = Button(self.root, text="Change DP", bg="#fff", width=20, command=lambda: self.change_dp()).pack(pady=(5, 5))

        self.label5 = Label(self.root, text="Hi " + self.user_data[1], bg="#FF5357", fg="#fff", font=("Times", 12)).pack(pady=(10, 5))

        self.frame1 = Frame(self.root, bg="#FF5357")
        self.frame1.pack(pady=(10, 10))
        # age
        if self.user_data[4] == 0:
            self.label6 = Label(self.frame1, text="Age: " + "Not specified", bg="#FF5357", fg="#fff").pack(side=LEFT)
        else:
            self.label6 = Label(self.frame1, text="Age: " + str(self.user_data[4]), bg="#FF5357", fg="#fff", font=("Times", 12)).pack(side=LEFT)

        # gender
        if self.user_data[5] == "":
            self.label7 = Label(self.frame1, text=" Gender: " + "Not specified", bg="#FF5357", fg="#fff").pack(side=LEFT)
        else:
            self.label7 = Label(self.frame1, text=" Gender: " + str(self.user_data[5]), bg="#FF5357", fg="#fff", font=("Times", 12)).pack(side=LEFT)

        # city
        if self.user_data[6] == "":
            self.label8 = Label(self.frame1, text=" City: " + "Not specified", bg="#FF5357", fg="#fff").pack(side=LEFT)
        else:
            self.label8 = Label(self.frame1, text=" City: " + str(self.user_data[6]), bg="#FF5357", fg="#fff", font=("Times", 12)).pack(side=LEFT)

        # bio
        if self.user_data[8] == "":
            self.label9 = Label(self.root, text="About Me: " + "Not specified", bg="#FF5357", fg="#fff").pack(pady=(5, 10))
        else:
            self.label9 = Label(self.root, text="About Me: " + str(self.user_data[8]), bg="#FF5357", fg="#fff", font=("Times", 12)).pack(pady=(5, 10))
        self.frame2 = Frame(self.root, bg="#FF5357")
        self.frame2.pack(pady=(10, 10))
        self.password_change_btn = Button(self.frame2, text="Update Profile", font=("Times", 11), width=20, command=lambda: self.load_new_gui(self.load_edit_profile_gui)).pack(side=LEFT)
        self.password_change_btn = Button(self.frame2, text="Change Password", font=("Times", 11), width=20, command=lambda: self.load_new_gui(self.load_edit_password_gui)).pack(side=LEFT)

    def load_edit_profile_gui(self):
        self.header_menu2()
        # Dropdown menu options
        options = ["Male", "Female", "Other"]
        self.gender = StringVar()
        if self.user_data[5] == "":
            self.gender.set("Select The  Gender")
        else:
            self.gender.set(str(self.user_data[5]))
        self.label0 = Label(self.root, text="Edit Profile", bg="#FF5357", fg="#fff", font=("Times", 32, "bold")).pack(pady=(20, 20))

        self.frame1 = Frame(self.root, bg="#FF5357")
        self.frame1.pack(pady=(10, 10))
        self.label2 = Label(self.frame1, text="Gender ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)

        # Create Dropdown menu
        drop = OptionMenu(self.frame1, self.gender, *options)
        drop.configure(font=("Times", 15, "italic"))
        drop.pack()

        self.frame2 = Frame(self.root, bg="#FF5357")
        self.frame2.pack(pady=(10, 10))
        self.label1 = Label(self.frame2, text="Age ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)

        v = StringVar(self.frame2, value=self.user_data[4])
        self.edit_age_input = Entry(self.frame2, textvariable=v)
        self.edit_age_input.pack(side=LEFT, ipady=7, ipadx=80)

        self.frame3 = Frame(self.root, bg="#FF5357")
        self.frame3.pack(pady=(10, 10))
        self.label3 = Label(self.frame3, text="City ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)

        v = StringVar(self.frame3, value=self.user_data[6])
        self.edit_city_input = Entry(self.frame3, textvariable=v)
        self.edit_city_input.pack(side=LEFT, ipady=7, ipadx=80)

        self.frame4 = Frame(self.root, bg="#FF5357")
        self.frame4.pack(pady=(10, 10))
        self.label4 = Label(self.frame4, text="About Me ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)

        v = StringVar(self.frame4, value=self.user_data[8])
        self.edit_about_input = Entry(self.frame4, textvariable=v)
        self.edit_about_input.pack(side=LEFT, ipady=7, ipadx=80)

        self.frame5 = Frame(self.root, bg="#FF5357")
        self.frame5.pack(pady=(10, 10), side=BOTTOM)
        self.edit_btn = Button(self.frame5, text="Update Profile", width=40, height=2, command=lambda: self.edit_profile(2)).pack()

    def edit_profile(self, function):
        if function == 1:
            response = self.db.edit_user_profile(user_id=self.user_data[0], password=self.edit)

        else:
            age = self.edit_age_input.get()
            gender = self.gender.get()
            city = self.edit_city_input.get()
            about = self.edit_about_input.get()
            response = self.db.edit_user_profile(user_id=self.user_data[0], age=age, gender=gender, city=city, about=about)

        if response == -1:
            messagebox.showerror("Error", "Some error occurred")
        else:
            messagebox.showinfo("Massage", "Profile Updated")
            self.user_data = response[0]
            self.load_new_gui(self.load_user_profile_gui)

    def load_edit_password_gui(self):
        self.header_menu2()

        self.label1 = Label(self.root, text="Change Password", bg="#FF5357", fg="#fff", font=("Times", 32, "bold")).pack(pady=(20, 20))

        if self.function == 1:
            self.frame1 = Frame(self.root, bg="#FF5357")
            self.frame1.pack(pady=(15, 10), anchor=W)
            self.label2 = Label(self.frame1, text=" Enter Current Password ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)
            self.current_password_input = Entry(self.frame1)
            self.current_password_input.pack(side=LEFT, ipady=7, ipadx=70)

        self.frame2 = Frame(self.root, bg="#FF5357")
        self.frame2.pack(pady=(15, 10), anchor=W)
        self.label3 = Label(self.frame2, text=" Enter New Password ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)
        self.new_password_input = Entry(self.frame2)
        self.new_password_input.pack(side=LEFT, ipady=7, ipadx=80)

        self.frame3 = Frame(self.root, bg="#FF5357")
        self.frame3.pack(pady=(15, 10), anchor=W)
        self.label4 = Label(self.frame3, text=" Re-enter New Password ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(side=LEFT)
        self.edit_password_input = Entry(self.frame3)
        self.edit_password_input.pack(side=LEFT, ipady=7, ipadx=70)
        self.password_change_btn = Button(self.root, text="Change Password", font=("Times", 14), command=lambda: self.update_password()).pack(pady=(30, 30))

        if self.function == 1:
            self.label5 = Label(self.root, text=" Forget Password?  ", bg="#FF5357", fg="#fff", font=("Times", 14)).pack(pady=(15, 5))
            self.forget_password_btn = Button(self.root, text="Press Here", width=20, command=lambda: self.load_new_gui(self.load_forget_password_gui)).pack(pady=(10, 10))

    def update_password(self):
        new = self.new_password_input.get()
        self.new_password_input.delete(0, 'end')
        self.edit = self.edit_password_input.get()
        self.edit_password_input.delete(0, 'end')

        if self.function == 1:
            current = self.current_password_input.get()
            self.current_password_input.delete(0, 'end')
            if current == self.user_data[3]:
                if new == self.edit:
                    self.edit_profile(1)
                else:
                    messagebox.showerror("Error", "Your two new input password and not same")
            else:
                messagebox.showerror("Error", "Incorrect current password")
        else:
            if new == self.edit:
                self.edit_profile(1)
            else:
                messagebox.showerror("Error", "Your two new input password and not same")

    def load_forget_password_gui(self):
        self.header_menu2()

        self.label1 = Label(self.root, text="Forget  Password", bg="#FF5357", fg="#fff", font=("Times", 32, "bold")).pack(pady=(20, 20))

        self.label2 = Label(self.root, text=str(self.user_data[9]), bg="#FF5357", fg="#fff", font=("Times", 14)).pack(pady=(10, 5))
        self.forget_password_input = Entry(self.root)
        self.forget_password_input.pack(pady=(2, 15), ipady=7, ipadx=70)

        self.forget_password_btn = Button(self.root, text="Next", width=20, command=lambda: self.forget_password_validation()).pack(pady=(10, 10))

    def forget_password_validation(self):
        answer = self.forget_password_input.get()
        self.forget_password_input.delete(0, 'end')
        if answer == self.user_data[10]:
            self.fanction = 2
            self.load_new_gui(self.load_edit_password_gui)
        else:
            messagebox.showerror("Error", "Incorrect answer")

    def count_relation_users(self, btn):
        self.data_type = btn
        self.row_no = 0
        self.total_row_no = len(self.db.count_users(btn, self.user_data[0])) - 1
        if self.total_row_no < 0:
            self.load_new_gui(self.empty_gui)
        else:
            if btn == 'other_profile':
                self.view_profile()
            else:
                self.fetch_data()

    def empty_gui(self):
        self.header_menu2()

        self.label1 = Label(self.root, text="Empty", bg="#FF5357", fg="#fff", font=("Times", 50, "bold")).pack(pady=(55, 15))

    def fetch_data(self, btn=None):
        if btn == 'Prev':
            self.row_no = self.row_no - 1
        elif btn == 'Next':
            self.row_no = self.row_no + 1
        if self.row_no > self.total_row_no:
            messagebox.showerror("Error", "This is the last user")
            self.row_no = self.row_no - 1
        elif self.row_no < 0:
            messagebox.showerror("Error", "This is the first user")
            self.row_no = self.row_no + 1
        else:
            counter = self.total_row_no - self.row_no
            data = self.db.fetch_one_data(self.data_type, self.user_data[0], self.row_no, counter)
            self.load_new_gui(self.load_relationship_gui, data[0])

    def load_relationship_gui(self, data):
        self.header_menu2()

        # Dropdown menu options
        options = ["Accept", "Refuse", "Postpone"]
        approval = StringVar()
        approval.set("Approval")

        # Command of dropdown menu
        def callback(*args):
            text = approval.get()
            if text != "Approval":
                if messagebox.askyesno("Massage", "Are you want to " + str(text) + " this proposal?") is True:
                    self.approvals(data[0], text)

        # load dp
        if data[11] == "":
            imageUrl = "img/avatar.jpg"
        else:
            imageUrl = "img/{}".format(data[11])

        load = Image.open(imageUrl)
        load = load.resize((200, 200), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        img = Label(image=render)
        img.image = render
        img.pack()

        self.label5 = Label(self.root, text=data[5], bg="#FF5357", fg="#fff", font=("Times", 12)).pack(pady=(10, 5))

        # age
        if data[8] == 0:
            self.label6 = Label(self.root, text="Age: " + "Not specified", bg="#FF5357", fg="#fff", font=("Times", 12))
        else:
            self.label6 = Label(self.root, text="Age: " + str(data[8]), bg="#FF5357", fg="#fff", font=("Times", 12))
        self.label6.pack(pady=(10, 5))

        # gender
        if data[9] == "":
            self.label7 = Label(self.root, text="Gender: " + "Not specified", bg="#FF5357", fg="#fff", font=("Times", 12))
        else:
            self.label7 = Label(self.root, text="Gender: " + str(data[9]), bg="#FF5357", fg="#fff", font=("Times", 12))
        self.label7.pack(pady=(10, 5))

        # city
        if data[10] == "":
            self.label8 = Label(self.root, text="City: " + "Not specified", bg="#FF5357", fg="#fff", font=("Times", 12))
        else:
            self.label8 = Label(self.root, text="City: " + str(data[10]), bg="#FF5357", fg="#fff", font=("Times", 12))
        self.label8.pack(pady=(10, 5))

        # bio
        if data[12] == "":
            self.label9 = Label(self.root, text="About " + str(data[5]) + " : " + "Not specified", bg="#FF5357", fg="#fff", font=("Times", 12))
        else:
            self.label9 = Label(self.root, text="About " + str(data[5]) + " : " + str(data[12]), bg="#FF5357", fg="#fff", font=("Times", 12))
        self.label9.pack(pady=(10, 25))

        self.frame1 = Frame(self.root)
        self.frame1.pack(pady=(10, 25), side=BOTTOM)

        self.prev = Button(self.frame1, text="Previous", bg="#fff", height=1, width=10, font=("Times", 15), command=lambda: self.fetch_data("Prev"))
        self.prev.pack(side=LEFT)

        if self.data_type == 'request':
            # Create Dropdown menu
            drop = OptionMenu(self.frame1, approval, *options)
            drop.configure(font=("Times", 15, "italic"))
            drop.pack(side=LEFT)
            approval.trace("w", callback)

        self.next = Button(self.frame1, text="Next", bg="#fff", height=1, width=10, font=("Times", 15), command=lambda: self.fetch_data("Next"))
        self.next.pack(side=LEFT)

    def approvals(self, id, btn):
        response = self.db.approvals(id, btn)
        if response == 2:
            messagebox.showinfo("Massage", "Proposal accepted")
        elif response == 1:
            messagebox.showinfo("Massage", "Proposal Postponed")
        elif response == 0:
            messagebox.showinfo("Massage", "Proposal Refused")
        else:
            messagebox.showerror("Error", "Some error occurred")
        self.load_new_gui(self.load_user_profile_gui)

    def view_profile(self, btn=None):
        if btn == 'Prev':
            self.row_no = self.row_no - 1
        elif btn == 'Next':
            self.row_no = self.row_no + 1
        if self.total_row_no < self.row_no:
            messagebox.showerror("Error", "This is the last user")
            self.row_no = self.row_no - 1
        elif self.row_no < 0:
            messagebox.showerror("Error", "This is the first user")
            self.row_no = self.row_no + 1
        else:
            data = self.db.fetch_user(self.row_no)
            if data[0][0] == self.user_data[0]:
                self.row_no = self.row_no + 1
                if btn == "Prev":
                    messagebox.showerror("Error", "This is the first user")
                else:
                    self.view_profile()
            else:
                self.load_new_gui(self.load_other_user_profile_gui, data[0])

    def load_other_user_profile_gui(self, data):
        self.header_menu()

        # load dp
        if data[7] == "":
            imageUrl = "img/avatar.jpg"
        else:
            imageUrl = "img/{}".format(data[7])

        load = Image.open(imageUrl)
        load = load.resize((200, 200), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        img = Label(image=render)
        img.image = render
        img.pack()

        self.label5 = Label(self.root, text=data[1], bg="#FF5357", fg="#fff", font=("Times", 12))
        self.label5.pack(pady=(10, 5))

        # age
        if data[4] == 0:
            self.label6 = Label(self.root, text="Age: " + "Not specified", bg="#FF5357", fg="#fff", font=("Times", 12))
        else:
            self.label6 = Label(self.root, text="Age: " + str(data[4]), bg="#FF5357", fg="#fff", font=("Times", 12))
        self.label6.pack(pady=(10, 5))

        # gender
        if data[5] == "":
            self.label7 = Label(self.root, text="Gender: " + "Not specified", bg="#FF5357", fg="#fff", font=("Times", 12))
        else:
            self.label7 = Label(self.root, text="Gender: " + str(data[5]), bg="#FF5357", fg="#fff", font=("Times", 12))
        self.label7.pack(pady=(10, 5))

        # city
        if data[6] == "":
            self.label8 = Label(self.root, text="City: " + "Not specified", bg="#FF5357", fg="#fff", font=("Times", 12))
        else:
            self.label8 = Label(self.root, text="City: " + str(data[6]), bg="#FF5357", fg="#fff")
        self.label8.pack(pady=(10, 5))

        # bio
        if data[8] == "":
            self.label9 = Label(self.root, text="About " + str(data[1]) + " : " + "Not specified", bg="#FF5357", fg="#fff", font=("Times", 12))
        else:
            self.label9 = Label(self.root, text="About " + str(data[1]) + " : " + str(data[8]), bg="#FF5357", fg="#fff", font=("Times", 12))
        self.label9.pack(pady=(10, 5))

        self.frame1 = Frame(self.root)
        self.frame1.pack()

        self.prev = Button(self.frame1, text="Previous", bg="#fff", width=18, command=lambda: self.view_profile("Prev"))
        self.prev.pack(side=LEFT)

        self.prop = Button(self.frame1, text="Propose", bg="#fff", width=20, command=lambda: self.propose(data[0]))
        self.prop.pack(side=LEFT)

        self.next = Button(self.frame1, text="Next", bg="#fff", width=18, command=lambda: self.view_profile("Next"))
        self.next.pack(side=LEFT)

    def propose(self, juliet_id):
        response = self.db.add_proposal(self.user_data[0], juliet_id)
        if response == 1:
            messagebox.showinfo("Congrats!", "Proposal sent successfully")
        elif response == 0:
            messagebox.showerror("Error", "How many times you propose?")
        else:
            messagebox.showerror("Error", "Some error occurred")


Hi()
