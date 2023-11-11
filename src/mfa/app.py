# from mfa.email import Email
# from mfa.sms import Sms
from typing import Tuple
import tkinter as tk
import psycopg2
import qrcode
import pyotp
import os


class App:
    WIDTH = 350
    HEIGHT = 350

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
        self.password = tk.Entry(self.root, width=30)
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

        self.register_username_label = tk.Label(self.register_frame, text="Username: ")
        self.register_username_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.register_username = tk.Entry(self.register_frame, width=30)
        self.register_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.register_password_label = tk.Label(self.register_frame, text="Password: ")
        self.register_password_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.register_password = tk.Entry(self.register_frame, width=30)
        self.register_password.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.register_email_label = tk.Label(self.register_frame, text="Email: ")
        self.register_email_label.grid(row=2, column=0)
        self.register_email = tk.Entry(self.register_frame, width=30)
        self.register_email.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.register_phone_label = tk.Label(self.register_frame, text="Phone: ")
        self.register_phone_label.grid(row=3, column=0)
        self.register_phone = tk.Entry(self.register_frame, width=30)
        self.register_phone.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        self.register_register_button = tk.Button(
            self.register_frame, text="Register", width=30, command=self.register_user
        )
        self.register_register_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E)

        self.register_frame.mainloop()

    def register_user(self) -> None:
        
        conn, cursor = self.connect_database()
        cursor.execute(
            f"""
            insert into account (username, password, email, phone, authy) values ('{self.register_username.get()}', '{self.register_password.get()}', '{self.register_email.get()}', '{self.register_phone.get()}', '{authy}')
            """
        )
        conn.commit()
        cursor.close()
        self.register_frame.destroy()
