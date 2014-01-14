#!/usr/bin/env python

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/6/14'

import os
from argparse import ArgumentParser
from fireworks.core.firework import FireWork
from fireworks.user_objects.firetasks.fileio_tasks import FileWriteTask
from fireworks.user_objects.firetasks.script_task import ScriptTask
import yaml


def create_fw_single(args, fnames, yaml_fname):
    tasks = []
    if fnames:
        files = []
        for fname in fnames:
            with open(fname) as f:
                files.append(
                    {
                        "filename": os.path.basename(fname),
                        "contents": f.read()
                    }
                )
        tasks.append(FileWriteTask({"files_to_write": files}))
    if args.command is not None:
        tasks.append(ScriptTask({"script": [args.command]}))
    fw = FireWork(tasks, name=args.name)
    with open(yaml_fname, "w") as f:
        yaml.dump(fw.to_dict(), f, default_flow_style=False)


def create_fw(args):
    if not args.directory_mode:
        create_fw_single(args, args.files_or_dirs, args.output)
    else:
        output_fname = args.output.replace(".yaml", "{}.yaml")
        for i, d in enumerate(args.files_or_dirs):
            create_fw_single(
                args,
                [os.path.join(d, f) for f in os.listdir(d)],
                output_fname.format(i)
            )


if __name__ == '__main__':
    p = ArgumentParser(description="""This script is used to create simple
    fireworks workflows from input files and script commands.
    """)
    sp = p.add_subparsers(help='command', dest='command')

    create_parser = sp.add_parser("create",
        help='Create a new simple workflow. A simple workflow involves '
             'writing a set of input files and/or running a series of '
             'commands.')

    create_parser.add_argument(
        '-c', '--command', default=[], nargs="*",
        type=str, help="Add a ScriptTask at the end to run a series of "
                       "commands.")
    create_parser.add_argument(
        '-o', '--output', default="my_fw.yaml",
        type=str,
        help="Output file name to write to. Defaults to \"my_fw.yaml\".")
    create_parser.add_argument(
        '-d', '--directory_mode', action="store_true",
        help="If specified, files_or_dirs is treated as a series of "
             "input directories and multiple fireworks will be generated with "
             "each directory treated as a single job. A _# will be appended "
             "to the yaml file name.")
    create_parser.add_argument(
        '-n', '--name', default="MyFW",
        type=str, help="Add a name for your firework. Defaults to \"MyFW\".")
    create_parser.add_argument(
        '-f', '--files_or_dirs', default=[], nargs="*",
        type=str, help="Files that need to be added as input files. Supports "
                       "wild cards.")

    create_parser.set_defaults(func=create_fw)

    args = p.parse_args()
    args.func(args)