# -*- coding: utf-8 -*-
"""app Description

This module does great things.
"""
import os
import tempfile
import subprocess
import shutil
from collections import namedtuple
# Implementation constants

BASH_SCRIPT_HEADER = """#!/bin/bash
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#     FILE:{}
#     DESCRIPTION:{}
#     USAGE:{}
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
BASH_SCRIPT_BODY='''
COMMAND=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --help) COMMAND="help"; shift 1;;
  esac
done

function help_message() {
  echo "ALIASH_NAME ALIASH_DOES_WHAT"
  echo "USAGE:"
  echo "  ALIASH_NAME [FLAGS]"
  echo "FLAGS:"
  echo "    --help            show help message"
}

function main() {
  ALIASH_FUNCTION_BODY
}

if [ "$COMMAND" == "help" ]; then
  help_message
else
  main
fi
'''


BColors = namedtuple("fontcolor", "HEADER OKBLUE OKCYAN OKGREEN WARNING FAIL"+
    "ENDC BOLD UNDERLINE"
)
BColors.HEADER = "\033[95m"
BColors.OKBLUE = "\033[94m"
BColors.OKCYAN = "\033[96m"
BColors.OKGREEN = "\033[92m"
BColors.WARNING = "\033[93m"
BColors.FAIL = "\033[91m"
BColors.ENDC = "\033[0m"
BColors.BOLD = "\033[1m"
BColors.UNDERLINE = "\033[4m"

def read_file(filename):  # pylint: disable=missing-function-docstring
    with open(filename, "rb") as fname:
        contents = fname.read().decode("UTF-8")
    return contents

def create_bash_script(filename):  # pylint: disable=missing-function-docstring
    with open(filename, "wb") as fname:
        header = BASH_SCRIPT_HEADER.format(
            filename,
            "",#DESCRIPTION
            "",#USAGE
        )
        fname.write(f"{header}".encode("UTF-8"))
        fname.write(BASH_SCRIPT_BODY.encode("UTF-8"))
    os.chmod(filename, 0o755)

def col_print(lines, term_width=160, indent=0, pad=2):  # pylint: disable=missing-function-docstring
    lines.sort()
    n_lines = len(lines)
    if n_lines == 0:
        return
    col_width = max(len(line) for line in lines)
    n_cols = int((term_width + pad - indent)/(col_width + pad))
    n_cols = min(n_lines, max(1, n_cols))
    col_len = int(n_lines/n_cols) + (0 if n_lines % n_cols == 0 else 1)
    if (n_cols - 1) * col_len >= n_lines:
        n_cols -= 1
    cols = [lines[i*col_len : i*col_len + col_len] for i in range(n_cols)]
    rows = list(zip(*cols))
    rows_missed = zip(*[col[len(rows):] for col in cols[:-1]])
    rows.extend(rows_missed)
    for row in rows:
        print(BColors.OKGREEN + " "*indent + (" "*pad).join(line.ljust(col_width) for line in row))

# Classes, methods, functions, and variables
class AliashTool():
    """AliashTool is the default class for app.

    As a default, the __init__ method does not set up any class attributes.
    However, if it does, you should follow the PEP-8 conventions and document
    them as shown below.

    Args:
        msg (str): Human readable str describing the exception.
        code (:obj:`int`, optional): Error code.

    Attributes:
        msg (str): Human readable str describing the exception.
        code (int): Exception error code.

    """
    def __init__(self, script_dir, bash_aliases_file):
        self.script_dir = script_dir
        self.alias_definition_file = bash_aliases_file

    def join_script_dir(self, filename) -> str:  # pylint: disable=missing-function-docstring
        return os.path.join(self.script_dir, filename)

    def _get_current_scripts_in_script_dir(self) -> list:
        return [os.path.join(self.script_dir, i) for i in os.listdir(
            self.script_dir) if i.endswith(".sh")]

    def _get_current_alias_definitions_from_file(self) -> list:
        alias_defintions = [line.strip() for line in read_file(
            self.alias_definition_file).split("\n") if not line == ""
        ]
        return alias_defintions

    def _get_current_aliases_in_alias_definition_file(self) -> list:
        alias_definition_file_aliases = []
        alias_defs = self._get_current_alias_definitions_from_file()
        for alias_def in alias_defs:
            if "=" in alias_def:
                alias_def = alias_def.split("=")
                alias = alias_def[0].split("alias ")[1]
                alias_definition_file_aliases.append(alias)
        return alias_definition_file_aliases

    def _get_current_scripts_in_alias_definition_file(self) -> list:
        alias_definition_file_scripts = []
        alias_defs = self._get_current_alias_definitions_from_file()
        for alias_def in alias_defs:
            if "=" in alias_def:
                alias_def = alias_def.split("=")
                filename = alias_def[1]
                alias_definition_file_scripts.append(filename)
        return alias_definition_file_scripts

    def _get_db(self) -> dict:
        """Returns {'alias': 'alias_script_path'}"""
        db = {}  # pylint: disable=invalid-name
        alias_defs = self._get_current_alias_definitions_from_file()
        for alias_def in alias_defs:
            if "=" in alias_def:
                alias_filename = alias_def.split("=")
                alias = alias_filename[0][6:].split(" ")[0]
                filename = alias_filename[1]
                if db.get(alias) is None:
                    db[alias] = filename
                else:
                    print("ERROR: duplicate alias")
                    assert False
        return db

    def _format_alias_definition(self, alias) -> str:
        return "alias {}={}".format(  # pylint: disable=consider-using-f-string
            alias,
            self.join_script_dir(alias+".sh")
        )

    def remove_file(self, filename):  # pylint: disable=missing-function-docstring
        old_script_dir = os.path.join(self.script_dir, "tmp")
        new_filename = filename.replace(self.script_dir, old_script_dir)
        shutil.move(filename, new_filename)

    def _clean_script_dir(self):
        scripts_in_dir = self._get_current_scripts_in_script_dir()
        scripts_in_alias_file = \
            self._get_current_scripts_in_alias_definition_file()
        for script in scripts_in_dir:
            if not script in scripts_in_alias_file:
                # actually just renames it
                self.remove_file(script)

    def _remove_alias_definition(self, alias):
        """Delete an alias definition from .bash_aliases"""
        remove_alias = self._format_alias_definition(alias)
        alias_definitions = self._get_current_alias_definitions_from_file()
        alias_definitions.remove(remove_alias)
        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as tmp_file:
            new_file = tmp_file.name
            for line in alias_definitions:
                if not line == "":
                    tmp_file.write(line+"\n")
            tmp_file.close()
        shutil.move(
            self.alias_definition_file,
            self.alias_definition_file+".bak"
        )
        shutil.move(new_file, self.alias_definition_file)
        self._clean_script_dir()

    def _append_bash_alias_file(self, new_alias):
        """Append an alias definition from .bash_aliases"""

        new_alias_definition = self._format_alias_definition(new_alias)
        alias_definitions = self._get_current_alias_definitions_from_file()

        if not new_alias_definition in alias_definitions:
            alias_definitions.append(new_alias_definition)

        alias_definitions.sort()

        with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as tmp_file:
            new_file = tmp_file.name
            for line in alias_definitions:
                if not line == "":
                    tmp_file.write(line+"\n")
            tmp_file.close()

        shutil.move(self.alias_definition_file,
            self.alias_definition_file+".bak"
        )
        shutil.move(new_file, self.alias_definition_file)

    def _is_alias_in_script_dir(self, alias) -> bool:
        return os.path.isfile(self.join_script_dir(alias+".sh"))

    def _is_alias_in_alias_definition_file(self, alias) -> bool:
        current_aliases = self._get_current_aliases_in_alias_definition_file()
        if alias not in current_aliases:
            return False
        return True

    def add_alias(self, alias):
        """Create a new alias .sh file in the script_dir and add it to
        .bash_aliases file
        Returns:
            True
        """
        if self._is_alias_in_script_dir(alias):
            print("ERROR: alias already exists with that name")
            return False

        self._append_bash_alias_file(alias)
        new_filename = self.join_script_dir(alias+".sh")
        create_bash_script(new_filename)
        print("SUCCESS: added new alias file to script dir")
        return True

    def remove_alias(self, alias):
        """Remove an existing alias definition and its script file
        Returns:
            True
        """
        # only add the alias if it does not exist as alias and there's
        # not a filename already in the script dir
        db = self._get_db()  # pylint: disable=invalid-name
        old_alias_file = db.get(alias)
        if old_alias_file is None:
            print("ERROR: alias does not exist with that name")
            return False
        self._remove_alias_definition(alias)
        print("SUCCESS: removed old alias from .bash_aliases")
        return True

    def show_alias_header(self, alias):
        """Show the help str from an alias definition

        Returns:
            True

        """
        # only show help if the alias does exist
        db = self._get_db()  # pylint: disable=invalid-name
        if db.get(alias) is None:
            print(f"ERROR: alias key {alias} not in db")
            return False

        try:
            script = read_file(db.get(alias))
            header_div="#%"
            lines=[]
            for line in script.split("\n"):
                if line.startswith(header_div) and line not in lines:
                    lines.append(line)
                    continue
                if line in lines:
                    for help_line in lines:
                        print(help_line)
                    print(line)
                    break
                lines.append(line)
        except FileNotFoundError as _:
            print(f"ERROR: reading filename {db.get(alias)}")
            return False
        return True

    def help_alias(self, alias):
        """Show the help str from an alias definition

        Returns:
            True

        """
        # only show help if the alias does exist
        db = self._get_db()  # pylint: disable=invalid-name
        if db.get(alias) is None:
            print(f"ERROR: alias key {alias} not in db")
            return False
        try:
            script = read_file(db.get(alias))
            for line in script.split("\n"):
                print(line)
        except FileNotFoundError as _:
            print(f"ERROR: reading filename {db.get(alias)}")
            return False
        return True

    def find_alias(self, tag) -> dict:
        """Find alias with a tag
        Returns:
            True
        """
        db = self._get_db()  # pylint: disable=invalid-name
        found_aliases = {}
        for key, value in db.items():
            if tag in key:
                found_aliases.update({key: value})
        return found_aliases

    def edit_alias(self, alias):
        """Edit an alias

        Returns:
            True

        """
        if not self._is_alias_in_script_dir(alias):
            print("ERROR: alias script does not exist with that name")
            return False
        # only show edit if the alias does exist
        db = self._get_db()  # pylint: disable=invalid-name
        if db.get(alias) is None:
            print(f"ERROR: alias key {alias} not in db")
            return False
        try:
            filename = self.join_script_dir(alias+".sh")
            script = read_file(filename)
            with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as tmp_fname:
                tmp_filename = tmp_fname.name
                tmp_fname.write(script)
                tmp_fname.close()
            subprocess.call(['nano', tmp_filename])
            shutil.move(tmp_filename, filename)
            os.chmod(filename, 0o755)
        except FileNotFoundError as _:
            print("ERROR: writing filename {}".format(alias+".sh")) # pylint: disable=consider-using-f-string
            return False
        return True

    def rename_alias(self, old_name, new_name):
        """Rename an alias

        Returns:
            True

        """
        if self._is_alias_in_script_dir(new_name):
            print("ERROR: alias already exists with that name in script dir")
            return False
        if not self._is_alias_in_script_dir(old_name):
            print("ERROR: alias does not exist with that name in script dir")
            return False
        if not self._is_alias_in_alias_definition_file(old_name):
            print("ERROR: alias does not exist with that name in alias file")
            return False
        self.add_alias(new_name)
        shutil.copy(
            self.join_script_dir(old_name+".sh"),
            self.join_script_dir(new_name+".sh")
        )
        self.remove_alias(old_name)
        return True

    def show_all_aliases(self):
        """Shows all of the aliases script names"""
        return [i for i in os.listdir(self.script_dir) if i.endswith(".sh")]

    def test_aliash_tool(self):
        """Class methods are similar to regular functions.

        Returns:
            True

        """
        return True
