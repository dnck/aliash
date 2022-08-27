# -*- coding: utf-8 -*-
"""aliash_tool Description

This is the command line interface for aliash_tool. The structure of this program
follows the structure of Click command line interface. You can read more about
Click here, https://click.palletsprojects.com/en/7.x/
"""
import os

from pathlib import Path

import click

from aliash_tool import aliash_tool


defaults = {}
defaults["ALIASH_SCRIPTS_DIR"] = os.environ.get(
        "ALIASH_SCRIPTS_DIR",
        os.path.join(str(Path.home()), "Utilities")
)
defaults["ALIASH_SCRIPTS_FILE"] = os.environ.get(
        "ALIASH_SCRIPTS_FILE",
        os.path.join(str(Path.home()), ".bash_aliases")
)


class CommandLineApp:  # pylint: disable=too-few-public-methods
    """CommandLineApp is the default command line client for aliash_tool.

    It uses the Click module instead of argparse.
    """

    def __init__(self, script_dir: str, bash_aliases_file:str):
        self.cli = aliash_tool.AliashTool(
            script_dir=script_dir,  # script directory default ~/Utilities
            bash_aliases_file=bash_aliases_file,  # default ~/.bash_aliases
        )


@click.group()
@click.option(
    "--script-dir", default=defaults["ALIASH_SCRIPTS_DIR"],
    type=click.Path(exists=True)
)
@click.option(
    "--bash-aliases-file",
    default=defaults["ALIASH_SCRIPTS_FILE"],
    type=click.Path(exists=True),
)
@click.pass_context
def cli(ctx, script_dir, bash_aliases_file):
    """
    aliash_tool manages your .bash_aliases!
    """
    ctx.obj = CommandLineApp(script_dir, bash_aliases_file)


@cli.command()
@click.pass_context
def test(ctx):
    """
    Test all methods of aliash_tool
    """
    assert ctx.obj.cli.test_aliash_tool()


@cli.command()
@click.argument("alias")
@click.pass_context
def add(ctx, alias):
    """
    Create a new [ALIAS] and put its alias in .bash_aliases
    """
    assert ctx.obj.cli.add_alias(alias)


@cli.command()
@click.pass_context
@click.argument("alias")
def remove(ctx, alias):
    """
    Remove an [ALIAS] from .bash_aliases
    """
    assert ctx.obj.cli.remove_alias(alias)


@cli.command()
@click.pass_context
@click.argument("alias")
def edit(ctx, alias):
    """
    Edit an [ALIAS] in the script_dir (requires nano)
    """
    assert ctx.obj.cli.edit_alias(alias)


@cli.command()
@click.pass_context
@click.argument("alias")
@click.argument("new_name")
def rename(ctx, alias, new_name):
    """Rename an [ALIAS] in .bash_aliases"""
    assert ctx.obj.cli.rename_alias(alias, new_name)


@cli.command()
@click.pass_context
@click.argument("tag")
def find(ctx, tag: str):
    """
    Find an alias in .bash_aliases using a [TAG]
    """
    found_aliases = ctx.obj.cli.find_alias(tag)
    if len(found_aliases):
        for k, v in found_aliases.items():  # pylint: disable=invalid-name
            print(k, v)
    else:
        print("no aliases found")


@cli.command()
@click.pass_context
@click.argument("alias")
def help(ctx, alias: str):  # pylint: disable=redefined-builtin
    """
    Display help for an [ALIAS] in .bash_aliases
    """
    assert ctx.obj.cli.help_alias(alias)


@cli.command()
@click.pass_context
def show_all(ctx):
    """
    Basically just ls on the script_dir
    """
    ctx.obj.cli.show_all_aliases()



if __name__ == "__main__":
    # disable because cli gets input from user
    cli()  # pylint: disable=no-value-for-parameter
