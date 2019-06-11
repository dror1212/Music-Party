import pickle
import md5

class DataBase():
    def __init__(self,name):
        self.name = name

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
        
        if username in b.keys():
            return ("The username " + username + " already exists")
        else:
            if not username.isspace() and not password.isspace() and username!="" and password!="":
                b[username] = md5.new(password).hexdigest()
                print b[username]
                return ("Username " + username + " was created succesfully")
                self.data.set(b)
            else:
                return ("You can't leave any tab empty")
