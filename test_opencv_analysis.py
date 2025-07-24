#!/usr/bin/env python3
"""
测试OpenCV图像分析功能
不需要API密钥，仅测试本地图像处理能力
"""

import cv2
import numpy as np
import os
import json
from photo_guide_agent import PhotoGuideAgent

def create_test_image():
    """创建一个测试图片"""
    # 创建一个简单的测试图片
    img = np.zeros((600, 800, 3), dtype=np.uint8)
    
    # 添加一些几何形状
    cv2.rectangle(img, (100, 100), (300, 300), (255, 255, 255), -1)  # 白色矩形
    cv2.circle(img, (600, 200), 80, (128, 128, 128), -1)  # 灰色圆形
    cv2.line(img, (0, 400), (800, 400), (64, 64, 64), 3)  # 水平线
    cv2.line(img, (400, 0), (400, 600), (192, 192, 192), 2)  # 垂直线
    
    # 添加一些颜色区域
    cv2.rectangle(img, (500, 400), (700, 550), (0, 255, 0), -1)  # 绿色矩形
    cv2.ellipse(img, (200, 500), (80, 40), 45, 0, 360, (0, 0, 255), -1)  # 红色椭圆
    
    # 保存测试图片
    cv2.imwrite("test_image.jpg", img)
    print("已创建测试图片: test_image.jpg")
    
    return "test_image.jpg"

def test_image_analysis():
    """测试图像分析功能"""
    print("=" * 60)
    print("测试OpenCV图像分析功能")
    print("=" * 60)
    
    # 创建测试图片
    test_image_path = create_test_image()
    
    # 初始化agent (使用虚拟API密钥，仅用于本地分析)
    agent = PhotoGuideAgent("dummy_key")
    
    try:
        # 分析图片技术参数
        print("正在分析图片技术参数...")
        tech_params = agent.analyze_image_technical_params(test_image_path)
        
        # 详细显示分析结果
        print("\n" + "=" * 40)
        print("基本信息")
        print("=" * 40)
        basic = tech_params['basic_info']
        print(f"分辨率: {basic['width']} x {basic['height']}")
        print(f"宽高比: {basic['aspect_ratio']:.2f}")
        print(f"总像素: {basic['total_pixels']:,}")
        print(f"颜色通道: {basic['channels']}")
        
        print("\n" + "=" * 40)
        print("曝光分析")
        print("=" * 40)
        exposure = tech_params['exposure']
        print(f"平均亮度: {exposure['mean_brightness']:.1f} (0-255)")
        print(f"亮度标准差: {exposure['std_brightness']:.1f}")
        print(f"对比度: {exposure['contrast']:.1f}")
        print(f"动态范围: {exposure['dynamic_range']:.1f}")
        print(f"阴影区域占比: {exposure['shadows_percentage']:.1f}%")
        print(f"中间调占比: {exposure['midtones_percentage']:.1f}%")
        print(f"高光区域占比: {exposure['highlights_percentage']:.1f}%")
        print(f"峰值亮度: {exposure['peak_brightness']}")
        print(f"是否欠曝: {'是' if exposure['is_underexposed'] else '否'}")
        print(f"是否过曝: {'是' if exposure['is_overexposed'] else '否'}")
        
        print("\n" + "=" * 40)
        print("图像质量评估")
        print("=" * 40)
        quality = tech_params['quality']
        print(f"边缘密度: {quality['edge_density']:.4f}")
        print(f"模糊度评分: {quality['blur_score']:.1f}")
        print(f"噪点水平: {quality['noise_level']:.1f}")
        print(f"清晰度评分: {quality['sharpness_score']:.2f}")
        print(f"清晰度等级: {quality['sharpness_level']}")
        
        print("\n" + "=" * 40)
        print("颜色分析")
        print("=" * 40)
        color = tech_params['colors']
        print(f"红色通道均值: {color['red_channel_mean']:.1f}")
        print(f"绿色通道均值: {color['green_channel_mean']:.1f}")
        print(f"蓝色通道均值: {color['blue_channel_mean']:.1f}")
        print(f"主导颜色 RGB: {color['dominant_color_rgb']}")
        
        print("\n" + "=" * 40)
        print("光线分析")
        print("=" * 40)
        lighting = tech_params['lighting']
        print(f"光线方向: {lighting['light_direction']}")
        print(f"色温类型: {lighting['color_temperature']}")
        print(f"阴影区域比例: {lighting['shadow_percentage']:.1f}%")
        print(f"阴影区域数量: {lighting['shadow_regions']}")
        print(f"是否有强阴影: {'是' if lighting['has_strong_shadows'] else '否'}")
        print(f"高光区域比例: {lighting['highlight_percentage']:.1f}%")
        print(f"过曝区域比例: {lighting['overexposed_percentage']:.1f}%")
        print(f"是否有高光溢出: {'是' if lighting['has_highlight_clipping'] else '否'}")
        
        print("\n" + "=" * 40)
        print("构图分析")
        print("=" * 40)
        composition = tech_params['composition']
        print(f"视觉重心: ({composition['visual_center'][0]}, {composition['visual_center'][1]})")
        print(f"图像中心: {composition['image_center']}")
        
        # 重心偏移分析
        offset_x, offset_y = composition['center_offset']
        print(f"重心偏移: X轴{offset_x:+}像素, Y轴{offset_y:+}像素")
        
        print(f"主要兴趣区域: {composition['main_subject_area']}")
        print(f"最活跃区域: {composition['most_active_region']} (密度: {composition['most_active_density']:.4f})")
        
        print(f"检测到水平线: {composition['horizontal_lines']} 条")
        print(f"检测到垂直线: {composition['vertical_lines']} 条")
        print(f"是否有地平线: {'是' if composition['has_horizon'] else '否'}")
        
        print(f"垂直对称性: {composition['vertical_symmetry']:.2f}")
        print(f"水平对称性: {composition['horizontal_symmetry']:.2f}")
        print(f"是否对称构图: {'是' if composition['is_symmetric'] else '否'}")
        
        print("\n" + "=" * 40)
        print("摄影建议生成测试")
        print("=" * 40)
        
        # 基于分析结果生成建议
        suggestions = generate_suggestions(tech_params)
        for suggestion in suggestions:
            print(f"• {suggestion}")
        
        # 保存分析结果
        with open("analysis_result.json", "w", encoding="utf-8") as f:
            json.dump(tech_params, f, ensure_ascii=False, indent=2)
        print(f"\n分析结果已保存到: analysis_result.json")
        
        print("\n" + "=" * 60)
        print("✓ 图像分析测试完成！所有功能正常工作")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理测试文件
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
            print(f"已清理测试文件: {test_image_path}")

def generate_suggestions(tech_params):
    """基于技术参数生成建议"""
    suggestions = []
    
    # 亮度建议
    brightness = tech_params['exposure']['mean_brightness']
    if brightness < 100:
        suggestions.append("光线不足，建议寻找更亮的拍摄位置或开启夜景模式")
    elif brightness > 200:
        suggestions.append("光线过强，建议寻找阴影区域或调整拍摄角度")
    
    # 对比度建议
    contrast = tech_params['exposure']['contrast']
    if contrast < 30:
        suggestions.append("对比度较低，可以寻找明暗对比更强的场景")
    elif contrast > 80:
        suggestions.append("对比度过高，可能造成细节丢失")
    
    # 构图建议
    primary_interest = tech_params['composition']['main_subject_area']
    if primary_interest == 'middle_center':
        suggestions.append("主体居中，可以尝试用三分法构图增加动感")
    
    # 清晰度建议
    sharpness_level = tech_params['quality']['sharpness_level']
    if sharpness_level == "模糊":
        suggestions.append("图像模糊，请保持手机稳定或检查对焦")
    
    # 光线方向建议
    lighting_direction = tech_params['lighting']['light_direction']
    if lighting_direction == "顶光":
        suggestions.append("顶光容易产生难看阴影，建议改变拍摄时间或寻找侧光")
    
    # 色彩建议
    color_temp = tech_params['lighting']['color_temperature']
    if color_temp == "暖色调":
        suggestions.append("暖色调营造温馨氛围，适合人像和生活场景")
    elif color_temp == "冷色调":
        suggestions.append("冷色调适合表现科技感和静谧氛围")
    
    if not suggestions:
        suggestions.append("当前拍摄参数良好，可以继续拍摄")
    
    return suggestions

if __name__ == "__main__":
    test_image_analysis()