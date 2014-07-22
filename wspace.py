#!/usr/bin/env python
# coding: utf-8
import sys

from util import print_msg
from parser import tokenizer, Parser
from vm import VM


def usage():
    print_msg("python-wspace 0.1 (c) 2014\n")
    print_msg("-------------------------------\n")
    print_msg("Usage: wspace.py [file]\n")


def execute(filename):
    try:
        f = open(filename)
    except:
        print_msg("open file error\n", abort=True)
    text = f.read()
    f.close()
    token = tokenizer(text)
    parser = Parser(token)
    instruction = parser.parse()
    #print repr(text)
    #print instruction

    vm = VM(instruction)
    vm.run()

    return text


def main():
    if len(sys.argv) == 2:
        execute(sys.argv[1])
    else:
        usage()


if __name__ == '__main__':
    main()
