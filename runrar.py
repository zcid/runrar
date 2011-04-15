#!/usr/bin/python3
"""
Runrar v0.1 created 14 Apr, 2011
"""

from sys import argv
import argparse
import os
import fnmatch
import subprocess

def runrar():
    parser = make_parser()

    # args is a tuple of arguments in the order expected by unrar
    args = run_parser(parser)
    print("\nblah\n",args)

    unrar(*args)

    return


def make_parser():
    """
    Creates a parser that handles -t and -s options.
    """
    print("initializing command line parser")
    
    parser = argparse.ArgumentParser(description = "runrar - a recursive unrar \
                wrapper")

    parser.add_argument('-t', nargs='?', default=os.getcwd(),
        metavar="target directory")
    
    parser.add_argument('-s', nargs='?', default=None,
        metavar="save directory")

    return parser


def run_parser(parser):
    """
    Parses the command line arguments and passes them back in a order
    consistent with what unrar() expects.
    """
    print("parsing command line")

    parsed_args = parser.parse_args(argv[1:])
    print("args=", parsed_args.t, parsed_args.s)
    
    return (parsed_args.t, parsed_args.s)


def unrar(target_dir=os.getcwd(), save_dir=None):
    """
    The core functionality is handled by this function.
    """
    files = os.listdir(target_dir)

    # spawn a new instance of unrar() for each directory
    for file in files:
        if os.path.isdir(os.path.join(target_dir, file)):
            unrar(os.path.join(target_dir, file), save_dir)

    print("\n*******************************************",
            "\nunraring files\nfrom: ", target_dir, "\nto: ", save_dir,
            "\n*******************************************\n")
    
    # unrar archives in current directory
    for file in fnmatch.filter(files, "*.rar"):
        print("unraring: ", file)
        abs_file = os.path.join(target_dir, file)

        call = ['/usr/bin/unrar', 'x', abs_file]
        if save_dir:
            call.append(save_dir)
        else:
            call.append(target_dir)

        subprocess.call(call)


if __name__ == "__main__":
    runrar()
