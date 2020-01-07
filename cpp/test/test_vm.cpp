#if __GNUG__ > 6
#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#endif

#include "loguru.hpp"

#include <iostream>
#include <boost/test/included/unit_test.hpp>

#include "vm.h"
#include "utils.h"

using namespace boost::unit_test;

#define BOOST_TEST_MODULE vm_module

BOOST_AUTO_TEST_SUITE( vm_day_2 )
BOOST_AUTO_TEST_CASE( test_2_1 )
{
    std::vector<int> p{1,9,10,3,2,3,11,0,99,30,40,50};
    
    VM vm;

    vm.loadIntCode(p);
    vm.execute();
    
    auto &mem = vm.memory();

    LOG_F(INFO, "p[0] = %d", mem[0], mem[3]);
     
    BOOST_CHECK(mem[0] == 3500);
}

BOOST_AUTO_TEST_CASE( test_2_2 )
{
    std::vector<int> p{1,1,1,4,99,5,6,0,99};
    
    VM vm;

    vm.loadIntCode(p);
    vm.execute();
    
    auto &mem = vm.memory();

    LOG_F(INFO, "p[0] = %d", mem[0]);
     
    BOOST_CHECK(mem[0] == 30);
}


BOOST_AUTO_TEST_CASE( test_2_3 )
{
    std::vector<int> p{2,4,4,5,99,0};
    
    VM vm;

    vm.loadIntCode(p);
    vm.execute();
    
    auto &mem = vm.memory();

    LOG_F(INFO, "p[0] = %d", mem[0]);
     
    BOOST_CHECK(mem[0] == 2);
}

BOOST_AUTO_TEST_CASE( test_2_4 )
{
    std::vector<int> p{1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,99};
    
    VM vm;

    vm.loadIntCode(p);
    vm.execute();
    
    auto &mem = vm.memory();

    LOG_F(INFO, "p[0] = %d", mem[0]);
     
    BOOST_CHECK(mem[0] == 1);
}
BOOST_AUTO_TEST_SUITE_END() // vm_day_2

BOOST_AUTO_TEST_SUITE( vm_day_5 )
BOOST_AUTO_TEST_CASE( test_5_1 )
{
    std::vector<int> p{3,9,8,9,10,9,4,9,99,-1,8};
    
    VM vm(
        [](std::string s) -> int {
            return 8;
        },
        [](int i) -> void {
            BOOST_CHECK(i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_2 )
{
    std::vector<int> p{3,9,8,9,10,9,4,9,99,-1,8};
    
    VM vm(
        [](std::string s) -> int {
            return 7;
        },
        [](int i) -> void {
            BOOST_CHECK(!i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_3 )
{
    std::vector<int> p{3,9,7,9,10,9,4,9,99,-1,8};
    
    VM vm(
        [](std::string s) -> int {
            return 7;
        },
        [](int i) -> void {
            BOOST_CHECK(i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_4 )
{
    std::vector<int> p{3,9,7,9,10,9,4,9,99,-1,8};
    
    VM vm(
        [](std::string s) -> int {
            return 8;
        },
        [](int i) -> void {
            BOOST_CHECK(!i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_5 )
{
    std::vector<int> p{3,3,1108,-1,8,3,4,3,99};
    
    VM vm(
        [](std::string s) -> int {
            return 8;
        },
        [](int i) -> void {
            BOOST_CHECK(i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_6 )
{
    std::vector<int> p{3,3,1107,-1,8,3,4,3,99};
    
    VM vm(
        [](std::string s) -> int {
            return 6;
        },
        [](int i) -> void {
            BOOST_CHECK(i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_7 )
{
    std::vector<int> p{3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9};
    
    VM vm(
        [](std::string s) -> int {
            return 0;
        },
        [](int i) -> void {
            BOOST_CHECK(!i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_8 )
{
    LOG_F(INFO, "- test_5_8 -------------------------------------");
    std::vector<int> p{3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9};
    
    VM vm(
        [](std::string s) -> int {
            return 1;
        },
        [](int i) -> void {
            BOOST_CHECK(i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_9 )
{
    LOG_F(INFO, "- test_5_9 -------------------------------------");
    std::vector<int> p{3,3,1105,-1,9,1101,0,0,12,4,12,99,1};
    
    VM vm(
        [](std::string s) -> int {
            return 0;
        },
        [](int i) -> void {
            LOG_F(INFO, "%d", i);
            BOOST_CHECK(!i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_10 )
{
    LOG_F(INFO, "- test_5_10 -------------------------------------");
    std::vector<int> p{3,3,1105,-1,9,1101,0,0,12,4,12,99,1};
    
    VM vm(
        [](std::string s) -> int {
            return 1;
        },
        [](int i) -> void {
            BOOST_CHECK(i);
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}

BOOST_AUTO_TEST_CASE( test_5_11 )
{
    std::vector<int> p{3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                       1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                       999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99
    };
    
    VM vm(
        [](std::string s) -> int {
            return 7;
        },
        [](int i) -> void {
            std::cout << i;
        }
    );

    vm.loadIntCode(p);
    vm.execute();
}
BOOST_AUTO_TEST_SUITE_END() // vm_day_5


//____________________________________________________________________________//

test_suite*
init_unit_test_suite( int argc, char* argv[] )
{
    #ifdef UNIT_TEST_VERBOSITY
        loguru::g_stderr_verbosity = UNIT_TEST_VERBOSITY;
    #else
        loguru::g_stderr_verbosity = loguru::Verbosity_9;
    #endif

    loguru::set_thread_name("Test Vm");

    return 0;
}

//____________________________________________________________________________//
