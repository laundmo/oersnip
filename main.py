# Import Library
from tkinter import Entry, Listbox, StringVar, Tk, END
import tkinter.font as font
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip

from win32gui import GetForegroundWindow, SetForegroundWindow


# Create Object
root = Tk()

# Set title
root.title("Main Window")

# Set Geometry
root.geometry("400x200")

font_cmu = font.Font(
    root=root,
    font=(
        "CMU Serif",
        20,
    ),
    name="CMU Serif",
)

snippetname = StringVar()

text = Entry(root, textvariable=snippetname, font=font_cmu, justify="center")
text.pack()


def on_key(*args):
    update_listbox()


snippetname.trace("w", on_key)


class MyListbox(Listbox):
    def __init__(self, *args, **kwargs):
        Listbox.__init__(self, *args, **kwargs)
        self.current_selection = 0

    def select(self, index):
        self.select_clear(0, "end")
        self.selection_set(index)
        self.see(index)
        self.activate(index)
        self.selection_anchor(index)

    def up(self, *args):
        self.current_selection -= 1
        self.select(self.current_selection)

    def down(self, *args):
        self.current_selection += 1
        self.select(self.current_selection)


lb = MyListbox(root, font=font_cmu)
lb.pack()

root.bind("<Up>", lb.up)
root.bind("<Down>", lb.down)

all_items = ["test1", "test2", "test3"]


def update_listbox(*args):
    search_term = snippetname.get()
    lb.delete(0, END)
    for item in all_items:
        if search_term.lower() in item.lower():
            lb.insert(END, item)


prev_window = None

def show():
    global prev_window
    prev_window = GetForegroundWindow()

    root.deiconify()
    text.focus()


# Hide the window
def hide():
    root.withdraw()
    if prev_window:
        SetForegroundWindow(prev_window)


is_hidden = False


def check_state():
    global is_hidden
    if is_hidden:
        show()
    else:
        hide()
    is_hidden = not is_hidden


keyboard.GlobalHotKeys({"<cmd>+<space>": check_state}).__enter__()

keyboard = Controller()

def paste_and_close(*args): # TODO: why does this only trigger when the mouse is hovering on top of the window?
    text = lb.get(lb.curselection())
    pyperclip.copy(text)
    hide()
    keyboard.press(Key.ctrl)
    keyboard.press("v")
    keyboard.release("v")
    keyboard.release(Key.ctrl)


root.bind("<Enter>", paste_and_close)

# Execute Tkinter
root.mainloop()