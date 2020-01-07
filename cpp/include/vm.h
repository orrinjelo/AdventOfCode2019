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
        HALT = 99
    };

    VM( int memSize=512 );
    VM( std::function<int(std::string)>  inputCB, 
        std::function<void(int)> ouputCB,
        int memSize=512
    );
    ~VM() {}

    void loadIntCode(std::ifstream &in);
    void loadIntCode(std::string &s);
    void loadIntCode(std::vector<int> &v);

    void execute();
    void reset();

    void terminate();

    std::vector<int>& memory() { return memory_; }

private:
    bool             running_;
    std::vector<int> memory_;
    Operators        operators_;
    int              pc_;
    int              relativeBase_;

    std::function<int(std::string)>  inputCB_;
    std::function<void(int)> outputCB_;

    void stringToVector(std::string s);
};