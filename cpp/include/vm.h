#pragma once

#include <functional>
#include <string>
#include <vector>
#include <fstream>

#include "operators.h"

class VM
{
public:
    enum OpCode {
        ADD = 1,
        MUL = 2,
        INP = 3,
        PRT = 4,
        JMP = 5,
        JMF = 6,
        LTN = 7,
        EQL = 8,
        REL = 9,
        HALT = 99
    };

    VM( int memSize=4096 );
    VM( std::function<big_int(std::string)>  inputCB, 
        std::function<void(big_int&)> ouputCB,
        int memSize=4096
    );
    ~VM() {}

    void loadIntCode(std::ifstream &in);
    void loadIntCode(std::string &s);
    void loadIntCode(vector_big_int &v);

    void execute();
    void reset();

    void terminate();

    vector_big_int& memory() { return memory_; }

private:
    bool             running_;
    vector_big_int   memory_;
    Operators        operators_;
    int              pc_;
    int              relativeBase_;

    std::function<int(std::string)>  inputCB_;
    std::function<void(big_int&)> outputCB_;

    void stringToVector(std::string s);
};