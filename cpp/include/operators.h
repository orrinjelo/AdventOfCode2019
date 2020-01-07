#pragma once

#include <vector>
#include <functional>

class Operators
{
public:
    Operators() {};
    ~Operators() {};

    void add(
        std::vector<int> &program,
        int              &pc,
        int              offset=0
    );

    void mul(
        std::vector<int> &program,
        int              &pc,
        int              offset=0
    );

    void inp(
        std::vector<int> &program,
        int              &pc,
        int              offset,
        std::function<int(std::string)> inputCallback
    );

    void prt(
        std::vector<int> &program,
        int              &pc,
        int              offset,
        std::function<void(int)> outputCallback
    );

    void jmp(
        std::vector<int> &program,
        int              &pc,
        int              offset=0
    );

    void jmf(
        std::vector<int> &program,
        int              &pc,
        int              offset=0
    );

    void ltn(
        std::vector<int> &program,
        int              &pc,
        int              offset=0
    );

    void eql(
        std::vector<int> &program,
        int              &pc,
        int              offset=0
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
        std::vector<int> &program, 
        int              &o, 
        int              O, 
        int              offset
    );

    void interpretOperandAndSet(
        std::vector<int> &program, 
        int              value, 
        int              &c, 
        int              C, 
        int              offset
    );
};
