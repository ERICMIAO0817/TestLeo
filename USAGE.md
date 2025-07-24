# 拍照引导Agent使用指南

## 项目概述

这是一个基于计算机视觉和AI的智能拍照引导系统，能够：

- **实时分析手机拍照画面**的技术参数（曝光、构图、光线、清晰度等）
- **提供具体可执行的拍摄建议**（如"向左2步"、"蹲下30cm"、"手机倾斜15度"）
- **融合专业摄影知识**，基于摄影书籍内容进行domain-specific指导
- **支持React Native集成**，适用于移动应用开发

## 核心特性

### 🔍 图像技术分析
- **曝光分析**: 亮度分布、动态范围、欠曝/过曝检测
- **构图分析**: 三分法、对称性、视觉重心、线条检测  
- **光线分析**: 光线方向、色温、阴影/高光分布
- **质量评估**: 清晰度、模糊度、噪点水平
- **颜色分析**: 色彩平衡、主导颜色提取

### 💡 智能拍摄指导
- **位置调整**: "向左移动2步"、"前进1米"、"蹲下30cm"
- **角度调整**: "手机向上倾斜15度"、"逆时针旋转45度"、"仰拍30度角"
- **技术设置**: "开启人像模式"、"调整曝光+1档"、"使用夜景模式"
- **构图优化**: "将主体移至右侧三分线"、"保持地平线水平"

### 📚 摄影知识融合
- 基于《拿起手机，人人都是摄影师》等专业书籍
- 针对不同场景（人像/风景/美食/建筑）的专业建议
- 避免理论化，专注具体可操作的指导

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\\Scripts\\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置API密钥

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入你的OpenRouter API密钥
OPENROUTER_API_KEY=your_actual_api_key_here
```

### 3. 基本使用

```python
from photo_guide_agent import PhotoGuideAgent

# 初始化agent
agent = PhotoGuideAgent(api_key="your_openrouter_api_key")

# 分析图片并获取指导
guidance = agent.generate_guidance(
    image_path="your_photo.jpg",
    scene_type="人像",
    user_intent="拍摄证件照"
)

# 打印建议
for suggestion in guidance['basic_suggestions']:
    print(f"• {suggestion}")
```

### 4. React Native集成

```python
from photo_guide_agent import PhotoGuideAgent, ReactNativeInterface

# 初始化接口
agent = PhotoGuideAgent("your_api_key")
rn_interface = ReactNativeInterface(agent)

# 分析base64图片
result = rn_interface.analyze_camera_frame(
    base64_image=base64_data,
    scene_type="人像"
)

# 获取场景技巧
tips = rn_interface.get_scene_specific_tips("风景")
```

## 测试和演示

### 运行图像分析测试
```bash
source venv/bin/activate
python test_opencv_analysis.py
```

### 运行React Native演示
```bash
source venv/bin/activate  
python react_native_demo.py
```

### 查看示例使用
```bash
source venv/bin/activate
python example_usage.py
```

## API接口说明

### PhotoGuideAgent 类

#### `analyze_image_technical_params(image_path)`
分析图片的技术参数

**返回格式:**
```json
{
  "basic_info": {
    "width": 800,
    "height": 600,
    "aspect_ratio": 1.33,
    "total_pixels": 480000,
    "channels": 3
  },
  "exposure": {
    "mean_brightness": 120.5,
    "contrast": 65.2,
    "is_underexposed": false,
    "shadows_percentage": 25.3
  },
  "quality": {
    "sharpness_level": "清晰",
    "blur_score": 1250.8,
    "noise_level": 8.2
  },
  "lighting": {
    "light_direction": "左侧光",
    "color_temperature": "暖色调",
    "has_strong_shadows": true
  },
  "composition": {
    "main_subject_area": "middle_center",
    "visual_center": [400, 300],
    "has_horizon": true,
    "is_symmetric": false
  }
}
```

#### `generate_guidance(image_path, scene_type, user_intent)`
生成完整的拍摄指导建议

**参数:**
- `image_path`: 图片文件路径
- `scene_type`: 场景类型（"人像"/"风景"/"美食"/"建筑"/"通用"）
- `user_intent`: 用户拍摄意图（可选）

**返回格式:**
```json
{
  "technical_analysis": {...},
  "basic_suggestions": [
    "光线不足，建议寻找更亮的拍摄位置",
    "主体偏左，建议向右移动2步"
  ],
  "ai_suggestions": {
    "position_adjustments": ["向前走1步", "蹲下30cm"],
    "angle_adjustments": ["手机向上倾斜15度"],
    "technical_settings": ["开启人像模式"],
    "composition_tips": ["将主体放在右侧三分线上"]
  },
  "scene_type": "人像",
  "timestamp": "2024-01-15T10:30:00"
}
```

### ReactNativeInterface 类

#### `analyze_camera_frame(base64_image, scene_type)`
分析React Native传来的base64图片

#### `get_scene_specific_tips(scene_type)`
获取特定场景的拍摄技巧

## 场景类型说明

### 人像拍摄
- 重点关注眼部对焦
- 优化面部光线
- 背景虚化效果
- 避免不当角度

### 风景拍摄  
- 三分法构图
- 地平线水平对齐
- 前中后景层次
- 黄金时间光线

### 美食拍摄
- 45度俯拍角度
- 色彩搭配协调
- 自然光线利用
- 道具层次感

### 建筑拍摄
- 透视线条控制
- 对称性构图
- 独特视角寻找
- 光影效果利用

## 技术参数详解

### 曝光分析
- **平均亮度**: 0-255范围，120-180为正常
- **动态范围**: 画面最亮和最暗区域的差值
- **阴影/中间调/高光比例**: 亮度分布统计
- **欠曝/过曝检测**: 自动判断曝光问题

### 构图分析
- **视觉重心**: 基于图像内容计算的兴趣中心
- **三分法分析**: 九宫格区域活跃度
- **线条检测**: 水平线、垂直线数量和位置
- **对称性**: 水平和垂直对称度评分

### 光线分析
- **光线方向**: 顶光/侧光/底光/均匀光
- **色温估计**: 暖色调/冷色调/中性色调
- **阴影分析**: 阴影区域分布和强度
- **高光检测**: 过曝区域识别

## 常见问题

### Q: API调用失败怎么办？
A: 检查API密钥是否正确设置，网络连接是否正常，API额度是否充足。

### Q: 图片分析速度较慢？
A: 可以压缩图片尺寸，推荐1024x768以下；或使用较快的硬件。

### Q: 建议不够准确？
A: 确保场景类型选择正确，可以添加用户意图描述来提高准确性。

### Q: 如何添加新的场景类型？
A: 在`ReactNativeInterface.get_scene_specific_tips()`中添加新的场景和对应技巧。

## 开发和扩展

### 添加新的图像分析功能
在`PhotoGuideAgent._analyze_*`方法中添加新的分析算法

### 扩展摄影知识库
将新的摄影书籍内容转换为JSON格式，放在项目根目录

### 自定义建议生成
修改`_generate_basic_suggestions`方法来添加自定义规则

### 优化AI提示词
编辑`_build_guidance_prompt`方法来改进AI建议质量

## 项目文件结构

```
├── photo_guide_agent.py          # 核心Agent类
├── config.py                     # 配置文件
├── test_opencv_analysis.py       # OpenCV测试脚本
├── react_native_demo.py          # React Native演示
├── example_usage.py              # 使用示例
├── requirements.txt              # Python依赖
├── .env.example                  # 环境变量模板
├── README.md                     # 项目说明
├── USAGE.md                      # 使用指南
└── 摄影书籍JSON文件/             # 摄影知识库
```

## 注意事项

1. **API密钥安全**: 不要将真实API密钥提交到代码仓库
2. **图片隐私**: 注意用户图片数据的隐私保护
3. **性能优化**: 大量使用时考虑缓存和批处理
4. **错误处理**: 网络异常和API限制的优雅处理
5. **用户体验**: 提供加载状态和失败重试机制

## 支持和贡献

如遇到问题或有改进建议，欢迎提交Issue或Pull Request。

---

**版本**: 1.0.0  
**最后更新**: 2024年1月