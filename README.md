# aliash

`aliash` is a Python tool designed to manage and manipulate your .bash_aliases file, as well as handle the bash scripts referenced within it. This tool simplifies the process of managing bash scripts and their corresponding aliases, providing a straightforward interface for creating, editing, and organizing scripts.

## Key Features

- **Script Management**: Easily add, edit, rename, and remove scripts with automatic alias management.
- **Alias Management**: Keeps your .bash_aliases file organized by linking each script to an alias.
- **Configurable Paths**: Customize script and alias file locations through command-line options or environment variables.

By default, `aliash` assumes:

- **Script Directory**: `$HOME/Utilities` or as specified by the `ALIASH_SCRIPTS_DIR` environment variable.
- **Alias File**: `$HOME/.bash_aliases` or as specified by the `ALIASH_SCRIPTS_FILE` environment variable.

You can override these paths at runtime with the `--script-dir` and `--bash-aliases-file` arguments.


## Usage

```
Usage: aliash [OPTIONS] COMMAND [ARGS]...

  Manage your .bash_aliases with simplicity and ease!

Options:
  --script-dir PATH
  --bash-aliases-file PATH
  --help                    Show this message and exit.

Commands:
  add       Create a new [ALIAS] and put its alias in .bash_aliases
  edit      Edit an [ALIAS] in the script_dir (requires nano)
  find      Find an alias in .bash_aliases using a [TAG]
  help      Display help for an [ALIAS] in .bash_aliases
  remove    Remove an [ALIAS] from .bash_aliases
  rename    Rename an [ALIAS] in .bash_aliases
  show-all  Basically just ls on the script_dir
  test      Test all methods of aliash
```

## Examples

**Adding a Script Alias**

```bash
aliash add helloworld
aliash edit helloworld  # Opens the script in nano for editing
aliash show-all         # Lists all available scripts
source ~/.bashrc        # Reloads the updated bash configuration
helloworld              # Runs the new script
```

**Renaming an Alias**

```bash
aliash rename helloworld goodbyeworld
aliash show-all
source ~/.bashrc
goodbyeworld  # Runs the renamed script
```

**Removing an Alias**

```bash
aliash remove goodbyeworld
aliash find world  # Verifies if any alias containing 'world' exists
```

**Environment Variables**

You can configure `aliash` through the following environment variables:

- `ALIASH_SCRIPTS_DIR`: Directory to store and manage your bash scripts.
- `ALIASH_SCRIPTS_FILE`: Path to the .bash_aliases file.


## Installation

**1. Set up a virtual environment and install the project dependencies:**

```bash
python -m . .aliash
source bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
aliash --help
```

**2. Set up environment variables and alias:**

After installing the project, add the following to your login profile (e.g., `.bashrc` or `.bash_profile`) to ensure `aliash` is available in all terminal sessions:

```bash
# Define the directory where your bash scripts will be stored
ALIASH_SCRIPTS_DIR="$HOME/Utilities"

# Define the path to your .bash_aliases file
ALIASH_SCRIPTS_FILE="$HOME/.bash_aliases"

# Set the path to your aliash virtual environment
PATH_TO_ALIASH_VENV="$HOME/aliash/.aliash/"

# Create a shortcut for running aliash
alias aliash='$PATH_TO_ALIASH_VENV/bin/aliash'
```

**3. Reload you shell profile**
```bash
source ~/.bashrc  # or source ~/.bash_profile
```

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests. Feel free to open issues for feature requests or bug reports.

## License

This project is licensed under the MIT License.

## Common Issues

**Alias file does not exist!**

```
user@pc:~$ aliash add helpme
Usage: aliash [OPTIONS] COMMAND [ARGS]...
Try 'aliash --help' for help.

Error: Invalid value for '--bash-aliases-file': Path '/home/user/.bash_aliases' does not exist.
```

**Solution:**
```bash
touch .bash_aliases
```
