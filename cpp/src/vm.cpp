#include <stdexcept>
#include <iostream>
#include <boost/algorithm/string.hpp>

#include "loguru.hpp"
#include "vm.h"

VM::VM( int memSize ) : running_(false), pc_(0), relativeBase_(0)
{
    memory_.resize(memSize);

    inputCB_ = [](std::string s) -> int {
        std::cout << s;
        int i = 0;
        std::cin >> i;
        return i;
    };

    outputCB_ = [](std::string s) -> void {
        std::cout << s;
    };
}

VM::VM( std::function<int(std::string)>  inputCB, 
        std::function<void(std::string)> ouputCB,
        int memSize
) : running_(false), pc_(0), relativeBase_(0)
{
    inputCB_ = inputCB;
    outputCB_ = ouputCB;
    memory_.resize(memSize);
}

void VM::loadIntCode(std::ifstream &in)
{
    std::string inputs;
    in >> inputs;
    loadIntCode(inputs);
}

void VM::loadIntCode(std::string &s)
{
    std::vector<std::string> sv;
    boost::split(sv, s, boost::is_any_of(","));
    for (unsigned int i=0; i<sv.size(); ++i)
        memory_[i] = std::stoi(sv[i]);
}

void VM::loadIntCode(std::vector<int> &v)
{
    memory_ = v;
}

void VM::reset()
{
    for (auto &entry : memory_)
        entry = 0;
    pc_ = 0;
    relativeBase_ = 0;
}

void VM::terminate()
{
    running_ = false;
}

void VM::execute()
{
    running_ = true;

    while (running_)
    {
        switch(memory_[pc_])
        {
            case ADD: operators_.add(memory_, pc_, relativeBase_); break;
            case MUL: operators_.mul(memory_, pc_, relativeBase_); break;
            case HALT: running_ = false; break;
            default:
                LOG_F(ERROR, "Unknown op: %d", memory_[pc_]);
                throw std::runtime_error("Invalid op code.");
        };
    }
}
