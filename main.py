# -*- coding: utf-8 -*-
"""aliash_tool Description

This is the command line interface for aliash_tool. The structure of this program
follows the structure of Click command line interface. You can read more about
Click here, https://click.palletsprojects.com/en/7.x/
"""
import click
import os

from pathlib import Path

from aliash_tool import aliash_tool

DEFAULTS = {
    "HOME_DIR": str(Path.home()),
    "SCRIPT_DIR": os.path.join(str(Path.home()), "Utilities"),
    "BASH_ALIASES_FILE": os.path.join(str(Path.home()), ".bash_aliases")
}



class CommandLineApp():
    """CommandLineApp is the default command line client for aliash_tool.

    It uses the Click module instead of argparse.
    """
    def __init__(self, home_dir, script_dir, bash_aliases_file):
        self.cli = aliash_tool.AliashTool(
            home_dir=home_dir, # home directory default ~/
            script_dir=script_dir, # script directory default ~/Utilities
            bash_aliases_file=bash_aliases_file, # default ~/.bash_aliases
        )

@click.group()
@click.option("--home-dir", default=DEFAULTS["HOME_DIR"], type=click.Path(exists=True))
@click.option("--script-dir", default=DEFAULTS["SCRIPT_DIR"], type=click.Path(exists=True))
@click.option("--bash-aliases-file", default=DEFAULTS["BASH_ALIASES_FILE"], type=click.Path(exists=True))
@click.pass_context
def cli(ctx, home_dir, script_dir, bash_aliases_file):
    """
    aliash_tool manages your .bash_aliases!
    """
    ctx.obj = CommandLineApp(home_dir, script_dir, bash_aliases_file)


@cli.command()
@click.pass_context
def test(ctx):
    """
    Test all methods of aliash_tool
    """
    assert ctx.obj.cli.test_aliash_tool()

@cli.command()
@click.argument('alias')
@click.pass_context
def add(ctx, alias):
    """
    Create a new [ALIAS] and put its alias in .bash_aliases
    """
    assert ctx.obj.cli.add_alias(alias)

@cli.command()
@click.pass_context
@click.argument('alias')
def remove(ctx, alias):
    """
    Remove an [ALIAS] from .bash_aliases
    """
    assert ctx.obj.cli.remove_alias(alias)

@cli.command()
@click.pass_context
@click.argument('alias')
def edit(ctx, alias):
    """
    Edit an [ALIAS] in the script_dir (requires nano)
    """
    assert ctx.obj.cli.edit_alias(alias)

@cli.command()
@click.pass_context
@click.argument('alias')
@click.argument('new_name')
def rename(ctx, alias, new_name):
    """Rename an [ALIAS] in .bash_aliases"""
    assert ctx.obj.cli.rename_alias(alias, new_name)

@cli.command()
@click.pass_context
@click.argument('tag')
def find(ctx, tag):
    """
    Find an alias in .bash_aliases using a [TAG]
    """
    found_aliases = ctx.obj.cli.find_alias(tag)
    if len(found_aliases):
        for k,v in found_aliases.items():
            print(k, v)
    else:
        print("no aliases found")

@cli.command()
@click.pass_context
@click.argument('alias')
def help(ctx, alias):
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
    cli()
