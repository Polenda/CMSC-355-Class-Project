from tkinter import *
from tkinter import ttk

class Gui:
    def __init__(self, root):
        root.title("CMSC-355 Class Project")

        self.users = ["Red", "Blue", "Green"]

        self.login_window(root)
        # self.main_window(root)
        # self.send_window(root)

        root.withdraw()

    def main_window(self, root, *user):
        self.window = Toplevel(root)
        self.window.title("Messages")
        self.selected_user = "None"

        # main frame
        content_frame = ttk.Frame(self.window, padding='5 5 5 5')
        content_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.resizable(0, 0)

        # user select
        users_frame = ttk.LabelFrame(content_frame, text="Users")
        users_frame.grid(column=1, row=1, sticky=(N, W, E, S))
        users_var = StringVar(value=self.users)
        users_list = Listbox(users_frame, listvariable=users_var, selectmode=SINGLE)
        users_list.grid(sticky=(N, W, E, S))
        users_list.bind("<<ListboxSelect>>", lambda e:show_chat())

        # active chat
        chat_frame = ttk.LabelFrame(content_frame, text=self.selected_user)
        chat_frame.grid(column=2, row=1, sticky=(N, W, E, S))
        active_chat = Text(chat_frame, state='disabled', width=40, wrap='word')
        active_chat.grid(column=0, row=0, sticky=(N, W, E, S))

        # send message button
        send_button = ttk.Button(content_frame, text="Send Message", command=self.send_message)
        send_button.grid(column=2, row=2, sticky=(W, E))

        # disconnect button
        # make it open login screen and also disconnect client from server
        send_button = ttk.Button(content_frame, text="Disconnect", command=self.close)
        send_button.grid(column=1, row=2, sticky=(W, E))

        for child in content_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

        def show_chat():
            self.selected_user = self.users[users_list.curselection()[0]]
            print(f"Selected user: {self.selected_user}")
            chat_frame.configure(text=self.selected_user)


    def login_window(self, root):
        self.window = Toplevel(root)
        self.window.title("Login")

        # main frame
        content_frame = ttk.Frame(self.window, padding='5 5 5 5')
        content_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.resizable(0, 0)

        # username entry box
        self.username = StringVar()
        username_entry = ttk.Entry(content_frame, width=20, textvariable=self.username)
        username_entry.grid(column=2, row=1, sticky=(W, E))

        # password entry box
        self.password = StringVar()
        password_entry = ttk.Entry(content_frame, width=20, textvariable=self.password, show='*')
        password_entry.grid(column=2, row=2, sticky=(W, E))

        # login button
        ttk.Label(content_frame, text="Username:").grid(column=1, row=1, sticky=E)
        login_button = ttk.Button(content_frame, text="Login", default='active', command=self.login)
        login_button.grid(column=2, row=3, sticky=E)
        self.window.bind('<Key-Return>', lambda e:self.login())

        # cancel button
        ttk.Label(content_frame, text="Password:").grid(column=1, row=2, sticky=E)
        cancel_button = ttk.Button(content_frame, text="Cancel", command=self.close)
        cancel_button.grid(column=1, row=3, sticky=W)
        self.window.bind('<Key-Escape>', lambda e:self.close())

        for child in content_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        username_entry.focus()

    def send_window(self, root, *user):
        self.window = Toplevel(root)
        self.window.title("Send Message")

        # main frame
        content_frame = ttk.Frame(self.window, padding='5 5 5 5')
        content_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.resizable(0, 0)

        # message box
        ttk.Label(content_frame, text="Send message").grid(column=1, row=1, columnspan=2, sticky=(W, E))
        self.message = StringVar()
        message_entry = Text(content_frame, width=40, height=10, wrap=WORD)
        message_entry.grid(column=1, row=2, columnspan=2, sticky=(W, E))

        # send button
        send_button = ttk.Button(content_frame, text="Send", default='active')
        send_button.grid(column=2, row=3, sticky=E)

        # cancel button
        cancel_button = ttk.Button(content_frame, text="Cancel", command=self.cancel)
        cancel_button.grid(column=1, row=3, sticky=W)

        for child in content_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        message_entry.focus()

    def send_message(self, *user):
        self.send_window(root)

    def close(self):
        self.window.destroy()
        root.destroy()

    def cancel(self):
        self.window.destroy()
    
    def login(self):
        username = self.username.get()
        pw = self.password.get()

        # USERNAME CHECKING
        if not 13 > len(username) > 0:
            print("Invalid username length (0 - 13)")
            return
        if not username.isalnum():
            print("Invalid characters (Alphanumeric characters only)")
            return
        # if self.username.get() doesn't exist:
        #   return

        # PASSWORD CHECKING
        if not 100 > len(pw) > 4:
            print("Invalid password size (4 - 100)")
            return
        # if pw doesn't match with the password of the username:
        #   return

        print(f"Logging in {username}")
        print(f"Password: {pw}")

        self.window.destroy()
        self.main_window(root)

root = Tk()
Gui(root)
root.mainloop()