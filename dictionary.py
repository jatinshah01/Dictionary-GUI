import json
import tkinter as tk 
from tkinter import messagebox 
from PIL import Image, ImageTk
import requests

class JSL_dictionary:
    def __init__(self,root):
        self.root = root
        self.recheck = False
        self.heading = tk.Label(root, font=("Helvetica",30,"bold") ,fg="snow",text="JSL Dictionary",bg="gray14")
        self.heading.place(x=50,y=30)
        self.frame2 = tk.Frame(root,height=25, highlightbackground="cyan",highlightthickness=2,width=470,bg="snow")
        self.frame2.place(x=25,y=100)
        # self.frame2.config(highlightbackground="cyan")
        self.searchbox = tk.Entry( self.frame2, font=("Comic Sans MS", 13,"bold"), width=30,bg="snow")
        self.searchbox.pack(side=tk.LEFT,padx=1,pady=1)
        self.pil_image = Image.open("C:\\Users\\jatin\\Desktop\\Jatin\\search.png")
        self.resized_image = self.pil_image.resize((19, 19))
        # self.words = self.searchbox.get()
        # print(self.words)
        self.image = ImageTk.PhotoImage(self.resized_image)
        self.btn = tk.Button(self.frame2, borderwidth=2,image=self.image, height=24,width=25 , bg="gray",command=lambda:self.onclick(self.searchbox.get()))
        self.btn.pack(side=tk.LEFT,padx=1,pady=1)
        self.btn.config(activebackground="snow")

    
        self.canvas  = tk.Canvas(root, width=300,height=100)
        self.canvas.place(x=40,y=170)
        
        self.recent = tk.Label(root, height=2,width=15, text="Recent Activity : ", fg="snow" ,font=("Comic Sans MS",12,"bold"),bg="gray14")
        self.recent.place(x=0,y=290)

        self.frame2 = tk.Frame(root,height=30,width=320)
        self.frame2.place(x=20, y=340)
        self.buttons = {}
        for col in range(5):
               self.btn1= tk.Button(self.frame2, height=2,width=9,command=lambda col=col: self.onlist(col) ) 
               self.btn1.grid(row=0,column=col)
               self.buttons[col] = self.btn1
    

        with open("my.json","r") as file:
            myfile = json.load(file)
        print(myfile['words'])
        if len(myfile['words']) == 0:
             self.my_words_list = []

        else:
             self.my_words_list = myfile['words']
             self.display_data(self.my_words_list)

    def onlist(self,col):
        listbtn = self.buttons[col] 
        for  key in self.my_words_list:
            if key == listbtn["text"]:
               self.recheck = True
               self.onclick(key)
               return 0 

    def onclick(self, word):
            # try:
                self.btn['state'] = "disabled"
                self.canvas.delete("all")
                url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
                response = requests.get(url)
                data = response.json()
                data1 = data[0]
                data2 = data1["meanings"][0]
                definations = data2["definitions"][0]
                self.answer = definations["definition"]
            
                self.canvas.create_text(150,50,text=self.answer,anchor=tk.CENTER, font=("Comic Sans MS",10, "bold"),width=250)
                if self.recheck == False:
                    self.updatedata(word)
                else:
                    self.btn['state'] = "normal"
                    self.recheck = False
            # except:
            #     messagebox.showerror("invalid word", "Try another word")
    
    
    def updatedata(self,word):
        word = word
        self.btn['state'] = "normal"
        self.my_words_list.insert(0,word)
        with open("my.json","w") as file:
            datatosave = {"words":self.my_words_list}
            json.dump(datatosave,file)
        with open("my.json", 'r') as file:
            data = json.load(file)
            words_list = data["words"]
            # print(words_list)
        self.display_data(words_list)

    def display_data(self, data):
        for btn in range(len(data)):
            if btn<=4:
                self.buttons[btn]["text"] = data[btn]
            else:
                self.my_words_list.pop()
                break
        self.recheck=False

           
root = tk.Tk()
root.title("JSL Dictionary")
root.geometry("400x400")
root.configure(bg='gray14')
JSL_dictionary(root)
root.mainloop()