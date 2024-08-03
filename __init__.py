# -*- coding: utf-8 -*-

"""
Add todo tasks to Todoist and view existing tasks
"""

from albert import *
from todoist_api_python.api import TodoistAPI
import os
from pathlib import Path
import time

md_iid = '2.3'
md_version = "1.4"
md_name = "Todoist Tasks"
md_description = "Add tasks to Todoist and view existing tasks"
md_license = "MIT"
md_url = "https://github.com/Rei-x/albert-todoist"
md_authors = "@Rei-x"
md_lib_dependencies = "todoist-api-python"

class Plugin(PluginInstance, TriggerQueryHandler):

    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(
            self,
            id=self.id,
            name=self.name,
            description=self.description,
            synopsis="todo <task>",
            defaultTrigger='todo '
        )
        self.icon = str(Path(__file__).parent / "todoist.png")
        self._api_token = self.readConfig('api_token', str) or os.environ.get('TODOIST_API_TOKEN')
        self.api = None
        self.initialize_api()
        self.last_fetch_time = 0
        self.cached_tasks = []
        self.debounce_interval = 5  # 5 seconds debounce
        self.task_limit = 30  # Limit to 5 tasks

    def initialize_api(self):
        if self._api_token:
            try:
                self.api = TodoistAPI(self._api_token)
                # Test the API connection
                self.api.get_projects()
            except Exception as e:
                warning(f"Failed to initialize Todoist API: {str(e)}")
                self._api_token = None
                self.api = None

    def handleTriggerQuery(self, query):
        if query.string.strip().lower().startswith('config '):
            _, token = query.string.strip().split(maxsplit=1)
            self.set_api_token(token)
            query.add(StandardItem(
                id=f"{self.id}_config",
                text="Todoist API Token Updated",
                subtext="The API token has been set. Try adding a task now.",
                iconUrls=[self.icon]
            ))
            return

        if not self.api:
            query.add(StandardItem(
                id=f"{self.id}_error",
                text="Todoist API token not set",
                subtext="Use 'todo config <YOUR_API_TOKEN>' to set your Todoist API token",
                iconUrls=[self.icon]
            ))
            return

        task = query.string.strip()
        if task:
            query.add(StandardItem(
                id=f"{self.id}_add",
                text=f"Add task: {task}",
                subtext="Press Enter to add this task to Todoist",
                iconUrls=[self.icon],
                actions=[Action("add", "Add task", lambda t=task: self.add_task(t))]
            ))

            # Fetch and display existing tasks
            existing_tasks = self.get_existing_tasks()
            for existing_task in existing_tasks:
                query.add(StandardItem(
                    id=f"{self.id}_existing_{existing_task.id}",
                    text=existing_task.content,
                    subtext="Existing task",
                    iconUrls=[self.icon]
                ))

    def set_api_token(self, token):
        self._api_token = token
        self.writeConfig('api_token', token)
        self.initialize_api()
        if self.api:
            Notification(title="Todoist API Token", text="API token has been set successfully").send()
        else:
            Notification(title="Todoist API Token", text="Failed to set API token. Please check if it's correct.").send()

    def add_task(self, task):
        try:
            self.api.quick_add_task(task)
            self.last_fetch_time = 0  # Reset last fetch time to update cache on next query
            return Notification(title="Task added", text=f"Successfully added task: {task}").send()
        except Exception as e:
            return Notification(title="Error", text=f"Failed to add task: {str(e)}").send()

    def get_existing_tasks(self):
        current_time = time.time()
        if current_time - self.last_fetch_time > self.debounce_interval:
            try:
                self.cached_tasks = self.api.get_tasks(limit=self.task_limit)
                self.last_fetch_time = current_time
            except Exception as e:
                warning(f"Failed to fetch existing tasks: {str(e)}")
                self.cached_tasks = []
        return sorted(self.cached_tasks, key=lambda x: x.created_at, reverse=True)
