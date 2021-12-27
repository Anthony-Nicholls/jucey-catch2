include(FetchContent)

FetchContent_Declare(
    catch2
    URL https://github.com/catchorg/Catch2/archive/refs/heads/devel.zip
)

FetchContent_MakeAvailable(catch2)
list(APPEND CMAKE_MODULE_PATH ${catch2_SOURCE_DIR}/extras)
