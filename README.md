# xDo - a Simple Task Manager

xDo is a lightweight, terminal-based task manager built with Python and the Textual TUI framework.

## Features

- Create, complete, and delete tasks
- Persistent storage using JSON
- Clean, intuitive terminal interface
- Keyboard shortcuts for quick actions

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/iprasannamb/xdo.git
   cd xdo
   ```

2. Install dependencies:
   ```
   pip install textual
   ```

## Usage

Run the application: 

### Keyboard Shortcuts

- `a`: Add a new task
- `d`: Delete selected task
- `c`: Toggle task completion status
- `q`: Quit the application

### Mouse Controls

- Click "Add" button or press Enter to add a task
- Select a task and click "Mark Complete/Incomplete" to toggle status
- Select a task and click "Delete" to remove it

## Data Storage

Tasks are stored in a `tasks.json` file in the same directory as the application.

## Requirements

- Python 3.7+
- Textual library
