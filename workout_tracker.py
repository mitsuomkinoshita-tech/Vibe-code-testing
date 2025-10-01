import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import time

class WorkoutTrackerApp:
    def __init__(self, root):
        """
        Initialize the application state and build the GUI.
        
        Configure the top-level window (title, size, background), initialize data structures for workouts and timer state (workouts list, timer_seconds, timer_running, rest_time), and construct all UI widgets by calling create_widgets.
        
        Parameters:
            root (tk.Tk): The Tk root window used as the application's main window.
        """
        self.root = root
        self.root.title("Workout Tracker")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f4ff")
        
        self.workouts = []
        self.timer_seconds = 0
        self.timer_running = False
        self.rest_time = 90
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        """
        Builds the main application UI: header and tabbed interface, and populates each tab.
        
        Creates a header bar with the app title, initializes a ttk.Notebook stored on self.notebook, adds two tabs labeled "Track Workout" and "Analytics", and calls create_tracker_tab and create_analytics_tab to populate their contents.
        """
        header_frame = tk.Frame(self.root, bg="#4f46e5", pady=15)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="💪 Workout Tracker", 
                              font=("Arial", 24, "bold"), bg="#4f46e5", fg="white")
        title_label.pack()
        
        # Tab Control
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tracker Tab
        tracker_frame = tk.Frame(self.notebook, bg="#f0f4ff")
        self.notebook.add(tracker_frame, text="Track Workout")
        
        # Analytics Tab
        analytics_frame = tk.Frame(self.notebook, bg="#f0f4ff")
        self.notebook.add(analytics_frame, text="Analytics")
        
        self.create_tracker_tab(tracker_frame)
        self.create_analytics_tab(analytics_frame)
        
    def create_tracker_tab(self, parent):
        # Rest Timer Section
        """
        Create and lay out the "Track Workout" tab UI, including the rest timer controls, inputs for logging sets, and the scrollable recent-sets list.
        
        Parameters:
            parent (tk.Widget): Parent container (tab frame) to which the tracker UI widgets are attached.
        
        Description:
            - Builds a Rest Timer section with a configurable rest-time Spinbox, a large timer display, and Start/Pause/Reset controls.
            - Builds a Log Set section with fields for exercise name, weight, and reps and an "Add Set" button.
            - Builds a Recent Sets section containing a scrollable Listbox of logged sets and a "Delete Selected" button.
            - Stores widget state variables (e.g., rest_time_var, exercise_var, weight_var, reps_var) and key widget references (timer_label, start_btn, pause_btn, workout_listbox) on the instance for use by timer and data-management methods.
        """
        timer_frame = tk.LabelFrame(parent, text="Rest Timer", font=("Arial", 12, "bold"),
                                   bg="#e0e7ff", padx=15, pady=15)
        timer_frame.pack(fill=tk.X, padx=10, pady=10)
        
        rest_time_frame = tk.Frame(timer_frame, bg="#e0e7ff")
        rest_time_frame.pack()
        
        tk.Label(rest_time_frame, text="Rest Time (seconds):", 
                font=("Arial", 10), bg="#e0e7ff").pack(side=tk.LEFT, padx=5)
        
        self.rest_time_var = tk.IntVar(value=90)
        rest_spinbox = tk.Spinbox(rest_time_frame, from_=10, to=600, 
                                  textvariable=self.rest_time_var, width=10)
        rest_spinbox.pack(side=tk.LEFT, padx=5)
        
        self.timer_label = tk.Label(timer_frame, text="1:30", 
                                    font=("Arial", 36, "bold"), 
                                    fg="#4f46e5", bg="#e0e7ff")
        self.timer_label.pack(pady=10)
        
        button_frame = tk.Frame(timer_frame, bg="#e0e7ff")
        button_frame.pack()
        
        self.start_btn = tk.Button(button_frame, text="▶ Start", 
                                   command=self.start_timer, bg="#10b981", 
                                   fg="white", font=("Arial", 10, "bold"), 
                                   padx=15, pady=5)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(button_frame, text="⏸ Pause", 
                                   command=self.pause_timer, bg="#eab308", 
                                   fg="white", font=("Arial", 10, "bold"), 
                                   padx=15, pady=5, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="↻ Reset", command=self.reset_timer,
                 bg="#6b7280", fg="white", font=("Arial", 10, "bold"), 
                 padx=15, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Log Set Section
        log_frame = tk.LabelFrame(parent, text="Log Set", font=("Arial", 12, "bold"),
                                 bg="#f3f4f6", padx=15, pady=15)
        log_frame.pack(fill=tk.X, padx=10, pady=10)
        
        input_frame = tk.Frame(log_frame, bg="#f3f4f6")
        input_frame.pack(fill=tk.X)
        
        tk.Label(input_frame, text="Exercise:", bg="#f3f4f6").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.exercise_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.exercise_var, width=30).grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(input_frame, text="Weight (lbs):", bg="#f3f4f6").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.weight_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.weight_var, width=15).grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        
        tk.Label(input_frame, text="Reps:", bg="#f3f4f6").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reps_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.reps_var, width=15).grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)
        
        tk.Button(log_frame, text="➕ Add Set", command=self.add_workout,
                 bg="#4f46e5", fg="white", font=("Arial", 11, "bold"),
                 padx=20, pady=8).pack(pady=10)
        
        # Recent Sets Section
        sets_frame = tk.LabelFrame(parent, text="Recent Sets", font=("Arial", 12, "bold"),
                                  bg="#ffffff", padx=10, pady=10)
        sets_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollable list
        scroll_frame = tk.Frame(sets_frame, bg="#ffffff")
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.workout_listbox = tk.Listbox(scroll_frame, yscrollcommand=scrollbar.set,
                                         font=("Arial", 10), height=10)
        self.workout_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.workout_listbox.yview)
        
        tk.Button(sets_frame, text="🗑 Delete Selected", command=self.delete_workout,
                 bg="#ef4444", fg="white", font=("Arial", 10, "bold"),
                 padx=15, pady=5).pack(pady=5)
        
    def create_analytics_tab(self, parent):
        """
        Create and populate the Analytics tab UI for displaying per-exercise statistics.
        
        Sets up a scrollable area inside the given parent widget and stores references to the inner frame and a placeholder label:
        - self.analytics_frame: frame where analytics cards will be rendered.
        - self.no_data_label: label shown when there are no workouts to display.
        
        Parameters:
            parent (tk.Widget): The container widget (tab) to build the analytics UI into.
        """
        header = tk.Label(parent, text="📊 Analytics Dashboard", 
                         font=("Arial", 18, "bold"), bg="#f0f4ff")
        header.pack(pady=20)
        
        # Scrollable analytics frame
        canvas = tk.Canvas(parent, bg="#f0f4ff")
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.analytics_frame = tk.Frame(canvas, bg="#f0f4ff")
        
        self.analytics_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.analytics_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # Initial message
        self.no_data_label = tk.Label(self.analytics_frame, 
                                     text="No data yet.\nLog some workouts to see your analytics!",
                                     font=("Arial", 12), bg="#f0f4ff", fg="#6b7280")
        self.no_data_label.pack(pady=50)
        
    def format_time(self, seconds):
        """
        Format a duration given in seconds as "M:SS".
        
        Parameters:
            seconds (int): Total seconds to format.
        
        Returns:
            formatted_time (str): String representation with minutes and zero-padded two-digit seconds, e.g. "3:05".
        """
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"
        
    def start_timer(self):
        """
        Start the rest countdown and update the timer controls.
        
        Initializes the countdown from the current rest time value, marks the timer as running, disables the Start button, enables the Pause button, and begins the timer loop that updates the display.
        """
        if not self.timer_running:
            self.rest_time = self.rest_time_var.get()
            self.timer_seconds = self.rest_time
            self.timer_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.run_timer()
            
    def run_timer(self):
        """
        Advance the rest timer by one second, refresh the displayed time, and either schedule the next tick or stop the timer when it reaches zero.
        
        When the timer is running and remaining seconds are greater than zero, updates the timer label to show the current minutes:seconds, decrements the remaining seconds, and schedules the next invocation. When remaining seconds reach zero, stops the timer, resets start/pause button states, and sets the display to "0:00".
        """
        if self.timer_running and self.timer_seconds > 0:
            self.timer_label.config(text=self.format_time(self.timer_seconds))
            self.timer_seconds -= 1
            self.root.after(1000, self.run_timer)
        elif self.timer_seconds == 0:
            self.timer_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.timer_label.config(text="0:00")
            
    def pause_timer(self):
        """
        Pause the active rest timer and update timer controls.
        
        Stops the countdown and enables the Start button while disabling the Pause button so the timer can be resumed later.
        """
        self.timer_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
    def reset_timer(self):
        """
        Stop the rest timer and reset it to the configured rest duration.
        
        Updates the remaining seconds to the current rest duration, updates the timer display, and sets control buttons so Start is enabled and Pause is disabled.
        """
        self.timer_running = False
        self.rest_time = self.rest_time_var.get()
        self.timer_seconds = self.rest_time
        self.timer_label.config(text=self.format_time(self.rest_time))
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
    def add_workout(self):
        """
        Logs a new workout set from the current input fields and updates the UI and analytics.
        
        Validates the exercise, weight, and reps fields; shows a warning if any field is empty and an error if weight or reps are not numeric. On success, creates a workout record containing exercise, weight, reps, computed volume, and timestamp; prepends it to self.workouts, inserts a formatted entry at the top of the recent-sets listbox, clears the input fields, and refreshes the analytics view.
        """
        exercise = self.exercise_var.get().strip()
        weight_str = self.weight_var.get().strip()
        reps_str = self.reps_var.get().strip()
        
        if not exercise or not weight_str or not reps_str:
            messagebox.showwarning("Missing Data", "Please fill in all fields!")
            return
            
        try:
            weight = float(weight_str)
            reps = int(reps_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Weight and reps must be numbers!")
            return
            
        workout = {
            'exercise': exercise,
            'weight': weight,
            'reps': reps,
            'volume': weight * reps,
            'date': datetime.now()
        }
        
        self.workouts.insert(0, workout)
        
        # Add to listbox
        display_text = f"{exercise} - {weight} lbs × {reps} reps = {workout['volume']:.0f} lbs"
        self.workout_listbox.insert(0, display_text)
        
        # Clear inputs
        self.exercise_var.set("")
        self.weight_var.set("")
        self.reps_var.set("")
        
        self.update_analytics()
        
    def delete_workout(self):
        """
        Delete the currently selected workout from the Recent Sets list and refresh the analytics.
        
        If no workout is selected, displays a warning and leaves data unchanged. When a selection exists, removes the item from the listbox, deletes the corresponding entry from the internal workouts list, and calls update_analytics() to rebuild the analytics view.
        """
        selection = self.workout_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a workout to delete!")
            return
            
        index = selection[0]
        self.workout_listbox.delete(index)
        del self.workouts[index]
        self.update_analytics()
        
    def update_analytics(self):
        # Clear previous analytics
        """
        Rebuilds the analytics view to display per-exercise summary cards based on stored workout entries.
        
        Clears any existing analytics widgets and, if there are no logged workouts, shows a placeholder message. For each exercise present in self.workouts, creates a stat card showing:
        - Total Volume: sum of (weight * reps) across sets, displayed in pounds.
        - Est. 1RM: estimated one-repetition maximum computed as max weight * (1 + max reps / 30), displayed in pounds.
        - Total Sets: count of logged sets for that exercise.
        
        This method has no return value; it updates the UI inside self.analytics_frame.
        """
        for widget in self.analytics_frame.winfo_children():
            widget.destroy()
            
        if not self.workouts:
            self.no_data_label = tk.Label(self.analytics_frame, 
                                         text="No data yet.\nLog some workouts to see your analytics!",
                                         font=("Arial", 12), bg="#f0f4ff", fg="#6b7280")
            self.no_data_label.pack(pady=50)
            return
            
        # Group by exercise
        exercise_groups = {}
        for workout in self.workouts:
            exercise = workout['exercise']
            if exercise not in exercise_groups:
                exercise_groups[exercise] = []
            exercise_groups[exercise].append(workout)
            
        # Calculate stats
        for exercise, sets in exercise_groups.items():
            total_volume = sum(s['volume'] for s in sets)
            max_weight = max(s['weight'] for s in sets)
            max_reps = max(s['reps'] for s in sets if s['weight'] == max_weight)
            estimated_1rm = max_weight * (1 + max_reps / 30)
            total_sets = len(sets)
            
            # Create stat card
            card = tk.Frame(self.analytics_frame, bg="#e0e7ff", relief=tk.RAISED, borderwidth=2)
            card.pack(fill=tk.X, padx=20, pady=10)
            
            tk.Label(card, text=exercise, font=("Arial", 14, "bold"),
                    bg="#e0e7ff").pack(pady=10)
            
            stats_frame = tk.Frame(card, bg="#e0e7ff")
            stats_frame.pack(fill=tk.X, padx=20, pady=10)
            
            # Total Volume
            vol_frame = tk.Frame(stats_frame, bg="#e0e7ff")
            vol_frame.pack(side=tk.LEFT, expand=True)
            tk.Label(vol_frame, text="Total Volume", font=("Arial", 9),
                    bg="#e0e7ff", fg="#6b7280").pack()
            tk.Label(vol_frame, text=f"{total_volume:.0f} lbs", 
                    font=("Arial", 16, "bold"), bg="#e0e7ff", fg="#4f46e5").pack()
            
            # Est 1RM
            rm_frame = tk.Frame(stats_frame, bg="#e0e7ff")
            rm_frame.pack(side=tk.LEFT, expand=True)
            tk.Label(rm_frame, text="Est. 1RM", font=("Arial", 9),
                    bg="#e0e7ff", fg="#6b7280").pack()
            tk.Label(rm_frame, text=f"{estimated_1rm:.1f} lbs",
                    font=("Arial", 16, "bold"), bg="#e0e7ff", fg="#10b981").pack()
            
            # Total Sets
            sets_frame = tk.Frame(stats_frame, bg="#e0e7ff")
            sets_frame.pack(side=tk.LEFT, expand=True)
            tk.Label(sets_frame, text="Total Sets", font=("Arial", 9),
                    bg="#e0e7ff", fg="#6b7280").pack()
            tk.Label(sets_frame, text=str(total_sets),
                    font=("Arial", 16, "bold"), bg="#e0e7ff", fg="#a855f7").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutTrackerApp(root)
    root.mainloop()
