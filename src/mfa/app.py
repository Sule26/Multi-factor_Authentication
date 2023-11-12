from .email import Email
from .sms import SMS
from .otp import OTP
from typing import Tuple
from loguru import logger
import tkinter as tk
import psycopg2
import qrcode
import os
import re


class App:
    WIDTH = 400
    HEIGHT = 300
    otp = OTP()

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
        self.root = tk.Tk()
        self.root.title("Login")
        # self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.root.resizable(False, False)

        self.username_label = tk.Label(self.root, text="Username: ")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.username = tk.Entry(self.root, width=30)
        self.username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.password_label = tk.Label(self.root, text="Password: ")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.password = tk.Entry(self.root, show="*", width=30)
        self.password.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.login_button = tk.Button(self.root, text="Login", width=30)
        self.login_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E)

        self.register_button = tk.Button(self.root, text="Register", width=30, command=self.register_window)
        self.register_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E)

        self.root.mainloop()

    def register_window(self) -> None:
        self.register_frame = tk.Tk()
        self.register_frame.title("Register")
        # self.register_frame.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.register_frame.resizable(False, False)

        self.username_label = tk.Label(self.register_frame, text="Username: ")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.username = tk.Entry(self.register_frame, width=30)
        self.username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.username_warning = tk.Label(self.register_frame, text="", font=("Arial", 7), fg="red")

        self.password_label = tk.Label(self.register_frame, text="Password: ")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.password = tk.Entry(self.register_frame, show="*", width=30)
        self.password.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.password_warning = tk.Label(self.register_frame, text="", font=("Arial", 7), fg="red")

        self.email_label = tk.Label(self.register_frame, text="Email: ")
        self.email_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.email = tk.Entry(self.register_frame, width=30)
        self.email.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

        self.email_warning = tk.Label(self.register_frame, text="", font=("Arial", 7), fg="red")

        self.phone_label = tk.Label(self.register_frame, text="Phone: ")
        self.phone_label.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
        self.phone = tk.Entry(self.register_frame, width=30)
        self.phone.grid(row=6, column=1, padx=10, pady=10, sticky=tk.W)

        self.phone_warning = tk.Label(self.register_frame, text="", font=("Arial", 7), fg="red")

        self.register_button = tk.Button(self.register_frame, text="Register", width=30, command=self.register_user)
        self.register_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E)

        self.register_frame.mainloop()

    def register_user(self) -> None:
        if self.check_registry_entrys():
            authy = self.otp.generate_authenticator(self.email.get())
            phone_with_ddi = "+55" + self.phone.get()
            conn, cursor = self.connect_database()
            cursor.execute(
                f"""
                insert into account (username, password, email, phone, authy) values ('{self.username.get().lower()}', '{self.password.get()}', '{self.email.get().lower()}', '{phone_with_ddi}', '{authy}');
                """
            )
            conn.commit()
            cursor.close()
            qrcode.make(authy)
            self.register_frame.destroy()

    def check_registry_entrys(self) -> bool:
        return all([self.check_username(), self.check_password(), self.check_email(), self.check_phone()])

    def check_username(self) -> bool:
        self.username_warning.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        if self.username.get().strip() == "" or " " in self.username.get():
            self.username_warning.config(text="* Username can't be blank or space or have spaces")
            return False

        if self.check_if_username_in_use(self.username.get().lower()):
            self.username_warning.config(text="* Username already in use")
            return False

        self.username_warning.grid_remove()
        return True

    def check_password(self) -> bool:
        self.password_warning.grid(row=3, column=0, columnspan=2, sticky=tk.W)

        if self.password.get().strip() == "" or " " in self.password.get():
            self.password_warning.config(text="* Password can't be blank or space or have spaces")
            return False

        self.password_warning.grid_remove()
        return True

    def check_email(self) -> bool:
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@gmail.com$")
        self.email_warning.grid(row=5, column=0, columnspan=2, sticky=tk.W)

        if self.email.get().strip() == "" or " " in self.email.get():
            self.email_warning.config(text="* Email can't be blank or have spaces")
            return False

        if len(re.findall(pattern, self.email.get())) == 0:
            self.email_warning.config(text="* Not valid email (must be gmail)")
            return False

        if self.check_if_email_in_use(self.email.get().lower()):
            self.email_warning.config(text="* Email already in use")
            return False

        self.email_warning.grid_remove()
        return True

    def check_phone(self) -> bool:
        pattern = re.compile(r"^\d+$")
        self.phone_warning.grid(row=7, column=0, columnspan=2, sticky=tk.W)

        if self.phone.get().strip() == "" or " " in self.phone.get():
            self.phone_warning.config(text="* Phone can't be blank or have spaces")
            return False

        if len(re.findall(pattern, self.phone.get())) == 0:
            self.phone_warning.config(text="* Phone can't have letters")
            return False

        if len(self.phone.get()) != 11:
            self.phone_warning.config(text="* Phone must have 11 digits (ddd + personal number)")
            return False

        if self.check_if_phone_in_use(self.phone.get()):
            self.phone_warning.config(text="* Phone already in use")
            return False

        self.phone_warning.grid_remove()
        return True

    def check_if_username_in_use(self, username_to_check) -> bool:
        conn, cursor = self.connect_database()
        cursor.execute(f"""select exists(select username from account where username = '{username_to_check}')""")
        return cursor.fetchone()[0]

    def check_if_email_in_use(self, email_to_check) -> bool:
        conn, cursor = self.connect_database()
        cursor.execute(f"""select exists(select email from account where username = '{email_to_check}')""")
        return cursor.fetchone()[0]

    def check_if_phone_in_use(self, phone_to_check) -> bool:
        conn, cursor = self.connect_database()
        cursor.execute(f"""select exists(select phone from account where username = '{phone_to_check}')""")
        return cursor.fetchone()[0]
