import keyboard
from functions import *

# root

root = tk.Tk()

# get user screen and scale window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 5
window_height = screen_height // 4
position_x = int((screen_width / 2) - (window_width / 2))
position_y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
# customization
root.resizable(0, 0)
root.iconbitmap("foss_1.ico")
root.configure(bg = "gray")
root.title("Fossil_dev Terminal")

# input bar

lastcommand = tk.StringVar()
input_bar = tk.Entry(root, bg = "gray", font = ("Courier New Italic", 12), textvariable = lastcommand)
input_bar.focus()
input_bar.pack(side = "bottom", fill = "both", expand = 1, padx = 4, pady = 4)

# console

console = (tk.Text(root, bg = "black", fg = "white", state = "disabled"))
console.config(font = ("Courier New", 10))
console.pack(side = "top", fill = "both", expand = 1, padx = 4, pady = 4)


# hotkeys

def ask_hotkey():
    ask(console, input_bar)


keyboard.add_hotkey("enter", ask_hotkey)

# loop

if __name__ == "__main__":
    root.mainloop()
