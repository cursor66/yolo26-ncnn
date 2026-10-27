cmake_minimum_required(VERSION 3.10)

project(yolo26_ncnn CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(YOLO26_BUILD_SEG "Build YOLO26 segmentation demo" ON)
option(YOLO26_BUILD_TOOLS "Build helper tools" ON)

# 查找 OpenMP（必须，因为 ncnn 需要）
find_package(OpenMP REQUIRED)

# 查找 OpenCV
find_package(OpenCV REQUIRED)

# 包含目录
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/./
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    /ncnn/build/install/include/ncnn
)

# 链接目录（确保 glslang 库路径已包含）
link_directories(
    /ncnn/build/install/lib
    /usr/local/glslang/install/lib
    /usr/local/glslang/install/include
)

# 核心库 yolo26
add_library(yolo26
    src/yolo26.cpp
    src/yolo26_draw.cpp
    src/yolo26_preprocess.cpp
)

target_include_directories(yolo26
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# 链接 ncnn、OpenCV、glslang 和 OpenMP（PUBLIC 使依赖者也自动获得）
target_link_libraries(yolo26
    PUBLIC
        ncnn
        glslang
        ${OpenCV_LIBS}
        OpenMP::OpenMP_CXX
)

# 检测 demo
add_executable(yolo26_det src/yolo26_det.cpp)
target_link_libraries(yolo26_det yolo26)   # 依赖 yolo26，自动获得 glslang 等库

# 分割 demo（可选）
if(YOLO26_BUILD_SEG)
    target_sources(yolo26 PRIVATE src/yolo26_seg.cpp)

    add_executable(yolo26_seg_demo src/yolo26_seg_demo.cpp)
    target_link_libraries(yolo26_seg_demo yolo26)   # 依赖 yolo26，自动获得 glslang
endif()

# 工具（可选）
if(YOLO26_BUILD_TOOLS)
    add_executable(yolo26_topk_parity tools/topk_parity.cpp)
    target_include_directories(yolo26_topk_parity PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
    # 如果 topk_parity 使用了 ncnn，需显式链接 glslang（若未使用则无需）
    target_link_libraries(yolo26_topk_parity PRIVATE ncnn ${OpenCV_LIBS} OpenMP::OpenMP_CXX glslang)

    add_executable(yolo26_nms_parity tools/nms_parity.cpp)
    target_include_directories(yolo26_nms_parity PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
    target_link_libraries(yolo26_nms_parity PRIVATE ncnn ${OpenCV_LIBS} OpenMP::OpenMP_CXX glslang)

    add_executable(yolo26_mask_parity tools/mask_parity.cpp)
    target_include_directories(yolo26_mask_parity PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
    target_link_libraries(yolo26_mask_parity PRIVATE ncnn ${OpenCV_LIBS} OpenMP::OpenMP_CXX glslang)
endif()