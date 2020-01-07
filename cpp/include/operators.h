#pragma once

#include <vector>
#include <functional>

typedef int64_t big_int;
typedef std::vector<big_int> vector_big_int;

class Operators
{
public:
    Operators() {};
    ~Operators() {};

    void add(
        vector_big_int   &program,
        int              &pc,
        int              offset=0
    );

    void mul(
        vector_big_int   &program,
        int              &pc,
        int              offset=0
    );

    void inp(
        vector_big_int   &program,
        int              &pc,
        int              offset,
        std::function<big_int(std::string)> inputCallback
    );

    void prt(
        vector_big_int   &program,
        int              &pc,
        int              offset,
        std::function<void(big_int&)> outputCallback
    );

    void jmp(
        vector_big_int   &program,
        int              &pc,
        int              offset=0
    );

    void jmf(
        vector_big_int   &program,
        int              &pc,
        int              offset=0
    );

    void ltn(
        vector_big_int   &program,
        int              &pc,
        int              offset=0
    );

    void eql(
        vector_big_int   &program,
        int              &pc,
        int              offset=0
    );

    void rel(
        vector_big_int   &program,
        int              &pc,
        int              &offset
    );

private:
    void scrapeOp(
        int x, 
        int &A,
        int &B,
        int &C,
        int &DE
    );

    void interpretOperand(
        vector_big_int  &program, 
        big_int          &o, 
        int              O, 
        int              offset
    );

    void interpretOperandAndSet(
        vector_big_int  &program, 
        big_int          value, 
        big_int          &c, 
        int              C, 
        int              &offset
    );
};
