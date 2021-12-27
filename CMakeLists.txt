cmake_minimum_required(VERSION 3.15)

option(JUCEY_CATCH2_FETCH_CATCH2 "Automatically fetch the latest version of the Catch2 git repo" ON)
option(JUCEY_CATCH2_FETCH_JUCE "Automatically fetch the latest version of the JUCE git repo" OFF)
option(JUCEY_CATCH2_ADD_TEST_TARGETS "Add build targets for the tests" OFF)

project(jucey-catch2 VERSION 1.0.0 LANGUAGES CXX)

if(JUCEY_CATCH2_FETCH_CATCH2)
    message(CHECK_START "Fetching Catch2")
    include(cmake/fetch-catch2.cmake)
    message(CHECK_PASS "done")
endif()

if(JUCEY_CATCH2_FETCH_JUCE)
    message(CHECK_START "Fetching JUCE")
    include(cmake/fetch-juce.cmake)
    message(CHECK_PASS "done")
endif()

message(CHECK_START "Adding jucey-catch2 juce module targets")
add_subdirectory(modules)
message(CHECK_PASS "done")

if(JUCEY_CATCH2_ADD_TEST_TARGETS)
    message(CHECK_START "Adding jucey-catch2 test targets")
    add_subdirectory(tests)
    message(CHECK_PASS "done")
endif()
