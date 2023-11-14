from .modules import OTP, SMS, Email
from PIL import ImageTk, Image
from typing import Tuple
from loguru import logger
import tkinter as tk
from PIL import Image
import psycopg2
import qrcode
import os
import re


class App:
    WIDTH = 400
    HEIGHT = 300
    OTP = OTP()
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
        self.root = tk.Tk()
        self.root.title("Login")
        # self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.root.resizable(False, False)

        self.username_label = tk.Label(self.root, text="Username: ")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.username = tk.Entry(self.root, width=30)
        self.username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.login_username_warning = tk.Label(self.root, text="", font=("Arial", 7), fg="red")

        self.password_label = tk.Label(self.root, text="Password: ")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.password = tk.Entry(self.root, show="*", width=30)
        self.password.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        self.login_password_warning = tk.Label(self.root, text="", font=("Arial", 7), fg="red")
        self.login_warning = tk.Label(self.root, text="", font=("Arial", 7), fg="red")

        self.authenticator_option_label = tk.Label(self.root, text="What method are you goint to use?")
        self.authenticator_option_label.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)

        self.authentication_choosen = tk.StringVar()
        self.authentication_choosen.set("Email")
        for index, option in enumerate(self.AUTHENTICATOR_OPTION):
            tk.Radiobutton(self.root, text=option, variable=self.authentication_choosen, value=option).grid(
                row=index + 7, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W
            )

        self.login_button = tk.Button(self.root, text="Login", width=30, command=self.login)
        self.login_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E)

        self.register_button = tk.Button(self.root, text="Register", width=30, command=self.register_window)
        self.register_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E)

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

        self.register_button = tk.Button(self.register_frame, text="Register", width=30, command=lambda: [self.register_user(), self.qrcode_window()])
        self.register_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E)

        self.register_frame.mainloop()

    def qrcode_window(self) -> None:
        self.qrcode_frame = tk.Tk()
        self.qrcode_frame.title("Qrcode")
        self.qrcode_frame.resizable(False, False)
        self.qrcode = ImageTk.PhotoImage(Image.open("./qrcode.png"))
        self.qrcode_label = tk.Label(image=self.qrcode)
        self.qrcode_label.pack()
        
        self.qrcode_frame.mainloop()

    def logged_window(self) -> None:
        self.logged_frame = tk.Tk()
        self.logged_frame.title("Result")
        self.logged_frame.geometry("200x100")
        self.logged_frame.resizable(False, False)

        self.result_label = tk.Label(self.logged_frame, text="Logged!", font=("Arial", 15))
        self.result_label.place(x=70, y=40)

        self.logged_frame.mainloop()

    def authenticate_window(self, authentication_type) -> None:
        self.authenticate_frame = tk.Tk()
        self.authenticate_frame.title("Authenticate")
        # self.register_frame.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.authenticate_frame.resizable(False, False)
        conn, cursor = self.connect_database()
        cursor.execute(
            f"""
                select * from account where username='{self.username.get().lower()}' and password='{self.password.get()}'
            """
        )
        result = list(cursor.fetchone())
        account = {
            "email": result[2],
            "phone": result[3],
            "authy": result[4],
        }

        self.code_label = tk.Label(self.authenticate_frame, text="Insert code: ")
        self.code_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.code = tk.Entry(self.authenticate_frame, width=30)
        self.code.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        match authentication_type:
            case self.AUTHENTICATOR_OPTION.index(0):
                self.EMAIL.send_message(account["email"])
                
            case self.AUTHENTICATOR_OPTION.index(1):
                self.SMS.send_sms(account["phone"])

            # case self.AUTHENTICATOR_OPTION.index(2):
                pass
            case _:
                raise NotImplementedError
        
        self.authenticate_button = tk.Button(self.authenticate_frame, text="Authenticate", width=30, command=self.authenticate)
        self.authenticate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E)

        conn.close()
        self.authenticate_frame.mainloop()

    def authenticate(self) -> None:
        if self.OTP.verify(self.code.get()):
            self.logged_window()

    def login(self) -> None:
        if self.check_login_entry():
            conn, cursor = self.connect_database()
            cursor.execute(
                f"""
                select exists(select username, password from account where username='{self.username.get().lower()}' and password='{self.password.get()}')
                """
            )
            connected = cursor.fetchone()[0]
            self.login_warning.grid(row=4, column=0, columnspan=2, sticky=tk.W)

            if connected:
                self.login_warning.grid_remove()
                self.authenticate_window(self.authentication_choosen.get())

            else:
                self.login_warning.config(text="Username or password is wrong")

    def check_login_entry(self) -> bool:
        return all([self.check_login_username(), self.check_login_password()])

    def register_user(self) -> None:
        if self.check_registry_entrys():
            authy = self.OTP.generate_authenticator(self.email.get())
            phone_with_ddi = "+55" + self.phone.get()
            conn, cursor = self.connect_database()
            cursor.execute(
                f"""
                insert into account (username, password, email, phone, authy) values ('{self.username.get().lower()}', '{self.password.get()}', '{self.email.get().lower()}', '{phone_with_ddi}', '{authy}');
                """
            )
            conn.commit()
            cursor.close()
            qrcode.make(authy).save("./qrcode.png")
            img = Image.open("./qrcode.png")
            img.show()
            self.register_frame.destroy()

    def check_login_username(self) -> bool:
        self.login_username_warning.grid(row=1, column=0, columnspan=2, stick=tk.W)

        if self.username.get().strip() == "" or " " in self.username.get():
            self.login_username_warning.config(text="* Username can't be blank or space or have spaces")
            return False

        if not self.check_if_username_in_use(self.username.get().lower()):
            self.login_username_warning.config(text="* Username not registred")
            return False

        self.login_username_warning.grid_remove()
        return True

    def check_login_password(self) -> bool:
        self.login_password_warning.grid(row=3, column=0, columnspan=2, sticky=tk.W)

        if self.password.get().strip() == "" or " " in self.password.get():
            self.login_password_warning.config(text="* Password can't be blank or space or have spaces")
            return False

        self.login_password_warning.grid_remove()
        return True

    def check_registry_entrys(self) -> bool:
        return all(
            [
                self.check_registry_username(),
                self.check_registry_password(),
                self.check_registry_email(),
                self.check_registry_phone(),
            ]
        )

    def check_registry_username(self) -> bool:
        self.username_warning.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        if self.username.get().strip() == "" or " " in self.username.get():
            self.username_warning.config(text="* Username can't be blank or space or have spaces")
            return False

        if self.check_if_username_in_use(self.username.get().lower()):
            self.username_warning.config(text="* Username already in use")
            return False

        self.username_warning.grid_remove()
        return True

    def check_registry_password(self) -> bool:
        self.password_warning.grid(row=3, column=0, columnspan=2, sticky=tk.W)

        if self.password.get().strip() == "" or " " in self.password.get():
            self.password_warning.config(text="* Password can't be blank or space or have spaces")
            return False
        
        if len(self.password.get()) >=8:
            self.password_warning.config(text="* Password must have at least 8 characters")
            return False

        self.password_warning.grid_remove()
        return True

    def check_registry_email(self) -> bool:
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

    def check_registry_phone(self) -> bool:
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

    def check_code(self) -> bool:
        return self.currrent_code == self.code.get()
