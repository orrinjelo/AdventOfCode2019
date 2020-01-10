cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
project(elfvm LANGUAGES C CXX)

find_package(
    Boost 1.65.0
    COMPONENTS filesystem
               system
               program_options
               numpy3
               python3
    REQUIRED
)

set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

if (NOT Boost_PYTHON3_FOUND)
    find_package(Boost 1.67.0 COMPONENTS python36 numpy36)
    if (Boost_PYTHON36_FOUND)
        set(Boost_PYTHON3_LIBRARY ${Boost_PYTHON36_LIBRARY})
        set(Boost_NUMPY3_LIBRARY  ${Boost_NUMPY36_LIBRARY})
    else()
        # This is the last check, if it fails then error out
        find_package(Boost 1.67.0 COMPONENTS python37 numpy37 REQUIRED)
        set(Boost_PYTHON3_LIBRARY ${Boost_PYTHON37_LIBRARY})
        set(Boost_NUMPY3_LIBRARY  ${Boost_NUMPY37_LIBRARY})
    endif()
endif()

## == Python-Enabled =====================

message(STATUS "Python3_LIBRARIES = ${Python3_LIBRARIES}")
message(STATUS "Boost_PYTHON3_LIBRARY = ${Boost_PYTHON3_LIBRARY}")
message(STATUS "Boost_NUMPY3_LIBRARY = ${Boost_NUMPY3_LIBRARY}")


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

add_library(
    PyElfVm
    SHARED
        src/PyElfVm.cpp
        loguru/loguru.cpp        
)

target_compile_features (
    PyElfVm
    PUBLIC
        cxx_std_14
)

target_compile_options (
    vm
    PRIVATE
        -fPIC
        -Wall
        -O3
)

target_link_libraries(
    PyElfVm
        ${Python3_LIBRARIES}
        ${Boost_PYTHON3_LIBRARY}
        ${Boost_NUMPY3_LIBRARY}
        ${CMAKE_DL_LIBS}
        Threads::Threads
        vm
)

target_include_directories(
    PyElfVm
    PRIVATE
        ${Python3_INCLUDE_DIRS}
)

set_target_properties(
    PyElfVm
    PROPERTIES
        POSITION_INDEPENDENT_CODE ON
        PREFIX ""
)

option(BUILD_TESTS "Build the tests inclusive" ON)
if (BUILD_TESTS)
add_subdirectory(test)
endif()

