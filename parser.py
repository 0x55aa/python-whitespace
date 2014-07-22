# coding: utf-8

from constants import *
from util import print_msg
from error import WsSyntaxError


def tokenizer(text):
    token = []
    for c in text:
        if c == SPACE:
            token.append(SPACE)
        elif c == TAB:
            token.append(TAB)
        elif c == LF:
            token.append(LF)
    return token


class Parser(object):
    def __init__(self, token):
        self.token = token
        self.iter_token = self.next_token()
        self.index = 0

    def get_line_col(self):
        parse_code = self.token[:self.index]
        count_LF = parse_code.count('\n')
        if self.token[self.index] == '\n':
            line = count_LF - 1
            col = self.index - parse_code[:-1].rindex('\n')
            return (line, col)
        else:
            line = count_LF - 1
            col = self.index - parse_code.rindex('\n')
            return (line, col)

    def next_token(self):
        for t in self.token:
            yield t
            self.index += 1

    def parse_num(self):
        """
        return int
        """
        num = ''
        while 1:
            t = self.iter_token.next()
            if t == LF:
                break
            elif t == SPACE:
                num += '0'
            else:
                num += '1'
        if num[0] == '1':
            num = '-' + num[1:]
        if len(num) < 2:
            raise WsSyntaxError(*self.get_line_col())
        return int(num, 2)

    def parse_str(self):
        str_ = ''
        while 1:
            t = self.iter_token.next()
            if t == LF:
                break
            elif t == SPACE:
                str_ += '0'
            else:
                str_ += '1'
        if not str_:
            raise WsSyntaxError(*self.get_line_col())
        return str_

    def stack_manipulation(self):
        t = self.iter_token.next()
        if t == SPACE:
            return (PUSH, self.parse_num())
        else:
            next_t = self.iter_token.next()
            if t == TAB:
                if next_t == SPACE:
                    return (REF, self.parse_num())
                elif next_t == LF:
                    return (SLIDE, self.parse_num())
                else:
                    raise WsSyntaxError(*self.get_line_col())
            elif t == LF:
                if next_t == SPACE:
                    return DUP
                elif next_t == TAB:
                    return SWAP
                else:
                    return DISCARD

    def arithmetic(self):
        t, next_t = self.iter_token.next(), self.iter_token.next()
        if t == SPACE:
            if next_t == SPACE:
                return PLUS
            elif next_t == TAB:
                return MINUS
            else:
                return TIMES
        elif t == TAB:
            if next_t == SPACE:
                return DIVIDE
            elif next_t == TAB:
                return MODULO
            else:
                raise WsSyntaxError(*self.get_line_col())
        else:
            raise WsSyntaxError(*self.get_line_col())

    def heap_access(self):
        t = self.iter_token.next()
        if t == SPACE:
            return STORE
        elif t == TAB:
            return RETRIEVE
        else:
            raise WsSyntaxError(*self.get_line_col())

    def flow_control(self):
        t, next_t = self.iter_token.next(), self.iter_token.next()
        if t == SPACE:
            if next_t == SPACE:
                return (LABEL, self.parse_str())
            elif next_t == TAB:
                return (CALL, self.parse_str())
            else:
                return (JUMP, self.parse_str())
        elif t == TAB:
            if next_t == SPACE:
                return (IF_ZERO, self.parse_str())
            elif next_t == TAB:
                return (IF_NEGATIVE, self.parse_str())
            else:
                return RETURN
        else:
            if next_t == LF:
                # end parse
                # raise
                return END
            else:
                # err
                raise WsSyntaxError(*self.get_line_col())

    def io(self):
        t, next_t = self.iter_token.next(), self.iter_token.next()
        if t == SPACE:
            if next_t == SPACE:
                return OUTPUT_CHAR
            elif next_t == TAB:
                return OUTPUT_NUM
            else:
                raise WsSyntaxError(*self.get_line_col())
        elif t == TAB:
            if next_t == SPACE:
                return READ_CHAR
            elif next_t == TAB:
                return READ_NUM
            else:
                raise WsSyntaxError(*self.get_line_col())
        else:
            raise WsSyntaxError(*self.get_line_col())

    def imp(self):
        t = self.iter_token.next()
        if t == SPACE:
            return self.stack_manipulation()
        elif t == LF:
            return self.flow_control()
        else:
            t = self.iter_token.next()
            if t == SPACE:
                return self.arithmetic()
            elif t == TAB:
                return self.heap_access()
            elif t == LF:
                return self.io()
            else:
                raise WsSyntaxError(*self.get_line_col())

    def parse(self):
        instruction = []
        while 1:
            try:
                imp = self.imp()
            except WsSyntaxError, e:
                print_msg(e, abort=True)
            except StopIteration:
                break
            instruction.append(imp)

        return instruction
