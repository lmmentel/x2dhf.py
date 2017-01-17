
'Some useful methods for running `x2dhf` code'

import argparse
import os
import sys
import shutil
from subprocess import run


EXTS = ['.coul', '.dat', '.exch', '.orb']


def which(prog):
    '''
    Python equivalent of the unix which command, returns the absolute path of
    the "prog" if it is found on the system PATH.
    '''

    if sys.platform == "win32":
        prog += ".exe"
    for path in os.getenv('PATH').split(os.path.pathsep):
        fprog = os.path.join(path, prog)
        if os.path.exists(fprog) and os.access(fprog, os.X_OK):
            return fprog
    else:
        return None


def run_x2dhf(exe_path, inp_name, out_name, verbose=False):
    'Run the `x2dhf` program'

    inp = open(inp_name, 'r')
    out = open(out_name, 'w')

    if verbose:
        print('Running: ', inp_name)

    run([exe_path], stdin=inp, stdout=out, stderr=out)

    inp.close()
    out.close()


def copy(source, dest):
    'copy the files needed for restart calculation'

    for ext in EXTS:
        shutil.copy(source + ext, dest + ext)
        print('copied {0:<20s} to   {1:<20s}'.format(source + ext, dest + ext))


def clean():
    'Remove the temp files and files with 0 size'

    to_clean = ['stop_x2dhf']
    for fname in os.listdir(os.getcwd()):
        if os.path.isfile(fname):
            if (os.path.splitext(fname)[1] in EXTS) or\
                    (os.path.getsize(fname) == 0) or\
                    (fname in [to_clean]):
                os.remove(fname)
                print('Removed: {}'.format(fname))


def stop():
    'stop the xd2hf gracefully'

    fname = 'stop_x2dhf'
    with open(fname, 'w'):
        os.utime(fname, None)


def set_run_defaults(args):
    'Set the defaults for the run command'

    if args.output is None:
        args.output = os.path.splitext(args.input)[0] + '.out'


def set_copy_defaults(args):

    if getattr(args, 'source', None) is None:
        args.source = '2dhf_output'
    if getattr(args, 'dest', None) is None:
        args.dest = '2dhf_input'


def read_output(out_name):
    'Parse the total energy from output'

    with open(out_name, 'r') as fout:
        for line in fout:
            if ('orbital energy threshold reached' in line) or\
               ('orbital normalization threshold reached' in line):
                break
        for line in fout:
            if 'total energy:' in line:
                energy = float(line.split()[2])
                break
        else:
            energy = None

    return energy


def xhf(cliargs=None):

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    # create the parser for the "run" command
    p_run = subparsers.add_parser('run')
    p_run.add_argument('input', type=str, help='input file')
    p_run.add_argument('-o', '--output', type=str)
    p_run.add_argument('-v', '--verbose', action='store_true')
    p_run.add_argument('-x', '--executable', type=str)
    p_run.set_defaults(func=set_run_defaults)

    # create the parser for the "restart" command
    p_copy = subparsers.add_parser('copy')
    p_copy.add_argument('-s', '--source', type=str)
    p_copy.add_argument('-d', '--dest', type=str)
    p_copy.set_defaults(func=set_copy_defaults)

    p_clean = subparsers.add_parser('clean')
    p_stop = subparsers.add_parser('stop')
    p_parse = subparsers.add_parser('parse')
    p_parse.add_argument('filename', type=str)

    if cliargs is not None:
        args = parser.parse_args(cliargs)
    else:
        args = parser.parse_args()
    if getattr(args, 'func', None) is not None:
        args.func(args)

    if args.command == 'copy':
        copy(args.source, args.dest)
    elif args.command == 'clean':
        clean()
    elif args.command == 'stop':
        stop()
    elif args.command == 'parse':
        energy = read_output(args.filename)
        print('{0:20s} : {1:25.15f}'.format(args.filename, energy))
    elif args.command == 'run':
        executable = which('x2dhf')
        if executable is None:
            raise ValueError('cannot find "{}" executable'.format(executable))
        run_x2dhf(executable, args.input, args.output, args.verbose)
    else:
        raise ValueError('unknown command: {}'.format(args.command))
