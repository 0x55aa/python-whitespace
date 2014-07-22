# coding: utf-8
import sys


def print_msg(msg, abort=False):
    msg = "%s" % msg
    if abort:
        sys.stderr.write(msg)
        sys.exit(1)
    else:
        sys.stdout.write(msg)
