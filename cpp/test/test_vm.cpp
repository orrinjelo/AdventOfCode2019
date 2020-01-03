#if __GNUG__ > 6
#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#endif

#include "loguru.hpp"

#include <iostream>
#include <boost/test/included/unit_test.hpp>

#include "vm.h"

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
