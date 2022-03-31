from chatbot_meta import *
from tkinter import *

res = bot()
def send():
    # get the message text
    msg = EntryBox.get("1.0",'end-1c')
    EntryBox.delete("0.0",END)
    Chat.config(state=NORMAL)
    Chat.insert(END, "You: " + msg + '\n\n')
    Chat.config(foreground="#442265", font=("Verdana", 12 ))

    nbot = res.send(None)   
    try: 
        Chat.insert(END, "Bender: " + nbot + '\n\n', )
    except: 
        nbot = res.send(msg)
        Chat.insert(END, "Bender: " + nbot +  '\n\n', )
    Chat.config(state=DISABLED)
    Chat.yview(END)


base = Tk() # Create a window
base.iconbitmap(r"\bender.ico")
base.title("Bender ChatBot")
base.geometry("800x500") # Size of the window
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
Chat = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
Chat.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=Chat.yview)
Chat['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")

#Place all components on the screen
scrollbar.place(x=780,y=6, height=386)
Chat.place(x=6,y=6, height=386, width=775)
EntryBox.place(x=128, y=401, height=90, width=665)
SendButton.place(x=6, y=401, height=90)

base.mainloop()