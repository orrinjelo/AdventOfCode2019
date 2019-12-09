import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


class ElfMachine():
    def __init__(self, input_cb=input, output_cb=print):
        self.input_cb = input_cb
        self.output_cb = output_cb
        self.op = {
            1: self.add,
            2: self.mul,
            3: self.inp,
            4: self.prt,
            5: self.jmp,
            6: self.jmf,
            7: self.ltn,
            8: self.eql
        }

    def scrape_op(self, x):
        # Position 0, immediate 1
        DE = x % 100
        C = x // 100 % 10
        B = x // 1000 % 10
        A = x // 10000 % 10
        return A, B, C, DE

    def _set(self, s, pc, c, x, C):
        if C == 0:
            s[c]    = x
        else:
            s[pc+3] = x

    def add(self, s, pc):
        a, b, c = s[pc + 1], s[pc + 2], s[pc + 3]
        C,B,A, DE = self.scrape_op(s[pc])

        try:
            if A == 0:
                if B == 0:
                    x = s[a] + s[b]
                else:
                    x = s[a] + b 
            else:
                if B == 0:
                    x = a + s[b]
                else:
                    x = a + b
            self._set(s, pc, c, x, C)
            pc += 4
        except IndexError as e:
            print('Invalid index: {} {} {}'.format(a, b, c))
            print('Input list: {}'.format(s))
            raise e
        return pc

    def mul(self, s, pc):
        a, b, c = s[pc + 1], s[pc + 2], s[pc + 3]
        C, B, A, DE = self.scrape_op(s[pc])

        try:
            if A == 0:
                if B == 0:
                    x = s[a] * s[b]
                else:
                    x = s[a] * b 
            else:
                if B == 0:
                    x = a * s[b]
                else:
                    x = a * b
            self._set(s, pc, c, x, C)
            pc += 4
        except IndexError as e:
            print('Invalid index: {} {} {}'.format(a, b, c))
            print('Input list: {}'.format(s))
            raise e
        return pc

    def inp(self, s, pc):
        c = s[pc + 1]
        _, _, C, DE = self.scrape_op(s[pc])

        try:
            x = int(self.input_cb('> '))
            self._set(s,pc, c, x, C)
            pc += 2
        except IndexError as e:
            print('Invalid index:  {}'.format(c))
            print('Input list: {}'.format(s))
            raise e
        return pc

    def prt(self, s, pc):
        c = s[pc + 1]
        _, _, C, DE = self.scrape_op(s[pc])

        try:
            if C == 0:
                self.output_cb(s[c])
                # print(s[c])
            else:
                self.output_cb(c)
                # print(s)
            pc += 2
        except IndexError as e:
            print('Invalid index: {}'.format(c))
            print('Input list: {}'.format(s))
            raise e
        return pc

    def jmp(self, s, pc):
        b, c = s[pc + 1], s[pc + 2]
        _, C, B, DE = self.scrape_op(s[pc])

        try:
            if C == 0:
                if B == 0:
                    if s[b]:
                        pc = s[c]
                    else:
                        pc += 3
                else:
                    if b:
                        pc = s[c]
                    else:
                        pc += 3
            else:
                if B == 0:
                    if s[b]:
                        pc = c
                    else:
                        pc += 3
                else:
                    if b:
                        pc = c
                    else:
                        pc += 3
        except IndexError as e:
            print('Invalid index: {} {}'.format(b, c))
            print('Input list: {}'.format(s))
            raise e
        return pc    

    def jmf(self, s, pc):
        b, c = s[pc + 1], s[pc + 2]
        _, C, B, DE = self.scrape_op(s[pc])

        try:
            if C == 0:
                if B == 0:
                    if not s[b]:
                        pc = s[c]
                    else:
                        pc += 3
                else:
                    if not b:
                        pc = s[c]
                    else:
                        pc += 3
            else:
                if B == 0:
                    if not s[b]:
                        pc = c
                    else:
                        pc += 3
                else:
                    if not b:
                        pc = c
                    else:
                        pc += 3
        except IndexError as e:
            print('Invalid index: {} {}'.format(b, c))
            print('Input list: {}'.format(s))
            raise e
        return pc 

    def ltn(self, s, pc):
        a, b, c = s[pc + 1], s[pc + 2], s[pc + 3]
        C, B, A, DE = self.scrape_op(s[pc])

        try:
            if A == 0:
                if B == 0:
                    x = 1 if s[a] < s[b] else 0
                else:
                    x = 1 if s[a] < b else 0
            else:
                if B == 0:
                    x = 1 if a < s[b] else 0
                else:
                    x = 1 if a < b else 0
            self._set(s, pc, c, x, C)
            pc += 4
        except IndexError as e:
            print('Invalid index: {} {} {}'.format(a, b, c))
            print('Input list: {}'.format(s))
            raise e
        return pc

    def eql(self, s, pc):
        a, b, c = s[pc + 1], s[pc + 2], s[pc + 3]
        C, B, A, DE = self.scrape_op(s[pc])

        try:
            if A == 0:
                if B == 0:
                    x = 1 if s[a] == s[b] else 0
                else:
                    x = 1 if s[a] == b else 0
            else:
                if B == 0:
                    x = 1 if a == s[b] else 0
                else:
                    x = 1 if a == b else 0
            self._set(s, pc, c, x, C)
            pc += 4
        except IndexError as e:
            print('Invalid index: {} {} {}'.format(a, b, c))
            print('Input list: {}'.format(s))
            raise e
        return pc


    def run_program(self, s, p1=None, p2=None):
        self.finished = False
        pc = 0
        if p1:
            s[1] = p1
        if p2:
            s[2] = p2
        while s[pc] != 99: # Program term
            # try:
                pc = self.op[s[pc]%100](s, pc)
            # except Exception as e:
            #     print(e)
            #     print('Erroneous op: {}'.format(s[pc]))
            #     sys.exit(0)
        self.finished = True
        return pc, s
