import tkinter as tk


# Formica
# tkinter config window
root = tk.Tk()
window_width = 300
window_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_x = int((screen_width / 2) - (window_width / 2))
position_y = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
root.resizable(0,0)


class SliderWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Formica config")

        self.sliders = []
        labels = ["Rows", "Columns", "Scaling", "Speed"]
        ranges = [(3, 15), (3, 25), (40, 60), (0, 2)]

        for i in range(4):
            label = tk.Label(master, text = labels[i])
            label.pack()
            slider = tk.Scale(master, from_ = ranges[i][0], to = ranges[i][1], orient = tk.HORIZONTAL)
            slider.set((ranges[i][0] + ranges[i][1]) // 2)
            slider.config()
            slider.pack(fill = tk.X)
            self.sliders.append(slider)

        float_slider = tk.DoubleVar()
        self.sliders[3].config(variable = float_slider, resolution = 0.05)
        self.sliders[3].set((ranges[3][0] + ranges[3][1]) // 2)
        self.button = tk.Button(master, relief=tk.GROOVE, fg = 'BLUE', pady = 4, padx = 12, text = "START", command = self.get_values)
        self.button.pack(expand = True)

        self.values = None

    def get_values(self):
        self.values = [slider.get() for slider in self.sliders]
        self.master.destroy()


# loop then pass on values
def main():
    app = SliderWindow(root)
    root.mainloop()
    return app.values
