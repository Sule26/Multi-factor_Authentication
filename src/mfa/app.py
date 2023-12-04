from .modules import Authy, SMS, Email, generate_key
from PIL import ImageTk, Image
from typing import Tuple
from loguru import logger
from tkinter import *
from PIL import Image
import psycopg2
import qrcode
import os
import re


class App:
    WIDTH = 400
    HEIGHT = 300
    AUTHY = Authy()
    EMAIL = Email()
    SMS = SMS()
    AUTHENTICATOR_OPTION = ["Email", "SMS", "Google Authenticator/Authy"]

    def __init__(self) -> None:
        self.login_window()
        self.connect_database()

    def connect_database(self) -> Tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
        conn = psycopg2.connect(
            database="uerj",
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host="127.0.0.1",
            port="5432",
        )

        cursor = conn.cursor()
        return conn, cursor

    def login_window(self) -> None:
        self.root = Tk()
        self.root.title("Login")
        # self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.root.resizable(False, False)

        self.login_username_label = Label(master=self.root, text="Username: ")
        self.login_username_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.login_username = Entry(master=self.root, width=30)
        self.login_username.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        self.login_username_warning = Label(master=self.root, text="", font=("Arial", 7), fg="red")
        self.login_username_warning.grid(row=1, column=0, columnspan=2, stick=W)

        self.login_password_label = Label(master=self.root, text="Password: ")
        self.login_password_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.login_password = Entry(master=self.root, show="*", width=30)
        self.login_password.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        self.login_password_warning = Label(master=self.root, text="", font=("Arial", 7), fg="red")
        self.login_password_warning.grid(row=3, column=0, columnspan=2, sticky=W)

        self.login_warning = Label(master=self.root, text="", font=("Arial", 7), fg="red")
        self.login_warning.grid(row=4, column=0, columnspan=2, sticky=W)

        self.login_authenticator_option_label = Label(master=self.root, text="What method are you goint to use?")
        self.login_authenticator_option_label.grid(row=6, column=0, padx=10, pady=10, sticky=W)

        self.login_authentication_choosen = StringVar()
        self.login_authentication_choosen.set("Email")
        for index, option in enumerate(self.AUTHENTICATOR_OPTION):
            Radiobutton(master=self.root, text=option, variable=self.login_authentication_choosen, value=option).grid(
                row=index + 7, column=0, columnspan=2, padx=10, pady=10, sticky=W
            )

        self.login_login_button = Button(master=self.root, text="Login", width=30, command=self.login)
        self.login_login_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky=W + E)

        self.login_register_button = Button(master=self.root, text="Register", width=30, command=self.register_window)
        self.login_register_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky=W + E)

        self.root.mainloop()

    def register_window(self) -> None:
        self.register_frame = Tk()
        self.register_frame.title("Register")
        # self.register_frame.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.register_frame.resizable(False, False)

        self.register_username_label = Label(master=self.register_frame, text="Username: ")
        self.register_username_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.register_username = Entry(master=self.register_frame, width=30)
        self.register_username.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        self.register_username_warning = Label(master=self.register_frame, text="", font=("Arial", 7), fg="red")
        self.register_username_warning.grid(row=1, column=0, columnspan=2, sticky=W)

        self.register_password_label = Label(master=self.register_frame, text="Password: ")
        self.register_password_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.register_password = Entry(master=self.register_frame, show="*", width=30)
        self.register_password.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        self.register_password_warning = Label(master=self.register_frame, text="", font=("Arial", 7), fg="red")
        self.register_password_warning.grid(row=3, column=0, columnspan=2, sticky=W)

        self.register_email_label = Label(master=self.register_frame, text="Email: ")
        self.register_email_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)
        self.register_email = Entry(master=self.register_frame, width=30)
        self.register_email.grid(row=4, column=1, padx=10, pady=10, sticky=W)

        self.register_email_warning = Label(master=self.register_frame, text="", font=("Arial", 7), fg="red")
        self.register_email_warning.grid(row=5, column=0, columnspan=2, sticky=W)

        self.register_phone_label = Label(master=self.register_frame, text="Phone: ")
        self.register_phone_label.grid(row=6, column=0, padx=10, pady=10, sticky=W)
        self.register_phone = Entry(master=self.register_frame, width=30)
        self.register_phone.grid(row=6, column=1, padx=10, pady=10, sticky=W)

        self.register_phone_warning = Label(master=self.register_frame, text="", font=("Arial", 7), fg="red")
        self.register_phone_warning.grid(row=7, column=0, columnspan=2, sticky=W)

        self.register_register_button = Button(
            master=self.register_frame, text="Register", width=30, command=self.register_user
        )
        self.register_register_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=W + E)

        self.register_frame.mainloop()

    def qrcode_window(self) -> None:
        self.qrcode_frame = Toplevel()
        self.qrcode_frame.title("Qrcode")
        self.qrcode_frame.resizable(False, False)
        self.qrcode = ImageTk.PhotoImage(Image.open("./qrcode.png"))
        self.qrcode_label = Label(master=self.qrcode_frame, image=self.qrcode)
        self.qrcode_label.grid(row=0, column=0, padx=10, pady=10, sticky=W + E)
        self.register_frame.destroy()

        self.qrcode_frame.mainloop()

    def logged_window(self) -> None:
        self.logged_frame = Tk()
        self.logged_frame.title("Result")
        self.logged_frame.geometry("200x100")
        self.logged_frame.resizable(False, False)

        self.result_label = Label(master=self.logged_frame, text="Logged In!", font=("Arial", 15))
        self.result_label.place(x=55, y=40)

        self.logged_frame.mainloop()

    def authenticate_window(self, authentication_type: str) -> None:
        self.authenticate_frame = Tk()
        self.authenticate_frame.title("Authenticate")
        # self.register_frame.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.authenticate_frame.resizable(False, False)

        conn, cursor = self.connect_database()
        cursor.execute(
            f"""
                select username, email, phone, user_key from account where username='{self.login_username.get().lower()}' and password='{self.login_password.get()}'
            """
        )
        result = list(cursor.fetchone())

        account = {
            "username": result[0],
            "email": result[1],
            "phone": result[2],
            "user_key": result[3],
        }

        if authentication_type == self.AUTHENTICATOR_OPTION[0]:
            self.EMAIL.send_message(account["user_key"], account["email"])

        if authentication_type == self.AUTHENTICATOR_OPTION[1]:
            self.SMS.send_sms(account["user_key"], account["phone"])

        # if authentication_type == self.AUTHENTICATOR_OPTION[2]:
            # Don't need to generate code so it doesn't need to do anything
            # pass

        self.code_label = Label(master=self.authenticate_frame, text="Insert code: ")
        self.code_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.code = Entry(master=self.authenticate_frame, width=30)
        self.code.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        self.code_warning = Label(master=self.authenticate_frame, text="", font=("Arial", 7), fg="red")
        self.code_warning.grid(row=1, column=0, columnspan=2, sticky=W)

        self.authenticate_button = Button(
            master=self.authenticate_frame,
            text="Authenticate",
            width=30,
            command=lambda: [self.authenticate(account["user_key"], self.code.get())],
        )
        self.authenticate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=W + E)

        conn.close()
        self.authenticate_frame.mainloop()


    def authenticate(self, user_key: str, code: str) -> None:
        if self.AUTHY.verify_code(user_key, code) or self.EMAIL.verify_code(user_key, code) or self.SMS.verify_code(user_key, code):
            self.authenticate_frame.destroy()
            self.logged_window()
        else:
            self.code_warning.config(text="* The code is wrong!")


    def login(self) -> None:
        if self.check_login_entry():
            conn, cursor = self.connect_database()
            cursor.execute(
                f"""
                select exists(select username, password from account where username='{self.login_username.get().lower()}' and password='{self.login_password.get()}')
                """
            )
            connected = cursor.fetchone()[0]

            if connected:
                self.login_warning.grid_remove()
                self.authenticate_window(self.login_authentication_choosen.get())

            else:
                self.login_warning.config(text="* Username or password is wrong")

    def check_login_entry(self) -> bool:
        return all([self.check_login_username(), self.check_login_password()])

    def register_user(self) -> None:
        if self.check_register_entries():
            user_key = generate_key()
            # logger.debug(user_key)
            authy = self.AUTHY.generate_code(user_key, self.register_email.get())
            phone_with_ddi = "+55" + self.register_phone.get()
            conn, cursor = self.connect_database()
            cursor.execute(
                f"""
                insert into account (username, password, email, phone, user_key) values ('{self.register_username.get().lower()}', '{self.register_password.get()}', '{self.register_email.get().lower()}', '{phone_with_ddi}', '{user_key}');
                """
            )
            conn.commit()
            cursor.close()
            qrcode.make(authy).save("./qrcode.png")
            self.qrcode_window()

    def check_login_username(self) -> bool:
        if self.login_username.get().strip() == "" or " " in self.login_username.get():
            self.login_username_warning.config(text="* Username can't be blank or space or have spaces")
            return False

        if not self.check_if_username_in_use(self.login_username.get().lower()):
            self.login_username_warning.config(text="* Username not registred")
            return False

        self.login_username_warning.grid_remove()
        return True

    def check_login_password(self) -> bool:
        if self.login_password.get().strip() == "" or " " in self.login_password.get():
            self.login_password_warning.config(text="* Password can't be blank or space or have spaces")
            return False

        self.login_password_warning.grid_remove()
        return True

    def check_register_entries(self) -> bool:
        return all(
            [
                self.check_registry_username(),
                self.check_registry_password(),
                self.check_registry_email(),
                self.check_registry_phone(),
            ]
        )

    def check_registry_username(self) -> bool:
        if self.register_username.get().strip() == "" or " " in self.register_username.get():
            self.register_username_warning.config(text="* Username can't be blank or space or have spaces")
            return False

        if len(self.register_username.get()) < 6:
            self.register_username_warning.config(text="* Username must have at least 6 characteres")
            return False

        if self.check_if_username_in_use(self.register_username.get().lower()):
            self.register_username_warning.config(text="* Username already in use")
            return False

        self.register_username_warning.grid_remove()
        return True

    def check_registry_password(self) -> bool:
        if self.register_password.get().strip() == "" or " " in self.register_password.get():
            self.register_password_warning.config(text="* Password can't be blank or space or have spaces")
            return False

        if len(self.register_password.get()) < 8:
            self.register_password_warning.config(text="* Password must have at least 8 characters")
            return False

        self.register_password_warning.grid_remove()
        return True

    def check_registry_email(self) -> bool:
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@gmail.com$")

        if self.register_email.get().strip() == "" or " " in self.register_email.get():
            self.register_email_warning.config(text="* Email can't be blank or have spaces")
            return False

        if len(re.findall(pattern, self.register_email.get())) == 0:
            self.register_email_warning.config(text="* Not valid email (must be gmail)")
            return False

        if self.check_if_email_in_use(self.register_email.get().lower()):
            self.register_email_warning.config(text="* Email already in use")
            return False

        self.register_email_warning.grid_remove()
        return True

    def check_registry_phone(self) -> bool:
        pattern = re.compile(r"^\d+$")

        if self.register_phone.get().strip() == "" or " " in self.register_phone.get():
            self.register_phone_warning.config(text="* Phone can't be blank or have spaces")
            return False

        if len(re.findall(pattern, self.register_phone.get())) == 0:
            self.register_phone_warning.config(text="* Phone can't have letters")
            return False

        if len(self.register_phone.get()) != 11:
            self.register_phone_warning.config(text="* Phone must have 11 digits (ddd + phone number)")
            return False

        if self.check_if_phone_in_use(self.register_phone.get()):
            self.register_phone_warning.config(text="* Phone already in use")
            return False

        self.register_phone_warning.grid_remove()
        return True

    def check_if_username_in_use(self, username_to_check: str) -> bool:
        conn, cursor = self.connect_database()
        cursor.execute(f"""select exists(select username from account where username = '{username_to_check}')""")
        return cursor.fetchone()[0]

    def check_if_email_in_use(self, email_to_check: str) -> bool:
        conn, cursor = self.connect_database()
        cursor.execute(f"""select exists(select email from account where username = '{email_to_check}')""")
        return cursor.fetchone()[0]

    def check_if_phone_in_use(self, phone_to_check: str) -> bool:
        conn, cursor = self.connect_database()
        cursor.execute(f"""select exists(select phone from account where username = '{phone_to_check}')""")
        return cursor.fetchone()[0]
