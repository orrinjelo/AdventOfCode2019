#include <stdexcept>

#include "loguru.hpp"
#include "operators.h"

void Operators::scrapeOp(int x, int &A, int &B, int &C, int &DE)
{
    DE = x % 100;
    C = static_cast<int>(x / 100) % 10;
    B = static_cast<int>(x / 1000) % 10;
    A = static_cast<int>(x / 10000) % 10;
}

void Operators::interpretOperand(std::vector<int> &program, int &o, int O, int offset)
{
    LOG_F(MAX, "O = %d, o = %d, offset = %d", O, o, offset);
    switch (O)
    {
        case 0: // a is an address
            o = program[o];
            break;
        case 1: // a is a value
            break;
        case 2: // a is an offset
            o = program[o + offset];
            break;
        default:
            throw std::runtime_error("Invalid opcode.");
    };    
    LOG_F(MAX, "o = %d", o);
}

void Operators::interpretOperandAndSet(std::vector<int> &program, int value, int &c, int C, int offset)
{
    LOG_F(MAX, "value = %d, C = %d, c = %d, offset = %d", value, C, c, offset);
    switch (C)
    {
        case 0: // a is an address
            program[c] = value;
            break;
        case 1: // a is a value
            c = value;
            break;
        case 2: // a is an offset
            program[c+ offset] = value;
            break;
        default:
            throw std::runtime_error("Invalid opcode.");
    };    
}

void Operators::add(
        std::vector<int> &program,
        int              &pc,
        int              offset
    )
{
    int a  = program[pc + 1];
    int b  = program[pc + 2];
    int &c = program[pc + 3];

    int A,B,C,DE;
    scrapeOp(program[pc],A,B,C,DE);
    LOG_F(MAX, "A=%d, B=%d, C=%d, DE=%d",A,B,C,DE);

    try
    {
        interpretOperand(program, a, C, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad A.");
    }

    try
    {
        interpretOperand(program, b, B, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad B.");
    }
    
    try
    {
        interpretOperandAndSet(program, a+b, c, A, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad C.");
    }

    pc += 4;
}


void Operators::mul(
        std::vector<int> &program,
        int              &pc,
        int              offset
    )
{
    int a  = program[pc + 1];
    int b  = program[pc + 2];
    int &c = program[pc + 3];

    int A,B,C,DE;
    scrapeOp(program[pc],A,B,C,DE);

    try
    {
        interpretOperand(program, a, C, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad A.");
    }

    try
    {
        interpretOperand(program, b, B, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad B.");
    }
    
    try
    {
        interpretOperandAndSet(program, a*b, c, A, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad C.");
    }

    pc += 4;
}


void Operators::inp(
        std::vector<int> &program,
        int              &pc,
        int              offset,
        std::function<int(std::string)> inputCallback
    )
{
    int &c = program[pc + 1];

    int A,B,C,DE;
    scrapeOp(program[pc],C,A,B,DE);

    int x = 0;
    try
    {
        x = inputCallback(">");
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Input callback.");
    }

    try
    {
        interpretOperandAndSet(program, x, c, C, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad C.");
    }

    pc += 2;
}


void Operators::prt(
        std::vector<int> &program,
        int              &pc,
        int              offset,
        std::function<void(int)> outputCallback
    )
{
    int &c = program[pc + 1];

    int A,B,C,DE;
    scrapeOp(program[pc],C,A,B,DE);

    try
    {
        if (C == 0)
            outputCallback(program[c]);
        else
            outputCallback(c);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Input callback.");
    }

    pc += 2;
}

void Operators::jmp(
        std::vector<int> &program,
        int              &pc,
        int              offset
    )
{
    int b = program[pc + 1];
    int c = program[pc + 2];

    int A,B,C,DE;
    scrapeOp(program[pc],A,B,C,DE);

    try
    {
        interpretOperand(program, b, C, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad B.");
    }

    try
    {
        interpretOperand(program, c, B, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad C.");
    }

    if (b)
        pc = c;
    else
        pc += 3;
}


void Operators::jmf(
        std::vector<int> &program,
        int              &pc,
        int              offset
    )
{
    int b = program[pc + 1];
    int c = program[pc + 2];

    int A,B,C,DE;
    scrapeOp(program[pc],A,B,C,DE);

    try
    {
        interpretOperand(program, b, C, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad B.");
    }

    try
    {
        interpretOperand(program, c, B, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad C.");
    }

    if (!b)
        pc = c;
    else
        pc += 3;
}


void Operators::ltn(
        std::vector<int> &program,
        int              &pc,
        int              offset
    )
{
    int a  = program[pc + 1];
    int b  = program[pc + 2];
    int &c = program[pc + 3];

    int A,B,C,DE;
    scrapeOp(program[pc],A,B,C,DE);

    try
    {
        interpretOperand(program, a, C, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad A.");
    }

    try
    {
        interpretOperand(program, b, B, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad B.");
    }
    
    try
    {
        interpretOperandAndSet(program, a < b ? 1 : 0, c, A, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad C.");
    }

    pc += 4;
}


void Operators::eql(
        std::vector<int> &program,
        int              &pc,
        int              offset
    )
{
    int a  = program[pc + 1];
    int b  = program[pc + 2];
    int &c = program[pc + 3];

    int A,B,C,DE;
    scrapeOp(program[pc],A,B,C,DE);

    try
    {
        interpretOperand(program, a, B, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad A.");
    }

    try
    {
        interpretOperand(program, b, A, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad B.");
    }
    
    try
    {
        interpretOperandAndSet(program, a == b ? 1 : 0, c, C, offset);
    } catch (std::runtime_error &e)
    {
        LOG_F(ERROR, "Bad C.");
    }

    pc += 4;
}
