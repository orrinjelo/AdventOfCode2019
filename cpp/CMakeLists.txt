cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
project(elfvm LANGUAGES C CXX)

find_package(
    Boost 1.65.0
    COMPONENTS filesystem
               system
               program_options
               numpy${BOOST_PYTHON_SUFFIX}
               python${BOOST_PYTHON_SUFFIX}
    REQUIRED
)

find_package(
    Python3
    COMPONENTS
        Interpreter
        Development
)

include_directories(
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/loguru
)

add_executable(
    elfvm
        loguru/loguru.cpp
        src/main.cpp    
)

add_library(
    vm STATIC
        src/operators.cpp
        src/vm.cpp
)

target_compile_features (
    vm
    PUBLIC
        cxx_std_14
)

target_compile_options (
    vm
    PRIVATE
        -Wall
        -O3
)

target_link_libraries(
    elfvm
        vm
        ${Boost_LIBRARIES}
        pthread
        ${CMAKE_DL_LIBS}    
)

option(BUILD_TESTS "Build the tests inclusive" ON)
if (BUILD_TESTS)
add_subdirectory(test)
endif()

