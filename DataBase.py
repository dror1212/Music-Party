import pickle
import md5
import Tkinter

class DataBase():
    def __init__(self,name,root):
        self.name = name
        self.root = root
        self.register_screen = None

    def create(self):
        try:
            with open(self.name, 'rb') as data_base:
                b = pickle.load(data_base)
        except:
            with open(self.name, 'wb') as data_base:
                pickle.dump({}, data_base, protocol=pickle.HIGHEST_PROTOCOL)
                
    def get(self):
        x = None
        with open(self.name, 'rb') as data_base:
                x = pickle.load(data_base)
        return x

    def set(self,b):
        with open(self.name, 'wb') as data_base:
            pickle.dump(b, data_base, protocol=pickle.HIGHEST_PROTOCOL)
        
    def check_login(self,name,password,names):
        b = self.get()
        if name in b.keys():
            if name in names.values():
                return "This user is taken"
            elif b[name]==md5.new(password).hexdigest():
                return "Connection accepted"
            else:
                return "Wrong password"
        else:
            return "This username does not exist"

    def check_register(self,username,password):
        b = self.get()
        print b
        if username in b.keys():
            return ("The username " + username + " already exists")
        else:
            if not username.isspace() and not password.isspace() and username!="" and password!="":
                b[username] = md5.new(password).hexdigest()
                print b[username]
                self.set(b)
                return ("Username " + username + " was created succesfully")               
            else:
                return ("You can't leave any tab empty")

    def res(self):
        self.register_screen.destroy()
        self.register_screen = None
        
    def Page(self):
        if self.register_screen == None:
            self.register_screen = Tkinter.Toplevel(self.root)
            self.register_screen.title("Register")
            self.register_screen.geometry("300x250")
            self.register_screen.wm_iconbitmap('pictures\\head.ico')
            self.register_screen.protocol("WM_DELETE_WINDOW", self.res)
            self.register_screen.resizable(0, 0)
            username = Tkinter.StringVar()
            password = Tkinter.StringVar()
     
            self.msg = Tkinter.Label(self.register_screen, text="Please enter details below", bg="grey")
            self.msg.pack()
            Tkinter.Label(self.register_screen, text="").pack()
            username_lable = Tkinter.Label(self.register_screen, text="Username * ")
            username_lable.pack()
            self.username_entry = Tkinter.Entry(self.register_screen, textvariable=username)
            self.username_entry.pack()
            password_lable = Tkinter.Label(self.register_screen, text="Password * ")
            password_lable.pack()
            self.password_entry = Tkinter.Entry(self.register_screen, textvariable=password, show='*')
            self.password_entry.pack()
            Tkinter.Label(self.register_screen, text="").pack()
            Tkinter.Button(self.register_screen, text="Register", width=10, height=1, bg="grey", command = lambda: self.register_user(username.get(),password.get())).pack()
            self.username_entry.focus_set()
            
    def register_user(self,username,password):
        b = self.get()

        check = self.check_register(username,password)
        self.msg.config(text=check)
                
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.username_entry.focus_set()
