cmake_minimum_required(VERSION 3.20)
project(FocusCef LANGUAGES CXX)

if(NOT DEFINED CEF_ROOT)
  message(FATAL_ERROR "Pass -DCEF_ROOT=C:/path/to/cef_binary")
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(FocusCef WIN32 main.cpp)
target_include_directories(FocusCef PRIVATE "${CEF_ROOT}")
target_link_directories(FocusCef PRIVATE "${CEF_ROOT}/Release")
target_link_libraries(FocusCef PRIVATE libcef)
target_compile_definitions(FocusCef PRIVATE UNICODE _UNICODE NOMINMAX)
add_custom_command(TARGET FocusCef POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy_if_different "${CEF_ROOT}/Release/libcef.dll" "$<TARGET_FILE_DIR:FocusCef>/libcef.dll")
