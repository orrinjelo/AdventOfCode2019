import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


class ElfMachine():
    def __init__(self, input_cb=input, output_cb=print, mem_size=512):
        self.input_cb = input_cb
        self.output_cb = output_cb
        self.relative_base = 0
        self.mem = [0]*mem_size
        self.mem_size = mem_size
        self.op = {
            1: self.add,
            2: self.mul,
            3: self.inp,
            4: self.prt,
            5: self.jmp,
            6: self.jmf,
            7: self.ltn,
            8: self.eql,
            9: self.rel,
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
            s[c] = x
        elif C == 1:
            s[pc+3] = x
        elif C == 2:
            s[self.relative_base + c] = x

    def add(self, s, pc):
        a, b, c = s[pc + 1], s[pc + 2], s[pc + 3]
        C,B,A, DE = self.scrape_op(s[pc])

        try:
            if A == 0:
                if B == 0:
                    x = s[a] + s[b]
                elif B == 1:
                    x = s[a] + b 
                elif B == 2:
                    x = s[a] + s[self.relative_base + b]
            elif A == 1:
                if B == 0:
                    x = a + s[b]
                elif B == 1:
                    x = a + b
                elif B == 2:
                    x = a + s[self.relative_base + b]
            elif A == 2:
                if B == 0:
                    x = s[self.relative_base + a] + s[b]
                elif B == 1:
                    x = s[self.relative_base + a] + b
                elif B == 2:
                    x = s[self.relative_base + a] + s[self.relative_base + b]


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
                elif B == 1:
                    x = s[a] * b
                elif B == 2:
                    x = s[a] * s[self.relative_base + b] 
            elif A == 1:
                if B == 0:
                    x = a * s[b]
                elif B == 1:
                    x = a * b
                elif B == 2:
                    x = a * s[self.relative_base + b]
            elif A == 2:
                if B == 0:
                    x = s[self.relative_base + a] * s[b]
                elif B == 1:
                    x = s[self.relative_base + a] * b
                elif B == 2:
                    x = s[self.relative_base + a] * s[self.relative_base + b]

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
            elif C == 1:
                self.output_cb(c)
            elif C == 2:
                self.output_cb(s[self.relative_base + c])
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
                elif B == 1:
                    if b:
                        pc = s[c]
                    else:
                        pc += 3
                elif B == 2:
                    if s[self.relative_base + b]:
                        pc = s[c]
                    else:
                        pc += 3
            elif C == 1:
                if B == 0:
                    if s[b]:
                        pc = c
                    else:
                        pc += 3
                elif B == 1:
                    if b:
                        pc = c
                    else:
                        pc += 3
                elif B == 2:
                    if s[self.relative_base + b]:
                        pc = c
                    else:
                        pc += 3
            elif C == 2:
                if B == 0:
                    if s[b]:
                        pc = s[self.relative_base + c]
                    else:
                        pc += 3
                elif B == 1:
                    if b:
                        pc = s[self.relative_base + c]
                    else:
                        pc += 3
                elif B == 2:
                    if s[self.relative_base + b]:
                        pc = s[self.relative_base + c]
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
                elif B == 1:
                    if not b:
                        pc = s[c]
                    else:
                        pc += 3
                elif B == 2:
                    if not s[self.relative_base + b]:
                        pc = s[c]
                    else:
                        pc += 3
            elif C == 1:
                if B == 0:
                    if not s[b]:
                        pc = c
                    else:
                        pc += 3
                elif B == 1:
                    if not b:
                        pc = c
                    else:
                        pc += 3
                elif B == 2:
                    if not s[self.relative_base + b]:
                        pc = c
                    else:
                        pc += 3
            elif C == 2:
                if B == 0:
                    if not s[b]:
                        pc = s[self.relative_base + c]
                    else:
                        pc += 3
                elif B == 1:
                    if not b:
                        pc = s[self.relative_base + c]
                    else:
                        pc += 3
                elif B == 2:
                    if not s[self.relative_base + b]:
                        pc = s[self.relative_base + c]
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
                elif B == 1:
                    x = 1 if s[a] < b else 0
                elif B == 2:
                    x = 1 if s[a] < s[self.relative_base + b] else 0
            elif A == 1:
                if B == 0:
                    x = 1 if a < s[b] else 0
                elif B == 1:
                    x = 1 if a < b else 0
                elif B == 2:
                    x = 1 if a < s[self.relative_base + b] else 0
            elif A == 2:
                if B == 0:
                    x = 1 if s[self.relative_base + a] < s[b] else 0
                elif B == 1:
                    x = 1 if s[self.relative_base + a] < b else 0
                elif B == 2:
                    x = 1 if s[self.relative_base + a] < s[self.relative_base + b] else 0


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
                elif B == 1:
                    x = 1 if s[a] == b else 0
                elif B == 2:
                    x = 1 if s[a] == s[self.relative_base + b] else 0
            elif A == 1:
                if B == 0:
                    x = 1 if a == s[b] else 0
                elif B == 1:
                    x = 1 if a == b else 0
                elif B == 2:
                    x = 1 if a == s[self.relative_base + b] else 0
            elif A == 2:
                if B == 0:
                    x = 1 if s[self.relative_base + a] == s[b] else 0
                elif B == 1:
                    x = 1 if s[self.relative_base + a] == b else 0
                elif B == 2:
                    x = 1 if s[self.relative_base + a] == s[self.relative_base + b] else 0       

            self._set(s, pc, c, x, C)
            pc += 4
        except IndexError as e:
            print('Invalid index: {} {} {}'.format(a, b, c))
            print('Input list: {}'.format(s))
            raise e
        return pc

    def rel(self, s, pc):
        c = s[pc + 1]
        _, _, C, DE = self.scrape_op(s[pc])

        if C == 0:
            self.relative_base += s[c]
        elif C == 1:
            self.relative_base += c
        else:
            self.relative_base += s[self.relative_base + c]

        pc += 2
        return pc        


    def run_program(self, s, p1=None, p2=None):
        self.finished = False
        self.relative_base = 0
        self.mem = [0]*self.mem_size
        self.mem[:len(s)] = s
        pc = 0
        if p1:
            self.mem[1] = p1
        if p2:
            self.mem[2] = p2
        while s[pc] != 99 and not self.finished: # Program term
            # try:
                pc = self.op[self.mem[pc]%100](self.mem, pc)
            # except Exception as e:
            #     print('Except: {}'.format(e))
            #     print('Erroneous op: {}'.format(s[pc]))
            #     sys.exit(0)
        self.finished = True
        return pc, s
