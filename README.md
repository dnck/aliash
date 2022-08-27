# aliash_tool

`aliash_tool` is a python tool for manipulating a `.bash_aliases` file and managing
the scripts referenced therein.

Scripts are stored in a runtime configurable argument `--script_dir`, or in the
path pointed to by the environment variable `ALIASH_SCRIPTS_DIR`, or by default
in `"$HOME"/Utilities`.

Alias definitions referencing these scripts are stored in a runtime configurable
argument `--bash-aliases-file`, or in the path pointed to by the environment variable `ALIASH_SCRIPTS_FILE`, or by default in a `"$HOME"/.bash_aliases` file.

**Usage**

```
Usage: aliash_tool [OPTIONS] COMMAND [ARGS]...

  aliash_tool manages your .bash_aliases!

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
  test      Test all methods of aliash_tool
```

**Example**

The following example shows how to add, edit, search, rename, and remove aliases

```bash
aliash_tool add helloworld
aliash_tool edit helloworld # edit the script in nano
aliash_tool show-all
source ~/.bashrc
helloworld
aliash_tool rename helloworld goodbyeworld
aliash_tool show-all
source ~/.bashrc
goodbyeworld
aliash_tool remove goodbyeworld
aliash_tool find world
```

**Install**

```bash
python -m . venv
source bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
aliash --help
```

After installing the project in a virtual environment, you can set the following
in your login profile (e.g. `.bashrc`) to have `aliash` at your disposal:

```bash
ALIASH_SCRIPTS_DIR="$HOME/Utilities"
ALIASH_SCRIPTS_FILE="$Home/.bash_aliases"
PATH_TO_ALIASH_VENV="$HOME/aliash_tool/.venv/"
alias aliash='$PATH_TO_ALIASH_VENV/bin/aliash_tool'
```
