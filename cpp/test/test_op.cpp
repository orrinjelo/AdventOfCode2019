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
    LOG_F(INFO, "- test_add_1 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{1,9,10,3,2,3,11,0,99,30,40,50};
    
    op.add(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 4);
    BOOST_CHECK(p[3] == 70);
}

BOOST_AUTO_TEST_CASE( test_add_2 )
{
    LOG_F(INFO, "- test_add_2 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{1001,9,10,3,2,3,11,0,99,30,40,50};
    
    op.add(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 4);
    BOOST_CHECK(p[3] == 40);
}

BOOST_AUTO_TEST_CASE( test_add_3 )
{
    LOG_F(INFO, "- test_add_3 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{101,9,10,3,2,3,11,0,99,30,40,50};
    
    op.add(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 4);
    BOOST_CHECK(p[3] == 49);
}

BOOST_AUTO_TEST_CASE( test_add_4 )
{
    LOG_F(INFO, "- test_add_4 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{1101,9,10,3,2,3,11,0,99,30,40,50};
    
    op.add(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 4);
    BOOST_CHECK(p[3] == 19);
}

BOOST_AUTO_TEST_CASE( test_add_5 )
{
    LOG_F(INFO, "- test_add_5 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 1;
    vector_big_int p{201,9,10,3,2,3,11,0,99,30,40,50};
    
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
    LOG_F(INFO, "- test_mul_1 ---------------------------");
    Operators op;
    int pc = 4;
    int relativeBase = 0;
    vector_big_int p{1,9,10,70,2,3,11,0,99,30,40,50};
    
    op.mul(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 8);
    BOOST_CHECK(p[0] == 3500);
}

BOOST_AUTO_TEST_CASE( test_mul_2 )
{
    LOG_F(INFO, "- test_mul_2 ---------------------------");
    Operators op;
    int pc = 4;
    int relativeBase = 0;
    vector_big_int p{1,9,10,70,102,3,11,0,99,30,40,50};
    
    op.mul(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d, relativeBase = %d", pc, relativeBase);
    LOG_F(INFO, "p[0] = %d, p[3] = %d", p[0], p[3]);
     
    BOOST_CHECK(pc == 8);
    BOOST_CHECK(p[0] == 150);
}
BOOST_AUTO_TEST_SUITE_END() // op_mul

BOOST_AUTO_TEST_SUITE( op_inp )
BOOST_AUTO_TEST_CASE( test_inp_1 )
{
    LOG_F(INFO, "- test_mul_3 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{3,3,99,-1};

    op.inp(p, pc, relativeBase, 
        [](std::string s) -> int {
            return 8;
        }
    );

    BOOST_CHECK(p[3] == 8);
}
BOOST_AUTO_TEST_SUITE_END() // op_inp

BOOST_AUTO_TEST_SUITE( op_prt )
BOOST_AUTO_TEST_CASE( test_prt_1 )
{
    LOG_F(INFO, "- test_prt_1 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{4,3,99,42};

    op.prt(p, pc, relativeBase, 
        [](int x) -> void {
            BOOST_CHECK(x == 42);
        }
    );
}
BOOST_AUTO_TEST_SUITE_END() // op_prt

BOOST_AUTO_TEST_SUITE( op_jmp )
BOOST_AUTO_TEST_CASE( test_jmp_1 )
{
    LOG_F(INFO, "- test_jmp_1 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{1105,1,33};

    op.jmp(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d", pc);

    BOOST_CHECK(pc == 33);
}

BOOST_AUTO_TEST_CASE( test_jmp_2 )
{
    LOG_F(INFO, "- test_jmp_2 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{1105,0,33};

    op.jmp(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d", pc);

    BOOST_CHECK(pc == 3);
}
BOOST_AUTO_TEST_SUITE_END() // op_jmp

BOOST_AUTO_TEST_SUITE( op_jmf )
BOOST_AUTO_TEST_CASE( test_jmf_1 )
{
    LOG_F(INFO, "- test_jmf_1 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{1106,1,33};

    op.jmf(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d", pc);

    BOOST_CHECK(pc == 3);
}

BOOST_AUTO_TEST_CASE( test_jmf_2 )
{
    LOG_F(INFO, "- test_jmf_2 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{1106,0,33};

    op.jmf(p, pc, relativeBase);

    LOG_F(INFO, "pc = %d", pc);

    BOOST_CHECK(pc == 33);
}
BOOST_AUTO_TEST_SUITE_END() // op_jmf

BOOST_AUTO_TEST_SUITE( op_ltn )
BOOST_AUTO_TEST_CASE( test_ltn_1 )
{
    LOG_F(INFO, "- test_ltn_1 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{7,5,6,7,99,1,2,0};

    op.ltn(p, pc, relativeBase);

    BOOST_CHECK(p[7] == 1);
}

BOOST_AUTO_TEST_CASE( test_ltn_2 )
{
    LOG_F(INFO, "- test_ltn_2 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{7,5,6,7,99,2,1,0};

    op.ltn(p, pc, relativeBase);

    BOOST_CHECK(p[7] == 0);
}
BOOST_AUTO_TEST_SUITE_END() // op_ltn

BOOST_AUTO_TEST_SUITE( op_eql )
BOOST_AUTO_TEST_CASE( test_eql_1 )
{
    LOG_F(INFO, "- test_eql_1 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{8,5,6,7,99,1,2,0};

    op.eql(p, pc, relativeBase);

    BOOST_CHECK(p[7] == 0);
}

BOOST_AUTO_TEST_CASE( test_eql_2 )
{
    LOG_F(INFO, "- test_eql_2 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{8,5,6,7,99,1,1,0};

    op.eql(p, pc, relativeBase);

    BOOST_CHECK(p[7] == 1);
}
BOOST_AUTO_TEST_SUITE_END() // op_eql
BOOST_AUTO_TEST_SUITE( op_rel )
BOOST_AUTO_TEST_CASE( test_rel_1 )
{
    LOG_F(INFO, "- test_rel_1 ---------------------------");
    Operators op;
    int pc = 0;
    int relativeBase = 0;
    vector_big_int p{109,5,99};

    op.rel(p, pc, relativeBase);
    LOG_F(INFO, "relativeBase = %d", relativeBase);

    BOOST_CHECK(relativeBase == 5);
}
BOOST_AUTO_TEST_SUITE_END() // op_rel

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
