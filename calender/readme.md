# Calendar System

This is a simple calendar system built using Python's Tkinter library and the `tkcalendar` module. The application allows users to add, delete, edit, and view events on specific dates. Events are stored in a JSON file to persist data between sessions.

## Features

- **Add Event**: Add an event to a selected date.
- **Delete Event**: Delete an event from a selected date.
- **Edit Event**: Edit an existing event on a selected date.
- **View Events**: View events for the selected date.
- **View All Events**: View all events for the month.
- **Clear All Events**: Clear all events from the calendar.

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- tkcalendar
- JSON (standard library)

## Installation

1. Install Python 3.x from the [official website](https://www.python.org/).
2. Install Tkinter (usually comes pre-installed with Python).
3. Install `tkcalendar` using pip:
    ```sh
    pip install tkcalendar
    ```

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/calendar-system.git
    cd calendar-system
    ```
2. Run the script:
    ```sh
    python calendar_system.py
    ```

## Code Explanation

### Importing Libraries

```python
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkcalendar import Calendar
from datetime import datetime
import json
import os
