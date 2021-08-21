cmake_minimum_required(VERSION 3.18)
project (ESFile)

SET(PROJECT_ROOT_PATH ${PROJECT_SOURCE_DIR})
SET(EXECUTABLE_OUTPUT_PATH "${PROJECT_SOURCE_DIR}/build")

include_directories(inc)
file(GLOB SOURCES "src/*.cpp")
# link_directories(lib)

add_executable(test ${SOURCES})

SET (LIB_SRC "inc/es_file.hpp")
ADD_LIBRARY (es_file SHARED ${LIB_SRC})    # 第一个参数为你需要构建的dll的名字，第二个为类型
SET_TARGET_PROPERTIES(es_file PROPERTIES LINKER_LANGUAGE CXX)
