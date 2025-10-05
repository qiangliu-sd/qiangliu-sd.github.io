# Free-standing message box, popup, and Tkinter tricks
    Free-standing (non-blocking) message box, pop-up (and pop-off) message box, and more tkinter tricks

I like **Tkinter** because it is distributed with Python as the **standard interface**. To make it work well, customizations are necessary, however.

For my own project, it is helpful to have free-standing (non-blocking) message box and pop-up (and pop-off) message box.

Since they are not readily available online, I have to implement them myself, which I share in this article.

### Free-standing (non-blocking) message box
Tkinter built-in `messagebox` is blocking. This isn't nice for at least two situations.

First, you want to send a message, but you need the App to run without stopping (i.e., **non-blocking**). Second, you want your message to stay after a (scheduled) task is finished (i.e., **free-standing** and of course, non-blocking).

When working with a GUI, launching a `messagebox` from an event, such as a Button click, is non-blocking. Without a GUI, launching a messagebox via a `threading.Thread` is non-blocking. Unfortunately, in both cases, the running Python instances are blocked by the messagebox. In other words, the messagebox is not free-standing.

To make a messagebox free-standing, you need to launch a messagebox from the `subprocess` (with the flag `CREATE_NO_WINDOW`), as follows:
```
def freeMsgBox(title:str, message:str):
    """FREE-standing non-blocking messagebox:
        Launch Py-script (Lib/site-packages/ql_package/qlMsgBox.py) in subprocess
    """
    from sys import executable
    from os import path
    pyDir = path.dirname(executable)
    qlMsgboxPy = path.join(pyDir, r'Lib\site-packages\ql_package', "qlMsgBox.py")

    from subprocess import Popen, CREATE_NO_WINDOW
    Popen(["Python", qlMsgboxPy, title, message], creationflags=CREATE_NO_WINDOW)
```
Further, you have to put the call to `messagebox` inside a Python script, **qlMsgBox.py** in my case:
```
# used by ql_tkUtils.freeMsgBox() to generate:
# 	Free-standing, Non-blocking messagebox

from sys import argv    
from tkinter import messagebox
messagebox.showinfo(argv[1], argv[2])

```

### Pop-up (and pop-off) message box

A fleeting pop-up and pop-off message box can be helpful in two situations. First, you can send a message without bothering a user to click anything. Second, you can automatically take the focus away from the active widget (for example, an `Entry`). This can be useful in forcing the validation of user input that may be left in an invalid state (see my GitHub Repo [Enforced Tkinter-validating](https://github.com/qiangliu-sd/enforcedDynaPyTkValid)).
```
def fleetingPopup(info='I take focus!', out_millisec=20):
    """Show for 20 milliseconds and disappear"""
    from tkinter import Tk
    myWin = Tk()
    myWin.withdraw()    
    try:
        myWin.after(out_millisec, myWin.destroy)
        from tkinter import messagebox
        messagebox.showinfo('DONT click OK-Button', info, master=myWin)
    except Exception: pass
```
Also, see [note](#Note) at the end.

### Two different built-in buttons

`tkinter.ttk` widgets may have better appearances than `tkinter`. As an example, `ttk.Button` looks nicer than `tkinter.Button`. Remember to use **ttk** whenever possible:

![tkinter.Button vs. ttk.Button](images/two_buttons.png)

### My own status bar
There is no built-in status-bar in Tkinter. It is quite simple to define one for your own use with `class`. See the following:
```
class StatusBar:
    """Place [StatusBar] at the bottom of argument [frame]""" 
    def __init__(self, frame):
        from tkinter import Label, LEFT, BOTTOM, X, GROOVE        
        self.label = Label(frame, fg = "gray", bg ="white", bd =1, relief=GROOVE, font=("Arial", 10, "normal"))
        self.label.pack(side = BOTTOM, fill=X)
        self.init()
     
    def show(self, new_txt):
        self.label.config(text = new_txt)
 
    def init(self):
        self.label.config(text = "Status: Ready")
```
### Note
<a name="Note"></a>
The following function does NOT work inside a Button click, probably due to messing with the focus of the Button-GUI:
```
def fleetingPopupNO(info='I take focus!', out_millisec=20):
    "Show for 20 milliseconds and disappear."
    from tkinter import Label, Tk
    myWin = Tk()
    myWin.title("Focus Taker")
    myWin.geometry("250x60")
    msg = f'\n<I will disapear in {out_millisec*0.001} seconds>'
    Label(myWin, text=f"{info}{msg}", fg="red",bd=2).pack(pady=10)
    try:
	myWin.after(out_millisec, myWin.destroy)
	myWin.mainloop() # with or without this statement
    except Exception: pass
```