add_compile_options (
    -Wall
    -O2
    -ggdb
)

add_executable (
    test_op
    ${CMAKE_SOURCE_DIR}/test/test_op.cpp
    ${CMAKE_SOURCE_DIR}/loguru/loguru.cpp
)

target_link_libraries(
    test_op
    vm
    ${Boost_LIBRARIES}
    pthread
    ${CMAKE_DL_LIBS}
)

add_executable (
    test_vm
    ${CMAKE_SOURCE_DIR}/test/test_vm.cpp
    ${CMAKE_SOURCE_DIR}/loguru/loguru.cpp
)

target_link_libraries(
    test_vm
    vm
    ${Boost_LIBRARIES}
    pthread
    ${CMAKE_DL_LIBS}
)

