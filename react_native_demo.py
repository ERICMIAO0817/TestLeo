#!/usr/bin/env python3
"""
React Native接口演示
展示如何在React Native应用中使用拍照引导Agent
"""

import json
import base64
from photo_guide_agent import PhotoGuideAgent, ReactNativeInterface

def demo_rn_interface():
    """演示React Native接口"""
    print("=" * 60)
    print("React Native 拍照引导Agent接口演示")
    print("=" * 60)
    
    # 初始化agent (在实际应用中需要真实的API密钥)
    agent = PhotoGuideAgent("dummy_key_for_demo")
    rn_interface = ReactNativeInterface(agent)
    
    # 演示1: 场景特定技巧
    print("\n1. 获取场景特定拍摄技巧")
    print("-" * 40)
    
    scene_types = ["人像", "风景", "美食", "建筑"]
    for scene in scene_types:
        tips = rn_interface.get_scene_specific_tips(scene)
        print(f"\n{scene}拍摄技巧:")
        for i, tip in enumerate(tips["tips"], 1):
            print(f"  {i}. {tip}")
    
    # 演示2: 模拟base64图片分析
    print("\n\n2. 模拟相机画面分析")
    print("-" * 40)
    
    # 创建测试图片并转换为base64
    import cv2
    import numpy as np
    import tempfile
    import os
    
    # 创建测试图片
    img = np.zeros((400, 600, 3), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (200, 200), (255, 255, 255), -1)
    cv2.circle(img, (400, 200), 60, (128, 128, 128), -1)
    cv2.line(img, (0, 300), (600, 300), (64, 64, 64), 2)
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        cv2.imwrite(temp_file.name, img)
        
        # 转换为base64
        with open(temp_file.name, 'rb') as f:
            image_data = f.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # 清理临时文件
        os.unlink(temp_file.name)
    
    # 分析图片
    print("分析模拟相机画面...")
    result = rn_interface.analyze_camera_frame(base64_image, "人像")
    
    print(f"分析结果:")
    print(f"  成功: {result['success']}")
    print(f"  场景类型: {result.get('scene_type', 'N/A')}")
    print(f"  建议数量: {len(result.get('suggestions', []))}")
    
    if result.get('suggestions'):
        print("\n拍摄建议:")
        for i, suggestion in enumerate(result['suggestions'][:5], 1):
            print(f"  {i}. [{suggestion['type']}] {suggestion['text']}")
    
    # 演示3: 技术参数展示
    if result.get('technical_analysis'):
        print("\n技术参数摘要:")
        tech = result['technical_analysis']
        
        if 'basic_info' in tech:
            basic = tech['basic_info']
            print(f"  分辨率: {basic['width']}x{basic['height']}")
            print(f"  宽高比: {basic['aspect_ratio']}")
        
        if 'exposure' in tech:
            exposure = tech['exposure']
            print(f"  平均亮度: {exposure['mean_brightness']:.1f}/255")
            print(f"  是否欠曝: {'是' if exposure['is_underexposed'] else '否'}")
        
        if 'quality' in tech:
            quality = tech['quality']
            print(f"  清晰度等级: {quality['sharpness_level']}")
    
    print("\n演示完成!")

def simulate_real_time_guidance():
    """模拟实时拍摄指导场景"""
    print("\n" + "=" * 60)
    print("模拟实时拍摄指导场景")
    print("=" * 60)
    
    agent = PhotoGuideAgent("dummy_key")
    rn_interface = ReactNativeInterface(agent)
    
    # 模拟不同的拍摄场景
    scenarios = [
        {
            "name": "光线不足的室内人像",
            "scene": "人像",
            "description": "模拟在室内光线不足的环境下拍摄人像"
        },
        {
            "name": "户外风景拍摄",
            "scene": "风景", 
            "description": "模拟在户外拍摄风景照片"
        },
        {
            "name": "美食近距离拍摄",
            "scene": "美食",
            "description": "模拟拍摄餐桌上的美食"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n场景: {scenario['name']}")
        print(f"描述: {scenario['description']}")
        print("-" * 40)
        
        # 获取该场景的拍摄技巧
        tips = rn_interface.get_scene_specific_tips(scenario['scene'])
        print("专业建议:")
        for tip in tips['tips']:
            print(f"  • {tip}")
        
        print()

def create_rn_integration_guide():
    """创建React Native集成指南"""
    guide = {
        "title": "拍照引导Agent - React Native集成指南",
        "description": "如何在React Native应用中集成拍照引导功能",
        "installation": {
            "dependencies": [
                "react-native-fs (文件系统访问)",
                "react-native-camera (相机功能)", 
                "react-native-image-picker (图片选择)",
                "@react-native-async-storage/async-storage (本地存储)"
            ],
            "python_backend": [
                "opencv-python>=4.8.0",
                "numpy>=1.24.0", 
                "openai>=1.0.0",
                "pillow>=10.0.0",
                "python-dotenv>=1.0.0"
            ]
        },
        "api_endpoints": {
            "analyze_frame": {
                "method": "POST",
                "url": "/api/analyze-frame",
                "payload": {
                    "image": "base64编码的图片数据",
                    "scene_type": "场景类型(人像/风景/美食/建筑等)"
                },
                "response": {
                    "success": True,
                    "technical_analysis": "技术参数分析",
                    "suggestions": [
                        {
                            "type": "建议类型",
                            "text": "具体建议内容",
                            "priority": "优先级(high/medium/low)"
                        }
                    ],
                    "scene_type": "场景类型",
                    "timestamp": "时间戳"
                }
            },
            "get_scene_tips": {
                "method": "GET", 
                "url": "/api/scene-tips/{scene_type}",
                "response": {
                    "scene_type": "场景类型",
                    "tips": ["技巧列表"],
                    "timestamp": "时间戳"
                }
            }
        },
        "usage_example": {
            "javascript": '''
// React Native 使用示例
import { captureImage, analyzeFrame } from './photoGuideService';

const PhotoGuideScreen = () => {
  const [suggestions, setSuggestions] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleCaptureAndAnalyze = async () => {
    try {
      setIsAnalyzing(true);
      
      // 捕获相机画面
      const base64Image = await captureImage();
      
      // 发送到后端分析
      const result = await analyzeFrame(base64Image, 'portrait');
      
      if (result.success) {
        setSuggestions(result.suggestions);
      }
    } catch (error) {
      console.error('分析失败:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <View>
      <Camera onCapture={handleCaptureAndAnalyze} />
      
      {suggestions.map((suggestion, index) => (
        <SuggestionCard 
          key={index}
          type={suggestion.type}
          text={suggestion.text}
          priority={suggestion.priority}
        />
      ))}
    </View>
  );
};
            '''
        },
        "best_practices": [
            "实时分析时控制调用频率，避免过度消耗API",
            "优先显示高优先级建议",
            "缓存场景特定技巧，减少网络请求",
            "提供离线基础建议功能",
            "优化图片压缩以减少传输时间",
            "添加用户反馈机制以改进建议质量"
        ]
    }
    
    with open("rn_integration_guide.json", "w", encoding="utf-8") as f:
        json.dump(guide, f, ensure_ascii=False, indent=2)
    
    print("React Native集成指南已保存到: rn_integration_guide.json")

if __name__ == "__main__":
    try:
        # 运行演示
        demo_rn_interface()
        simulate_real_time_guidance()
        create_rn_integration_guide()
        
        print("\n" + "=" * 60)
        print("✓ React Native接口演示完成！")
        print("✓ 集成指南已生成")
        print("=" * 60)
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()