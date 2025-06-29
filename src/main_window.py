import data_preparation as dp
import tkinter as tk
import stock_plot as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plot_canvas = None  # Global variable to hold the plot canvas

# Var to store chosen stock symbol
ticker = ""

# Create the main window
window = tk.Tk()
window.title("ML Stock Predictor")
window.geometry("1920x1080")  # Set the window size to 1920x1080

# Title
title = tk.Label(window, text="Welcome to ML Stock Predictor", font=("Arial", 16))
title.pack(pady=20)

# Instructions
instructions = tk.Label(window, text="Enter a stock symbol:", font=("Arial", 12))
instructions.pack(pady=10)

# Create an entry (text box)
entry = tk.Entry(window, width=30)
entry.pack(pady=5)

# Function to handle input (optional)
def on_submit():
    global ticker, plot_canvas
    ticker = entry.get()
    if plot_canvas:
        plot_canvas.get_tk_widget().destroy()  # Remove the old canvas if it exists
    fig = sp.plot_price_and_volume(ticker)  # Get the new figure
    plot_canvas = FigureCanvasTkAgg(fig, master=window)  # Create a new canvas
    plot_canvas.draw()  # Draw the figure on the canvas
    plot_canvas.get_tk_widget().pack(pady=20)  # Pack the canvas into the window
    entry.delete(0, tk.END)  # Clears the entry box after submit

# Create a submit button
submit_button = tk.Button(window, text="Search", command=on_submit)
submit_button.pack(pady=10)

window.mainloop()
window.destroy()  # Ensure the window is destroyed when the main loop ends