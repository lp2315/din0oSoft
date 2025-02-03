import datetime as dt
import random
import tkinter as tk
from tkinter import filedialog
from tkinter.constants import END

help_message = "HELP TEXT"
info_message = "WELCOME TO Fossil_dev CONSOLE"
error_message = "NO SUCH COMMAND..."

#


def rnd_hexcode():
    x = random.randrange(0, 16777215, 1)
    x = str((hex(x))[2:])
    return str("#" + ('{:<06}'.format(x)))


def remove_until_last_slash(input_string):
    # Find the position of the last "/"
    last_slash_index = input_string.rfind('/')
    # Slice the string up to the last "/"
    if last_slash_index != -1:
        return input_string[:last_slash_index + 1]
    else:
        pass


def save_console_log(console = tk.Text, file_path = str):
    # copy console to txt file
    text_widget = console
    text_content = text_widget.get("1.0", tk.END)
    with open(file_path, 'a') as file:
        file.write(text_content)


def get_file_path(input_bar = tk.Entry) -> str:
    # initialize root & hide it
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    input_bar.delete(0, END)
    # return file path as str
    return str(file_path)


def ask(console = tk.Text, input_bar = tk.Entry):
    timestamp = dt.datetime.now()
    msg = str(input_bar.get())
    console.tag_config("ask", foreground = "white")
    console.tag_config("system", foreground = "yellow")

    # enable console & insert msg
    console.config(state = "normal")
    console.insert("1.0", str(timestamp.strftime('%H:%M - ') + msg + "\n"), "ask")

    # test
    if msg == "§":
        console.insert("-1.0", "> " + error_message + "\n", "system")
        pass

    # help message
    elif msg == "§help":
        console.insert("-1.0", "> " + help_message + "\n", "system")

    # random formatted hex code
    elif msg == "§hex":
        h = rnd_hexcode()
        console.insert("-1.0", "> " + h + "\n", "system")

    # exports console text to file
    elif msg == "§export":
        try:
            file_path = get_file_path(input_bar)
            save_console_log(console, file_path)
            console.insert("1.0", "> " + "exported to " + file + "\n")
        except FileNotFoundError:
            pass

    # disable console & clear input bar
    console.config(state = "disabled")
    input_bar.delete(0, END)
