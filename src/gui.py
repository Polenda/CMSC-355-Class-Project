from tkinter import *
from tkinter import ttk

class Gui:
    def __init__(self, root):
        root.title("CMSC-355 Class Project")

        # example users
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
        send_button = ttk.Button(content_frame, text="Disconnect", command=self.disconnect)
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
        self.username_label = ttk.Label(content_frame, text="Username:")
        self.username_label.grid(column=1, row=1, columnspan=2, sticky=W, padx=5, pady=(5, 0))
        username_entry = ttk.Entry(content_frame, width=40, textvariable=self.username)
        username_entry.grid(column=1, row=2, columnspan=2, sticky=(W, E), padx=5, pady=5)

        # password entry box
        self.password = StringVar()
        self.password_label = ttk.Label(content_frame, text="Password:")
        self.password_label.grid(column=1, row=3, columnspan=2, sticky=W, padx=5, pady=(5, 0))
        password_entry = ttk.Entry(content_frame, width=40, textvariable=self.password, show='*')
        password_entry.grid(column=1, row=4, columnspan=2, sticky=(W, E), padx=5, pady=5)

        # login button
        login_button = ttk.Button(content_frame, text="Login", default='active', state='disabled', command=self.login)
        login_button.grid(column=2, row=5, sticky=E, padx=5, pady=5)
        self.window.bind('<Key-Return>', lambda e:login_button.invoke())

        # cancel button
        cancel_button = ttk.Button(content_frame, text="Cancel", command=self.disconnect)
        cancel_button.grid(column=1, row=5, sticky=W, padx=5, pady=5)
        self.window.bind('<Key-Escape>', lambda e:cancel_button.invoke())

        username_entry.focus()

        # enable login button if both username and password are filled
        def check_fields(*args):
            if self.username.get() and self.password.get():
                login_button.config(state='normal')
            else:
                login_button.config(state='disabled')

        self.username.trace_add('write', check_fields)
        self.password.trace_add('write', check_fields)

    def send_window(self, root, *user):
        self.window = Toplevel(root)
        self.window.title("Send Message")
        self.recipient = self.selected_user

        # main frame
        content_frame = ttk.Frame(self.window, padding='5 5 5 5')
        content_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.resizable(0, 0)

        # message box
        ttk.Label(content_frame, text=f"Send Message to {self.recipient}:").grid(column=1, row=1, columnspan=2, sticky=(W, E))
        self.message = StringVar()
        self.message_entry = Text(content_frame, width=40, height=10, wrap='word')
        self.message_entry.grid(column=1, row=2, columnspan=2, sticky=(W, E))

        # send button
        send_button = ttk.Button(content_frame, text="Send", default='active', command=self.send)
        send_button.grid(column=2, row=3, sticky=E)
        self.window.bind('<Key-Return>', lambda e:send_button.invoke())

        # cancel button
        cancel_button = ttk.Button(content_frame, text="Cancel", command=self.close_window)
        cancel_button.grid(column=1, row=3, sticky=W)
        self.window.bind('<Key-Escape>', lambda e:cancel_button.invoke())

        for child in content_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.message_entry.focus()

    # open window to send message
    def send_message(self, *user):
        self.send_window(root)

    # send message
    def send(self, *user):
        message = self.message_entry.get('1.0', 'end-1c')
        message = message[0:128]
        print(f"Sending message to {self.recipient}: \"{message}\"")
        self.close_window()

    # disconnect from chat and close entire program
    def disconnect(self):
        self.window.destroy()
        root.destroy()

    # close invoking window
    def close_window(self):
        self.window.destroy()
    
    # login to chat and open main window
    def login(self):
        username = self.username.get()
        pw = self.password.get()

        # USERNAME CHECKING
        if not 13 > len(username) > 0:
            print("Invalid username length (0 - 13)")
            self.username_label.configure(text="Username: (invalid username or password)")
            return
        elif not username.isalnum():
            print("Invalid characters (Alphanumeric characters only)")
            self.username_label.configure(text="Username: (invalid username or password)")
            return
        else:
            self.username_label.configure(text="Username:")
        # if self.username.get() doesn't exist:
        #   return

        # PASSWORD CHECKING
        if not 100 > len(pw) > 4:
            print("Invalid password size (4 - 100)")
            self.username_label.configure(text="Username: (invalid username or password)")
            return
        else:
            self.username_label.configure(text="Username:")
        # if pw doesn't match with the password of the username:
        #   return

        print(f"Logging in {username}")
        print(f"Password: {pw}")

        self.window.destroy()
        self.main_window(root)

root = Tk()
Gui(root)
root.mainloop()