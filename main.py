import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import services
import visualize

current_loop = None

# ~ def button_a_loop():
	# ~ global current_loop
	# ~ if current_loop == "A":
		# ~ services.button_a()
		
csv_file = "database.csv"

try:
    actions_df = pd.read_csv(csv_file)
    visualize.main()
except FileNotFoundError:
    actions_df = pd.DataFrame(columns=["ID", "Date", "Action"])
    actions_df.to_csv(csv_file, index=False)

def insert_action(action):
    global actions_df
    date = datetime.now().strftime("%Y-%m-%d")
    new_data = pd.DataFrame([[int(len(actions_df) + 1), date, action]], columns=["ID", "Date", "Action"])
    actions_df = pd.concat([actions_df, new_data], ignore_index=True)  # Append new data
    actions_df.to_csv(csv_file, index=False)
    visualize.main()

def button_b():
	global current_loop
	current_loop = None
	label_result.config(text="Now, you choose B")
	root.update()
	insert_action("B")
	services.text2speech("This is an engine assembly simulation. If the products are in the standard section.")
	services.button_b()

def button_mic_loop():
	global current_loop
	if current_loop == "Mic":
		services.button_mic()

def button_a():
	global current_loop
	current_loop = None
	label_result.config(text="Now, you choose A")
	root.update()
	insert_action("A")
	services.text2speech("This is a show of sorting products from labels. If the products are in the standard section, they will be transported to the next process.")
	services.button_a()

def button_mic():
	global current_loop
	current_loop = "Mic"
	label_result.config(text="Speak A or B for system show")
	root.update()
	root.after(100, button_mic_loop)		
	services.text2speech("Please speak A or B, After this voice message ends")
	button_mic_loop()

root = tk.Tk()
root.title("Enhanced System")
root.geometry("400x350")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(expand=True)

button_a = tk.Button(frame, text="A", font=("Helvetica", 14), width=10, bg="#4CAF50", fg="white", command=button_a)
button_a.grid(row=0, column=0, padx=20, pady=10)

button_b = tk.Button(frame, text="B", font=("Helvetica", 14), width=10, bg="#2196F3", fg="white", command=button_b)
button_b.grid(row=1, column=0, padx=20, pady=10)

button_mic = tk.Button(frame, text="Mic", font=("Helvetica", 14), width=10, bg="#FF5722", fg="white", command=button_mic)
button_mic.grid(row=2, column=0, padx=20, pady=10)

label_result = tk.Label(root, text="Please choose a button!", font=("Helvetica", 12), bg="#f0f0f0", fg="#333")
label_result.pack(pady=20)

root.mainloop()
