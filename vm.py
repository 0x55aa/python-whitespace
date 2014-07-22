# coding: utf-8
import sys

from constants import *
from util import print_msg
from error import (
    StackEmptyError,
    HeapIndexError,
    StackIndexError,
    NoExistLabelError,
)


class Stack(object):
    def __init__(self):
        self.l = []

    def push(self, val):
        self.l.append(val)

    def count(self):
        return len(self.l)

    def is_empty(self):
        if self.count() == 0:
            return True
        return False

    def pop(self):
        if self.is_empty():
            raise StackEmptyError
        return self.l.pop()

    def copy(self, index):
        try:
            i = self.count()-index-1
            if i < 0:
                raise StackIndexError
            self.l.append(self.l[i])
        except:
            import traceback
            traceback.print_exc()
            raise StackIndexError

    def remove(self, index):
        try:
            i = self.count()-index-1
            if i < 0:
                raise StackIndexError
            del self.l[i]
        except:
            import traceback
            traceback.print_exc()
            raise StackIndexError

    def swap(self):
        try:
            self.l[-2], self.l[-1] = self.l[-1], self.l[-2]
        except:
            import traceback
            traceback.print_exc()
            raise StackIndexError

    def get_two(self):
        try:
            return self.l.pop(), self.l.pop()
        except:
            import traceback
            traceback.print_exc()
            raise StackIndexError


class Heap(object):
    def __init__(self):
        self.l = []

    def insert(self, index, val):
        if index < 0:
            print_msg("wocao", abort=True)
        if index >= self.count():
            for i in range(self.count(), index+1):
                self.l.append(0)
        self.l[index] = val

    def count(self):
        return len(self.l)

    def get(self, index):
        try:
            value = self.l[index]
        except:
            import traceback
            traceback.print_exc()
            raise HeapIndexError
        return value


class VM(object):
    def __init__(self, instruction):
        self.program = instruction
        self.val_stack = Stack()
        self.call_stack = Stack()
        self.heap = Heap()
        # program index
        self.col = 0

    def jump(self, val):
        try:
            self.col = self.program.index((LABEL, val))
        except:
            raise NoExistLabelError(val)

    def exe(self, i):
        if isinstance(i, tuple):
            (instruction, val) = i
            if instruction == PUSH:
                self.val_stack.push(val)
            elif instruction == REF:
                self.val_stack.copy(val)
            elif instruction == SLIDE:
                self.val_stack.remove(val)
            elif instruction == LABEL:
                pass
            elif instruction == CALL:
                self.call_stack.push(self.col)
                self.jump(val)
            elif instruction == JUMP:
                self.jump(val)
            elif instruction == IF_ZERO:
                if self.val_stack.pop() == 0:
                    self.jump(val)
            elif instruction == IF_NEGATIVE:
                if self.val_stack.pop() < 0:
                    self.jump(val)
        else:
            if i == END:
                print_msg("\nThe End!\n")
                return 'end'
            elif i == DUP:
                self.val_stack.copy(0)
            elif i == SWAP:
                self.val_stack.swap()
            elif i == DISCARD:
                self.val_stack.remove(0)
            elif i == PLUS:
                a, b = self.val_stack.get_two()
                self.val_stack.push(b+a)
            elif i == MINUS:
                a, b = self.val_stack.get_two()
                self.val_stack.push(b-a)
            elif i == TIMES:
                a, b = self.val_stack.get_two()
                self.val_stack.push(b*a)
            elif i == DIVIDE:
                a, b = self.val_stack.get_two()
                self.val_stack.push(b/a)
            elif i == MODULO:
                a, b = self.val_stack.get_two()
                self.val_stack.push(b % a)
            elif i == STORE:
                val, index = self.val_stack.get_two()
                self.heap.insert(index, val)
            elif i == RETRIEVE:
                index = self.val_stack.pop()
                val = self.heap.get(index)
                self.val_stack.push(val)
            elif i == RETURN:
                self.col = self.call_stack.pop()
            elif i == OUTPUT_CHAR:
                val = self.val_stack.pop()
                print_msg('%c' % val)
            elif i == OUTPUT_NUM:
                val = self.val_stack.pop()
                print_msg(val)
            elif i == READ_CHAR:
                index = self.val_stack.pop()
                # val = raw_input()
                val = sys.stdin.read(1)
                try:
                    val = ord(val[0])
                except:
                    print_msg("value error\n", abort=True)
                self.heap.insert(index, val)
            elif i == READ_NUM:
                index = self.val_stack.pop()
                val = raw_input()
                try:
                    val = int(val)
                except:
                    print_msg("value error\n", abort=True)
                self.heap.insert(index, val)

    def run(self):
        while 1:
            i = self.program[self.col]
            self.col += 1
            try:
                r = self.exe(i)
                if r == 'end':
                    break
            except Exception, e:
                print_msg(e, abort=True)
