#author: Md lutfar Rahman
#mrahman9@memphis.edu

from tkinter import *

class MyGUI:
    def __init__(self, master, model):
        self.master = master
        self.model = model
        self.suggestion = "Insert emotional text here!"
        master.title("Sentiment Classification")
        master.minsize(width=600, height=400)

        
        self.setupMainFunc()
        self.create_menubar()
        self.setupMyself()
        
        self.center_appear()

    def greet(self):
        print("Greetings!")

    def train(self):
        #self.Trainlabel.configure(text = 'Training ...')
        self.model.train()
        p,r = self.model.runExperiment()
        self.Trainlabel['text'] = 'Training done!!!  precision=%.2f, Recall=%.2f'%(p,r)
        print("Training done!")

    def classify(self):
        #input_tweet = 'I love you'
        input_tweet = self.InputText.get('1.0', 'end')
        result = self.model.classify(input_tweet)
        self.Resultlabel['text'] =  "Result: "+ result + " emotion"
        print(result)

    def setupMainFunc(self):
        MyButton1 = Button(self.master, text="Train and Test", width=20, height=2, command=self.train)
        MyButton1.place(relx=.19, rely=.35, anchor="c")

        MyButton2 = Button(self.master, text="Run Model", width=20, height=2, command=self.classify)
        MyButton2.place(relx=.19, rely=.51, anchor="c")

        self.InputText = Text(self.master, height=10, width=80)
        self.InputText.place(relx=.5, rely=.76, anchor="c")
        self.InputText.insert('1.0', self.suggestion)
        self.InputText.bind("<FocusIn>", self.default)
        self.InputText.bind("<FocusOut>", self.default)

        self.Trainlabel = Label(self.master, text='First Train Your Model!!!')
        self.Trainlabel.place(relx=.60, rely=.35, anchor="c")

        self.Resultlabel = Label(self.master, text='Result: text emotion')
        self.Resultlabel.place(relx=.5, rely=.5, anchor="c")

    def default(self, event):
        current =  self.InputText.get("1.0", 'end')
        if current == self.suggestion+"\n":
             self.InputText.delete("1.0", 'end')
        elif current == "\n":
             self.InputText.insert("1.0", self.suggestion)
   

    def setupMyself(self):
        self.label1 = Label(self.master, text="Natural Language Processing - COMP 8780")
        self.label1.config(font=("Courier", 14))
        self.label1.place(relx=.5, rely=.05, anchor="c")

        self.label2 = Label(self.master, text="Sentiment Classification")
        self.label2.place(relx=.5, rely=.1, anchor="c")

        self.label3 = Label(self.master, text="Md Lutfar Rahman, PhD student, CS")
        self.label3.place(relx=.5, rely=.15, anchor="c")

        self.label4 = Label(self.master, text="mrahman9@memphis.edu")
        self.label4.place(relx=.5, rely=.2, anchor="c")

        self.sep = Frame(self.master,width=400, height=2, bg="black")
        self.sep.place(relx=.5, rely=.25, anchor="c")



    def create_menubar(self):
        root = self.master
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
         
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.greet)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)
 

    def center_appear(self):
        root = self.master
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        size = tuple(int(pos) for pos in root.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        root.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def quit(self):
        self.master.destroy()