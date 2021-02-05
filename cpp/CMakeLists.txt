cmake_minimum_required(VERSION 3.18)
project (main)

SET(PROJECT_ROOT_PATH "${PROJECT_SOURCE_DIR}")
SET(EXECUTABLE_OUTPUT_PATH "${PROJECT_SOURCE_DIR}")
# SET(LIBRARY_OUTPUT_PATH "${PROJtotal_SOURCE_DIR}/.build_release/lib/")

include_directories(inc)
# include_directories(${PROJECT_SOURCE_DIR}/assimp)
# include_directories(${PROJECT_SOURCE_DIR})
# aux_source_directory(${PROJECT_SOURCE_DIR}/src src_dirs)
file(GLOB SOURCES "src/*.cpp")
link_directories(lib)
link_libraries(assimp-vc142-mt)

add_executable(main ${SOURCES})

target_link_libraries(main assimp-vc142-mt)
