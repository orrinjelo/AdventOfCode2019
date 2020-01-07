#include <boost/program_options.hpp>
#include <boost/program_options/parsers.hpp>
#include <boost/tokenizer.hpp>
#include <boost/filesystem.hpp>

#include <fstream>
#include <iostream>

#include "loguru.hpp"

namespace po = boost::program_options;
namespace fs = boost::filesystem;

#include "vm.h"

int main( int ac, char* av[] )
{
    po::options_description desc("Allowed options");
    desc.add_options()
        ("help",                                "produce this help message")
        ("input,i",   po::value<std::string>(), "int code file to parse and run")
        ("memsize,s", po::value<int>()->default_value(512), "memory size")
        ("memset,m",  po::value<std::vector<int>>()->multitoken(), "memory size")
        ("optimal_date",po::value<int>(), "day 2 part 2 target date")
    ;

    po::variables_map vm;
    po::parsed_options parsed = po::command_line_parser(ac, av).options(desc).allow_unregistered().run();
    auto to_pass_further = po::collect_unrecognized(parsed.options, po::include_positional);
    po::store( parsed, vm );
    po::notify(vm);

    loguru::init(ac, av);

    if (vm.count("help"))
    {
        std::cout << desc << std::endl;
        return 0;
    }

    VM elf(vm["memsize"].as<int>());

    if (vm.count("optimal_date"))
    {
        // e.g 19690720
        std::ifstream in(vm["input"].as<std::string>());
        std::string inputCode;
        in >> inputCode;
        for (int i=0; i < 100; ++i)
        {
            for (int j=0; j<100; ++j)
            {
                elf.reset();
                elf.loadIntCode(inputCode);
                auto &mem = elf.memory();
                mem[1] = i;
                mem[2] = j;
                elf.execute();
                if (mem[0] == vm["optimal_date"].as<int>())
                {
                    std::cout << i*100 + j << std::endl;
                    return 0;
                }

            }
        }
                
    }

    if (vm.count("input"))
    {
        std::ifstream in(vm["input"].as<std::string>());
        elf.loadIntCode(in);
    }

    if (vm.count("memset"))
    {
        std::vector<int> tokens = vm["memset"].as<std::vector<int>>();
        int len = tokens.size();
        auto &mem = elf.memory();
        for (int i=0; i<len; i+=2)
        {
            LOG_F(INFO, "Set (%d) to %d", tokens[i], tokens[i+1]);
            mem[tokens[i]] = tokens[i+1];
        }
    }

    elf.execute();

    std::cout << "Memory location 0: " << elf.memory()[0] << std::endl;

    return 0;

}