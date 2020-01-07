#pragma once

#include <vector>
#include <sstream>

template<class T>
std::string vectorToString(std::vector<T> v)
{
    bool first = true;
    std::stringstream ss;
    for (auto x: v)
    {
        if (!first)
        {
            ss << ", ";
        }
        ss << x;
        first = false;
    }
    return ss.str();
}