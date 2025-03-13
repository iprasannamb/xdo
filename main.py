from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header, Input, Static, DataTable
from textual import on
import json
import os
from datetime import datetime

class xDo(App):
    """A simple task manager application built with Textual."""
    
    TITLE = "xDo - A simple task manager"
    
    CSS = """
    #task-list {
        height: 1fr;
        margin: 1 1;
    }
    
    #controls {
        height: auto;
        margin: 1 1;
        background: #333333;
        padding: 1;
    }
    
    #search-container {
        height: auto;
        margin: 1 1;
        background: #333333;
        padding: 1;
    }
    
    Button {
        margin-right: 1;
    }
    
    .completed {
        text-style: strike;
        color: #777777;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("a", "add_task", "Add Task"),
        ("d", "delete_task", "Delete Task"),
        ("c", "toggle_complete", "Toggle Complete"),
        ("s", "focus_search", "Search"),
    ]
    
    def __init__(self):
        super().__init__()
        self.data_file = "tasks.json"
        self.tasks = self.load_tasks()
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container(id="search-container"):
            yield Static("Search Tasks:")
            yield Input(placeholder="Search by task title", id="search-input")
            yield Button("Clear Search", id="clear-search-button")
            
        yield DataTable(id="task-list")
        
        with Container(id="controls"):
            # yield Static("New Task:")
            yield Input(placeholder="Task", id="new-task")
            yield Button("Add", id="add-button", variant="primary")
            yield Button("Mark Complete/Incomplete", id="toggle-button")
            yield Button("Remove", id="delete-button", variant="error")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the task table when the app starts."""
        table = self.query_one(DataTable)
        table.add_columns("Status", "Task", "Created")
        self.update_task_list()
    
    def update_task_list(self) -> None:
        """Update the task list display."""
        table = self.query_one(DataTable)
        table.clear(columns=False)
        
        search_text = self.query_one("#search-input").value.lower()
        
        for task in self.tasks:
            # Skip tasks that don't match the search query
            if search_text and search_text not in task["title"].lower():
                continue
                
            status = "✓" if task["completed"] else "○"
            status_cell = (status, "completed" if task["completed"] else "")
            task_cell = (task["title"], "completed" if task["completed"] else "")
            date_cell = (task["created_at"], "")
            
            table.add_row(status_cell, task_cell, date_cell)
    
    def action_add_task(self) -> None:
        """Add a new task."""
        input_field = self.query_one("#new-task")
        task_title = input_field.value.strip()
        
        if task_title:
            new_task = {
                "title": task_title,
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.tasks.append(new_task)
            self.save_tasks()
            self.update_task_list()
            input_field.value = ""
    
    def action_delete_task(self) -> None:
        """Delete the selected task."""
        table = self.query_one(DataTable)
        if table.cursor_row is not None:
            if 0 <= table.cursor_row < len(self.tasks):
                self.tasks.pop(table.cursor_row)
                self.save_tasks()
                self.update_task_list()
    
    def action_toggle_complete(self) -> None:
        """Toggle the completion status of the selected task."""
        table = self.query_one(DataTable)
        if table.cursor_row is not None:
            if 0 <= table.cursor_row < len(self.tasks):
                self.tasks[table.cursor_row]["completed"] = not self.tasks[table.cursor_row]["completed"]
                self.save_tasks()
                self.update_task_list()
    
    @on(Button.Pressed, "#add-button")
    def handle_add_button(self) -> None:
        self.action_add_task()
    
    @on(Button.Pressed, "#delete-button")
    def handle_delete_button(self) -> None:
        self.action_delete_task()
    
    @on(Button.Pressed, "#toggle-button")
    def handle_toggle_button(self) -> None:
        self.action_toggle_complete()
    
    @on(Input.Submitted, "#search-input")
    def handle_search_submitted(self) -> None:
        """Update the task list when search is submitted."""
        self.update_task_list()
    
    @on(Input.Changed, "#search-input")
    def handle_search_changed(self) -> None:
        """Update the task list as the user types in the search field."""
        self.update_task_list()
    
    @on(Button.Pressed, "#clear-search-button")
    def handle_clear_search(self) -> None:
        """Clear the search field and show all tasks."""
        self.query_one("#search-input").value = ""
        self.update_task_list()
    
    def action_focus_search(self) -> None:
        """Focus the search input field."""
        self.query_one("#search-input").focus()
    
    @on(Input.Submitted)
    def handle_input_submitted(self) -> None:
        self.action_add_task()
    
    def load_tasks(self) -> list:
        """Load tasks from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def save_tasks(self) -> None:
        """Save tasks to the JSON file."""
        with open(self.data_file, "w") as f:
            json.dump(self.tasks, f, indent=2)


if __name__ == "__main__":
    app = xDo()
    app.run() 
