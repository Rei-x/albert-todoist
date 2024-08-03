# Albert Todoist Integration

A powerful [albert-launcher](https://github.com/albertlauncher/albert) extension that allows you to quickly add tasks to your Todoist account and view existing tasks.

## Features

- Quickly add tasks to your Todoist inbox
- View your most recent Todoist tasks

## Installation

To install the extension, type the following in your terminal:

```
git clone https://github.com/rei-x/albert-todoist ~/.local/share/albert/python/plugins/todoist
```

Next, activate the extension: open Albert's settings, go to `Python > Todoist Tasks`, and check the checkbox.

## Configuration

Before using the extension, you need to set up your Todoist API token:

1. Go to your [Todoist Integrations settings](https://todoist.com/prefs/integrations)
2. Copy your API token
3. In Albert, type: `todo config YOUR_API_TOKEN_HERE`

Alternatively, you can set the `TODOIST_API_TOKEN` environment variable.

## Usage

The trigger to activate the extension is `todo`.

### Adding a Task

1. Activate Albert
2. Type `todo` followed by your task description
3. Press Enter to add the task to your Todoist inbox

Example: `todo Buy groceries tomorrow #shopping p1`

## Note
- The extension uses the `todoist-api-python` library, which should be installed automatically when you install the plugin.

## Troubleshooting

If you encounter any issues:

1. Ensure your API token is correctly set
2. Check your internet connection
3. Look for any error notifications in Albert

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
