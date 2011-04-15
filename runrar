#!/usr/bin/python3
"""
runrar - a recursive unrar wrapper
Copyright (C) 2011 Nicholas Holley

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
                            
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from sys import argv
import argparse
import os
import fnmatch
import subprocess
import zlib

def runrar():
    parser = make_parser()

    # args is a tuple of arguments in the order expected by unrar
    args = run_parser(parser)

    unrar(*args)

    return


def make_parser():
    """
    Creates a parser that handles -t and -s options.
    """
    print("\ninitializing command line parser")
    
    parser = argparse.ArgumentParser(description = "runrar - a recursive unrar \
                wrapper")

    parser.add_argument('-t', nargs='?', default=os.getcwd(),
        metavar="directory to begin traversal")
    
    parser.add_argument('-s', nargs='?', default=None,
        metavar="directory to save extracted files")

    parser.add_argument('-c', action='store_true', default=False)

    return parser


def run_parser(parser):
    """
    Parses the command line arguments and passes them back in a order
    consistent with what unrar() expects.
    """
    print("parsing command line")

    parsed_args = parser.parse_args(argv[1:])
    
    return (parsed_args.t, parsed_args.s, parsed_args.c)


def check_sfv(directory):
    """
    Processes all sfv files in a directory.
    """
    sfv_list = fnmatch.filter(os.listdir(directory), "*sfv")
    for file in sfv_list:
        sfv = open(os.path.join(directory, file), 'r')

        for line in sfv:
            data = line.split()

            if data[0][0] != ';':
                print(data[1], data[0])
                checkfile = os.path.join(directory, data[0])
                checksum = str(hex((zlib.crc32(open(checkfile, 'br').read()) \
                        & 0xffffffff)))[2:]

                if int(checksum, 16) == int(data[1], 16):
                    print(checksum, "OK")
                else:
                    print(checksum, "BAD")
                    print("ERROR: checksum fail: ", checkfile)
                    return False

        sfv.close()

    return True


def unrar(target_dir=os.getcwd(), save_dir=None, test_sfv=False, debug=False):
    """
    The core functionality is handled by this function.
    """
    files = os.listdir(target_dir)

    # spawn a new instance of unrar() for each directory
    for file in files:
        if os.path.isdir(os.path.join(target_dir, file)):
            unrar(os.path.join(target_dir, file), save_dir, test_sfv)

    print("\n*******************************************",
            "\nunraring files\nfrom: ", target_dir, "\nto: ", \
                    save_dir if save_dir else target_dir,
            "\n*******************************************\n")
    
    # fixme: needs return check for errors
    if test_sfv:
        check_sfv(target_dir)

    # unrar archives in current directory
    for file in fnmatch.filter(files, "*.rar"):
        print("unraring: ", file)
        abs_file = os.path.join(target_dir, file)

        call = ['/usr/bin/unrar', 'x', '-inul', '-y', abs_file]
        if save_dir:
            call.append(save_dir)
        else:
            call.append(target_dir)

        subprocess.call(call)


if __name__ == "__main__":
    runrar()
