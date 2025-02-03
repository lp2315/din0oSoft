import tkinter as tk
from tkinter import ttk
import subprocess
from datetime import datetime, timedelta


class ShutdownScheduler:
    def __init__(self, root):
        self.root = root
        root.title("ZzzTimer")
        root.resizable(False, False)
        root.attributes('-topmost', True)
        root.iconbitmap('sleep_icon_154827.ico')
        root.configure(highlightthickness = 4)

        # Core variables
        self.default_font = 'Verdana'
        self.colors = {
            'shutdown': '#ff6b6b',
            'restart': '#77dd77',
            'border_red': '#ff7f50',
            'border_grey': '#808080',
        }

        # Timer settings
        self.minutes = 0
        self.seconds = 10
        self.MIN_SECONDS = 10
        self.MAX_MINUTES = 720

        # State variables
        self.countdown_active = False
        self.shutdown_end_time = None
        self.shutdown_type = None
        self.current_cmd = None

        self.setup_styles()
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding = "15")
        main_frame.grid(row = 0, column = 0, sticky = 'nsew')
        main_frame.grid_columnconfigure(0, weight = 1)

        # Timer section
        timer_frame = ttk.Frame(main_frame)
        timer_frame.grid(row = 0, column = 0, sticky = 'ew', pady = (0, 15))
        timer_frame.grid_columnconfigure(0, weight = 1)

        self.task_label = ttk.Label(
            timer_frame,
            text = "Set timer:",
            style = 'Task.TLabel',
            anchor = 'center'
        )
        self.task_label.grid(row = 0, column = 0, sticky = 'ew')

        self.countdown_label = ttk.Label(
            timer_frame,
            text = f"{self.minutes:02d}:{self.seconds:02d}",
            style = 'Countdown.TLabel',
            anchor = 'center'
        )
        self.countdown_label.grid(row = 1, column = 0, sticky = 'ew', pady = (5, 0))

        # Mouse wheel binding
        self.countdown_label.bind('<Enter>', lambda e: self.countdown_label.focus_set())
        self.countdown_label.bind('<MouseWheel>', self.on_mousewheel)
        self.countdown_label.bind('<Button-4>', self.on_mousewheel)
        self.countdown_label.bind('<Button-5>', self.on_mousewheel)

        # Options frame
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row = 1, column = 0, sticky = 'ew', pady = (0, 15))
        options_frame.grid_columnconfigure(0, weight = 1)

        self.force_var = tk.BooleanVar(value = False)
        self.force_check = ttk.Checkbutton(
            options_frame,
            text = "Force Close Programs",
            variable = self.force_var,
            style = 'Small.TCheckbutton'
        )
        self.force_check.grid(row = 0, column = 0, sticky = 'w')

        self.restart_apps_var = tk.BooleanVar(value = False)
        self.restart_check = ttk.Checkbutton(
            options_frame,
            text = "Restart Programs",
            variable = self.restart_apps_var,
            style = 'Small.TCheckbutton'
        )
        self.restart_check.grid(row = 1, column = 0, sticky = 'w')

        # Action buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row = 2, column = 0, sticky = 'ew', pady = (0, 10))
        btn_frame.grid_columnconfigure((0, 1), weight = 1)
        self.btn_frame = btn_frame

        ttk.Button(
            btn_frame,
            text = "Shutdown",
            command = self.schedule_shutdown,
            style = 'Shutdown.TButton'
        ).grid(row = 0, column = 0, padx = 2)

        ttk.Button(
            btn_frame,
            text = "Restart",
            command = self.schedule_restart,
            style = 'Restart.TButton'
        ).grid(row = 0, column = 1, padx = 2)

        self.cancel_btn = ttk.Button(
            main_frame,
            text = "Cancel Task",
            command = self.cancel_all,
            style = 'Cancel.Inactive.TButton',
            state = 'disabled'
        )
        self.cancel_btn.grid(row = 3, column = 0, sticky = 'ew', pady = (0, 15))

        self.cmd_var = tk.StringVar(value = "<No Task Scheduled>")
        ttk.Label(
            main_frame,
            textvariable = self.cmd_var,
            style = 'Status.TLabel',
            anchor = 'center'
        ).grid(row = 4, column = 0, sticky = 'ew')

    def setup_styles(self):
        style = ttk.Style()
        style.configure('Task.TLabel', font = (self.default_font, 11))
        style.configure('Countdown.TLabel', font = ('Courier', 28, 'bold'))
        style.configure('Status.TLabel', font = (self.default_font, 9), foreground = 'gray')
        style.configure('Small.TCheckbutton', font = (self.default_font, 9))
        style.configure('Shutdown.TButton', font = (self.default_font, 9),
                        background = self.colors['shutdown'])
        style.configure('Restart.TButton', font = (self.default_font, 9),
                        background = self.colors['restart'])
        style.configure('Cancel.Inactive.TButton', font = (self.default_font, 9),
                        borderwidth = 2, relief = 'solid', bordercolor = self.colors['border_grey'])
        style.configure('Cancel.Active.TButton', font = (self.default_font, 9),
                        borderwidth = 2, relief = 'solid', bordercolor = self.colors['border_red'])

    def on_mousewheel(self, event):
        if not self.countdown_active:
            x = self.root.winfo_pointerx() - self.countdown_label.winfo_rootx()
            label_width = self.countdown_label.winfo_width()
            adjusting_minutes = x < (label_width / 2)

            # Calculate current total seconds
            total_seconds = self.minutes * 60 + self.seconds

            # Determine scroll direction
            scroll_up = not (event.num == 5 or event.delta < 0)

            if adjusting_minutes:
                if scroll_up:
                    self.minutes = min(self.MAX_MINUTES, self.minutes + 1)
                else:
                    new_minutes = max(0, self.minutes - 1)
                    if (new_minutes * 60 + self.seconds) >= self.MIN_SECONDS:
                        self.minutes = new_minutes
            else:
                if scroll_up:
                    self.seconds += 1
                    if self.seconds > 59:
                        self.seconds = 0
                        if self.minutes < self.MAX_MINUTES:
                            self.minutes += 1
                else:
                    new_seconds = self.seconds - 1
                    if new_seconds < 0:
                        if self.minutes > 0:
                            self.minutes -= 1
                            self.seconds = 59
                        else:
                            self.seconds = self.MIN_SECONDS
                    else:
                        if (self.minutes * 60 + new_seconds) >= self.MIN_SECONDS:
                            self.seconds = new_seconds

            # Update display
            self.countdown_label.configure(text = f"{self.minutes:02d}:{self.seconds:02d}")

    def update_countdown(self):
        if not self.countdown_active:
            return

        current_time = datetime.now()
        if current_time >= self.shutdown_end_time:
            self.countdown_active = False
            return

        remaining = self.shutdown_end_time - current_time
        seconds_left = max(0, int(remaining.total_seconds()))

        # Update countdown display with seconds
        self.countdown_label.configure(text = str(seconds_left))

        # Update task label with scheduled time
        scheduled_time = self.shutdown_end_time.strftime("%H:%M")
        self.task_label.configure(text = f"{self.shutdown_type} at {scheduled_time}")

        self.cmd_var.set(self.current_cmd)

        # Schedule the next update in 1000ms (1 second)
        self.root.after(1000, self.update_countdown)

    def start_countdown(self, seconds, shutdown_type, cmd):
        self.shutdown_type = shutdown_type
        self.current_cmd = cmd
        self.shutdown_end_time = datetime.now() + timedelta(seconds = seconds)
        self.countdown_active = True

        self.update_button_states(timer_active = True)
        self.update_window_border(type = shutdown_type)

        # Initial display update
        scheduled_time = self.shutdown_end_time.strftime("%H:%M")
        self.task_label.configure(text = f"{shutdown_type} at {scheduled_time}")
        self.countdown_label.configure(text = str(seconds))
        self.update_cancel_button(active = True)

        # Start the countdown immediately
        self.update_countdown()

    def update_window_border(self, type = None):
        color = {
            "Shutting Down": self.colors['shutdown'],
            "Restarting": self.colors['restart']
        }.get(type, self.colors['border_grey'])

        self.root.configure(highlightbackground = color,
                            highlightcolor = color,
                            highlightthickness = 4)

    def update_button_states(self, timer_active = False):
        state = 'disabled' if timer_active else 'normal'
        for child in self.btn_frame.winfo_children():
            child.configure(state = state)
        self.cancel_btn.configure(state = 'normal' if timer_active else 'disabled')
        self.force_check.configure(state = state)
        self.restart_check.configure(state = state)

    def update_cancel_button(self, active = False):
        style = 'Cancel.Active.TButton' if active else 'Cancel.Inactive.TButton'
        self.cancel_btn.configure(style = style)

    def schedule_shutdown(self):
        total_seconds = self.minutes * 60 + self.seconds
        flags = "/f" if self.force_var.get() else ""
        cmd = f'shutdown /s /t {total_seconds} {flags}'.strip()
        subprocess.run(cmd, shell = True)
        self.cmd_var.set(cmd)
        self.start_countdown(total_seconds, "Shutting Down", cmd)

    def schedule_restart(self):
        total_seconds = self.minutes * 60 + self.seconds
        flags = "/f" if self.force_var.get() else ""
        restart_flag = "/g" if self.restart_apps_var.get() else "/r"
        cmd = f'shutdown {restart_flag} /t {total_seconds} {flags}'.strip()
        subprocess.run(cmd, shell = True)
        self.cmd_var.set(cmd)
        self.start_countdown(total_seconds, "Restarting", cmd)

    def cancel_all(self):
        try:
            subprocess.run('shutdown /a', shell = True)
        except:
            pass

        self.countdown_active = False
        self.shutdown_type = None
        self.current_cmd = None

        self.update_button_states(timer_active = False)
        self.update_window_border()

        self.task_label.configure(text = "Set timer:")
        self.minutes = 0
        self.seconds = 10
        self.countdown_label.configure(text = f"{self.minutes:02d}:{self.seconds:02d}")
        self.cmd_var.set("<No Task Scheduled>")
        self.update_cancel_button(active = False)


if __name__ == '__main__':
    root = tk.Tk()
    app = ShutdownScheduler(root)
    root.mainloop()
