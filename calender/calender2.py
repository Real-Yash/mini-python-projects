import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkcalendar import Calendar
from datetime import datetime
import json
import os

# Dictionary to store events (date as key, list of events as value)
events = {}

# Load events from a JSON file if available
def load_events():
    global events
    try:
        with open('events.json', 'r') as file:
            events = json.load(file)
        for date in events:
            cal.calevent_create(datetime.strptime(date, '%Y-%m-%d'), 'Event', 'highlight')
        cal.tag_config('highlight', background='lightblue', foreground='black')
    except FileNotFoundError:
        pass

# Save events to a JSON file
def save_events():
    with open('events.json', 'w') as file:
        json.dump(events, file)

# Function to handle adding events and highlighting the date
def add_event():
    selected_date = cal.get_date()  # Get selected date from calendar
    event_description = simpledialog.askstring("Input", "Enter the event description:")
    
    if event_description:
        if selected_date in events:
            events[selected_date].append(event_description)
        else:
            events[selected_date] = [event_description]
        
        # Highlight the date with events
        cal.calevent_create(datetime.strptime(selected_date, '%Y-%m-%d'), 'Event', 'highlight')  # Tag the date
        cal.tag_config('highlight', background='lightblue', foreground='black')  # Define the tag's appearance
        save_events()
        messagebox.showinfo("Success", f"Event '{event_description}' added on {selected_date}.")
        show_events()  # Update the event list in the display

# Function to handle deleting events and updating the highlight
def delete_event():
    selected_date = cal.get_date()  # Get selected date from calendar
    if selected_date in events:
        event_description = simpledialog.askstring("Input", "Enter the event description to delete:")
        if event_description in events[selected_date]:
            events[selected_date].remove(event_description)
            if not events[selected_date]:  # Remove the date key and clear highlight if no events are left
                del events[selected_date]
                cal.calevent_remove('highlight', datetime.strptime(selected_date, '%Y-%m-%d'))
            save_events()
            messagebox.showinfo("Success", f"Event '{event_description}' deleted from {selected_date}.")
        else:
            messagebox.showwarning("Not Found", "Event not found.")
    else:
        messagebox.showwarning("Not Found", "No events found on this date.")
    
    show_events()  # Update the event list in the display

# Function to edit an event
def edit_event():
    selected_date = cal.get_date()  # Get selected date from calendar
    if selected_date in events:
        event_description = simpledialog.askstring("Input", "Enter the event description to edit:")
        if event_description in events[selected_date]:
            new_description = simpledialog.askstring("Input", "Enter the new description:")
            index = events[selected_date].index(event_description)
            events[selected_date][index] = new_description
            save_events()
            messagebox.showinfo("Success", f"Event '{event_description}' edited to '{new_description}' on {selected_date}.")
            show_events()  # Update the event list in the display
        else:
            messagebox.showwarning("Not Found", "Event not found.")
    else:
        messagebox.showwarning("Not Found", "No events found on this date.")

# Function to clear all events
def clear_all_events():
    global events
    response = messagebox.askyesno("Clear All", "Are you sure you want to clear all events?")
    if response:
        events = {}
        cal.calevent_remove('highlight')  # Remove all highlights
        save_events()
        messagebox.showinfo("Success", "All events have been cleared.")
        show_events()

# Function to show events for the selected date
def show_events():
    selected_date = cal.get_date()  # Get selected date from calendar
    if selected_date in events:
        event_list = "\n".join(events[selected_date])
        event_display.config(state=tk.NORMAL)  # Make the text box editable to update text
        event_display.delete(1.0, tk.END)  # Clear existing text
        event_display.insert(tk.END, f"Events on {selected_date}:\n{event_list}")
        event_display.config(state=tk.DISABLED)  # Set the text box back to read-only
    else:
        event_display.config(state=tk.NORMAL)
        event_display.delete(1.0, tk.END)
        event_display.insert(tk.END, f"No events found on {selected_date}.")
        event_display.config(state=tk.DISABLED)

# Function to view all events in the month
def view_all_events():
    all_events = ""
    for date in sorted(events.keys()):
        event_list = "\n".join(events[date])
        all_events += f"{date}:\n{event_list}\n\n"
    
    event_display.config(state=tk.NORMAL)
    event_display.delete(1.0, tk.END)
    event_display.insert(tk.END, "All Events:\n\n" + all_events)
    event_display.config(state=tk.DISABLED)

# Create the main application window
root = tk.Tk()
root.title("Calendar System")
root.geometry("500x500")

# Add the calendar widget
cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
cal.pack(pady=10)

# Add buttons for each functionality
add_button = tk.Button(root, text="Add Event", command=add_event, width=20)
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Event", command=delete_event, width=20)
delete_button.pack(pady=5)

edit_button = tk.Button(root, text="Edit Event", command=edit_event, width=20)
edit_button.pack(pady=5)

view_button = tk.Button(root, text="View Events", command=show_events, width=20)
view_button.pack(pady=5)

view_all_button = tk.Button(root, text="View All Events", command=view_all_events, width=20)
view_all_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear All Events", command=clear_all_events, width=20)
clear_button.pack(pady=5)

# Add a text box to display the events for the selected date
event_display = tk.Text(root, height=10, width=40)
event_display.pack(pady=10)
event_display.config(state=tk.DISABLED)  # Make the text box read-only

# Load saved events on start
load_events()

# Start the Tkinter main loop
root.mainloop()
