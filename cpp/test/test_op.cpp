#if __GNUG__ > 6
#pragma GCC diagnostic ignored "-Wint-in-bool-context"
#endif

#include "loguru.hpp"

#include <iostream>
#include <boost/test/included/unit_test.hpp>

#include "operators.h"

using namespace boost::unit_test;

#define BOOST_TEST_MODULE op_module

BOOST_AUTO_TEST_SUITE( op_add )
BOOST_AUTO_TEST_CASE( test_add_1 )
{
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    std::vector<int> p{1,9,10,3,2,3,11,0,99,30,40,50};
    
    op.add(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 4);
    BOOST_CHECK(p[3] == 70);
}

BOOST_AUTO_TEST_CASE( test_add_2 )
{
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    std::vector<int> p{1001,9,10,3,2,3,11,0,99,30,40,50};
    
    op.add(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 4);
    BOOST_CHECK(p[3] == 40);
}

BOOST_AUTO_TEST_CASE( test_add_3 )
{
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    std::vector<int> p{10001,9,10,3,2,3,11,0,99,30,40,50};
    
    op.add(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 4);
    BOOST_CHECK(p[3] == 49);
}

BOOST_AUTO_TEST_CASE( test_add_4 )
{
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    std::vector<int> p{11001,9,10,3,2,3,11,0,99,30,40,50};
    
    op.add(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 4);
    BOOST_CHECK(p[3] == 19);
}

BOOST_AUTO_TEST_CASE( test_add_5 )
{
    Operators op;
    int pc = 0;
    int relativeBase = 1;
    std::vector<int> p{20001,9,10,3,2,3,11,0,99,30,40,50};
    
    op.add(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 4);
    BOOST_CHECK(p[3] == 80);
}
BOOST_AUTO_TEST_SUITE_END() // op_add

BOOST_AUTO_TEST_SUITE( op_mul )
BOOST_AUTO_TEST_CASE( test_mul_1 )
{
    Operators op;
    int pc = 4;
    int relativeBase = 0;
    std::vector<int> p{1,9,10,70,2,3,11,0,99,30,40,50};
    
    op.mul(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 8);
    BOOST_CHECK(p[0] == 3500);
}

BOOST_AUTO_TEST_CASE( test_mul_2 )
{
    Operators op;
    int pc = 4;
    int relativeBase = 0;
    std::vector<int> p{1,9,10,70,10002,3,11,0,99,30,40,50};
    
    op.mul(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 8);
    BOOST_CHECK(p[0] == 150);
}
BOOST_AUTO_TEST_SUITE_END() // op_mul


//____________________________________________________________________________//

test_suite*
init_unit_test_suite( int argc, char* argv[] )
{
    #ifdef UNIT_TEST_VERBOSITY
        loguru::g_stderr_verbosity = UNIT_TEST_VERBOSITY;
    #else
        loguru::g_stderr_verbosity = loguru::Verbosity_9;
    #endif

    loguru::set_thread_name("Test Op");

    return 0;
}

//____________________________________________________________________________//
