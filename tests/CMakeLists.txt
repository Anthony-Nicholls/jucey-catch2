juce_add_console_app(jucey-catch2-tests)

target_sources(jucey-catch2-tests
               PRIVATE source/InvokeOnMessageThreadAndWaitTests.cpp)

target_link_libraries(
  jucey-catch2-tests
  PRIVATE juce::juce_recommended_config_flags juce::juce_recommended_lto_flags
          juce::juce_recommended_warning_flags jucey::jucey_catch2_with_main)

target_compile_features(jucey-catch2-tests PRIVATE cxx_std_17)

target_compile_definitions(jucey-catch2-tests PRIVATE JUCE_USE_CURL=0)

set_property(GLOBAL PROPERTY CTEST_TARGETS_ADDED 1)

include(CTest)
include(Dart)
include(Catch)
catch_discover_tests(jucey-catch2-tests)
