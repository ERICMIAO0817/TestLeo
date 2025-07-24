#!/usr/bin/env python3
"""
拍照引导Agent使用示例

演示如何使用PhotoGuideAgent进行实时拍照指导
"""

import os
import sys
import json
from photo_guide_agent import PhotoGuideAgent, ReactNativeInterface
from config import get_config, validate_config

def example_1_basic_usage():
    """示例1: 基本使用方法"""
    print("=" * 50)
    print("示例1: 基本使用方法")
    print("=" * 50)
    
    # 设置API密钥 (请替换为你的实际API密钥)
    api_key = os.getenv("OPENROUTER_API_KEY", "your_api_key_here")
    
    if api_key == "your_api_key_here":
        print("请设置环境变量 OPENROUTER_API_KEY 或在代码中替换API密钥")
        return
    
    # 初始化agent
    agent = PhotoGuideAgent(api_key)
    
    # 示例图片路径 (请替换为实际图片路径)
    image_path = "example_photo.jpg"
    
    if not os.path.exists(image_path):
        print(f"示例图片 {image_path} 不存在")
        print("请准备一张测试图片，或修改image_path变量")
        return
    
    try:
        # 分析图片技术参数
        print("正在分析图片技术参数...")
        tech_params = agent.analyze_image_technical_params(image_path)
        
        print("技术参数分析结果:")
        print(f"- 分辨率: {tech_params['basic_info']['width']} x {tech_params['basic_info']['height']}")
        print(f"- 亮度: {tech_params['exposure']['brightness']:.1f}")
        print(f"- 对比度: {tech_params['exposure']['contrast']:.1f}")
        print(f"- 清晰度评分: {tech_params['quality']['sharpness_score']:.2f}")
        print(f"- 光线方向: {tech_params['lighting']['direction']}")
        print(f"- 主要兴趣区域: {tech_params['composition']['rule_of_thirds']['primary_interest']}")
        
        # 获取拍照指导
        print("\n正在获取拍照指导建议...")
        guidance = agent.get_photo_guidance(image_path)
        
        print("拍照指导建议:")
        print(guidance)
        
    except Exception as e:
        print(f"出现错误: {e}")

def example_2_react_native_interface():
    """示例2: React Native接口使用"""
    print("\n" + "=" * 50)
    print("示例2: React Native接口使用")
    print("=" * 50)
    
    api_key = os.getenv("OPENROUTER_API_KEY", "your_api_key_here")
    
    if api_key == "your_api_key_here":
        print("请设置环境变量 OPENROUTER_API_KEY")
        return
    
    # 初始化agent和RN接口
    agent = PhotoGuideAgent(api_key)
    rn_interface = ReactNativeInterface(agent)
    
    # 获取快速技巧
    print("通用拍摄技巧:")
    general_tips = rn_interface.get_quick_tips("general")
    for i, tip in enumerate(general_tips, 1):
        print(f"{i}. {tip}")
    
    print("\n人像拍摄技巧:")
    portrait_tips = rn_interface.get_quick_tips("portrait")
    for i, tip in enumerate(portrait_tips, 1):
        print(f"{i}. {tip}")
    
    # 模拟从base64分析图片
    image_path = "example_photo.jpg"
    if os.path.exists(image_path):
        print(f"\n正在分析图片 {image_path}...")
        
        # 转换为base64
        import base64
        with open(image_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        
        # 分析
        result = rn_interface.analyze_photo_from_base64(base64_image)
        
        if result['success']:
            print("分析成功!")
            print("指导建议:")
            print(result['guidance'])
        else:
            print(f"分析失败: {result['error']}")

def example_3_batch_analysis():
    """示例3: 批量分析多张图片"""
    print("\n" + "=" * 50)
    print("示例3: 批量分析多张图片")
    print("=" * 50)
    
    api_key = os.getenv("OPENROUTER_API_KEY", "your_api_key_here")
    
    if api_key == "your_api_key_here":
        print("请设置环境变量 OPENROUTER_API_KEY")
        return
    
    # 初始化agent
    agent = PhotoGuideAgent(api_key)
    
    # 准备图片列表 (请替换为实际图片路径)
    image_paths = [
        "photo1.jpg",
        "photo2.jpg", 
        "photo3.jpg"
    ]
    
    # 过滤存在的图片
    existing_images = [path for path in image_paths if os.path.exists(path)]
    
    if not existing_images:
        print("没有找到测试图片")
        print("请准备一些测试图片，或修改image_paths列表")
        return
    
    print(f"正在批量分析 {len(existing_images)} 张图片...")
    
    # 批量分析
    results = agent.batch_analyze_images(existing_images)
    
    # 显示结果
    for i, result in enumerate(results, 1):
        print(f"\n图片 {i}: {result['image_path']}")
        if 'error' in result:
            print(f"错误: {result['error']}")
        else:
            print("指导建议:")
            print(result['guidance'])

def example_4_configuration_demo():
    """示例4: 配置演示"""
    print("\n" + "=" * 50)
    print("示例4: 配置演示")
    print("=" * 50)
    
    # 加载配置
    config = get_config()
    
    print("当前配置:")
    print(f"- API模型: {config['api']['model']}")
    print(f"- 最大tokens: {config['api']['max_tokens']}")
    print(f"- 温度参数: {config['api']['temperature']}")
    print(f"- 支持的图片格式: {config['react_native']['supported_formats']}")
    print(f"- 最大图片尺寸: {config['react_native']['max_image_size']}")
    
    # 验证配置
    print("\n验证配置...")
    if validate_config():
        print("✓ 配置验证通过")
    else:
        print("✗ 配置验证失败")
    
    # 显示阈值配置
    print("\n亮度阈值配置:")
    brightness_thresholds = config['image_analysis']['brightness_thresholds']
    for level, value in brightness_thresholds.items():
        print(f"  {level}: {value}")

def example_5_technical_analysis_only():
    """示例5: 仅进行技术分析（不调用API）"""
    print("\n" + "=" * 50)
    print("示例5: 仅进行技术分析")
    print("=" * 50)
    
    # 不需要API密钥，只进行本地分析
    agent = PhotoGuideAgent("dummy_key")
    
    image_path = "example_photo.jpg"
    
    if not os.path.exists(image_path):
        print(f"示例图片 {image_path} 不存在")
        return
    
    try:
        print(f"正在分析图片 {image_path}...")
        tech_params = agent.analyze_image_technical_params(image_path)
        
        # 详细显示分析结果
        print("\n=== 基本信息 ===")
        basic = tech_params['basic_info']
        print(f"分辨率: {basic['width']} x {basic['height']}")
        print(f"宽高比: {basic['aspect_ratio']:.2f}")
        print(f"总像素: {basic['resolution']:,}")
        
        print("\n=== 曝光分析 ===")
        exposure = tech_params['exposure']
        print(f"亮度: {exposure['brightness']:.1f}")
        print(f"对比度: {exposure['contrast']:.1f}")
        print(f"动态范围: {exposure['dynamic_range']:.1f}")
        
        hist = exposure['histogram_analysis']
        print(f"阴影比例: {hist['shadows_ratio']:.2%}")
        print(f"中间调比例: {hist['midtones_ratio']:.2%}")
        print(f"高光比例: {hist['highlights_ratio']:.2%}")
        print(f"是否欠曝: {hist['is_underexposed']}")
        print(f"是否过曝: {hist['is_overexposed']}")
        
        print("\n=== 图像质量 ===")
        quality = tech_params['quality']
        print(f"边缘密度: {quality['edge_density']:.4f}")
        print(f"模糊度: {quality['blur_score']:.1f}")
        print(f"噪点水平: {quality['noise_level']:.1f}")
        print(f"清晰度评分: {quality['sharpness_score']:.2f}")
        
        print("\n=== 颜色分析 ===")
        color = tech_params['color']
        print(f"红色均值: {color['red_mean']:.1f}")
        print(f"绿色均值: {color['green_mean']:.1f}")
        print(f"蓝色均值: {color['blue_mean']:.1f}")
        print(f"主导颜色 RGB: {color['dominant_color']}")
        
        print("\n=== 光线分析 ===")
        lighting = tech_params['lighting']
        print(f"光线方向: {lighting['direction']}")
        print(f"色温: {lighting['color_temperature']}")
        print(f"阴影比例: {lighting['shadows']['ratio']:.2%}")
        print(f"高光比例: {lighting['highlights']['ratio']:.2%}")
        print(f"是否有过曝: {lighting['highlights']['has_clipping']}")
        
        print("\n=== 构图分析 ===")
        composition = tech_params['composition']
        print(f"重心位置: ({composition['center_of_mass'][0]:.0f}, {composition['center_of_mass'][1]:.0f})")
        print(f"图像中心: {composition['image_center']}")
        print(f"主要兴趣区域: {composition['rule_of_thirds']['primary_interest']}")
        print(f"水平线数量: {composition['horizontal_lines']['count']}")
        print(f"垂直线数量: {composition['vertical_lines']['count']}")
        print(f"垂直对称性: {composition['symmetry']['vertical_symmetry']:.2f}")
        print(f"水平对称性: {composition['symmetry']['horizontal_symmetry']:.2f}")
        
    except Exception as e:
        print(f"分析出现错误: {e}")

def create_sample_config():
    """创建示例配置文件"""
    print("\n" + "=" * 50)
    print("创建示例配置文件")
    print("=" * 50)
    
    sample_env = """# 环境变量配置文件
# 将此文件重命名为 .env 并填入你的API密钥

# OpenRouter API密钥 (必需)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# 可选配置
DEBUG=False
LOG_LEVEL=INFO
"""
    
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(sample_env)
    
    print("已创建 .env.example 文件")
    print("请复制为 .env 并填入你的API密钥")

def main():
    """主函数"""
    print("拍照引导Agent使用示例")
    print("=" * 50)
    
    # 创建示例配置
    create_sample_config()
    
    # 运行所有示例
    example_4_configuration_demo()
    example_5_technical_analysis_only()
    example_2_react_native_interface()
    
    # 需要API密钥的示例
    if os.getenv("OPENROUTER_API_KEY") and os.getenv("OPENROUTER_API_KEY") != "your_api_key_here":
        example_1_basic_usage()
        example_3_batch_analysis()
    else:
        print("\n" + "=" * 50)
        print("提示: 设置 OPENROUTER_API_KEY 环境变量以运行完整示例")
        print("=" * 50)

if __name__ == "__main__":
    main()