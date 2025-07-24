# 拍照引导Agent

一个基于计算机视觉和AI的智能拍照引导系统，能够实时分析手机拍照画面并提供具体的拍摄建议。

## 功能特点

### 🎯 核心功能
- **实时图像分析**: 使用OpenCV分析图片的技术参数
- **智能拍摄指导**: 基于Minimax-01多模态模型提供具体的拍摄建议
- **摄影知识融合**: 整合多本专业手机摄影书籍的知识
- **React Native支持**: 提供专门的接口用于移动应用集成

### 🔍 技术分析能力
- **曝光分析**: 亮度、对比度、动态范围、直方图分析
- **构图分析**: 三分法、对称性、重心、线条检测
- **光线分析**: 光线方向、阴影、高光、色温估计
- **质量评估**: 清晰度、模糊度、噪点检测
- **颜色分析**: 色彩平衡、主导颜色提取

### 💡 智能指导
- **具体可执行的建议**: 不是理论，而是"向左移动2步"、"蹲下30cm"这样的具体指导
- **多维度优化**: 位置、角度、技术设置的全方位建议
- **场景适配**: 针对人像、风景、建筑等不同场景的专业建议

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 环境配置

1. 创建环境变量文件:
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，添加你的API密钥:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 基本使用

```python
from photo_guide_agent import PhotoGuideAgent

# 初始化agent
agent = PhotoGuideAgent(api_key="your_api_key")

# 分析图片并获取指导建议
guidance = agent.get_photo_guidance("your_photo.jpg")
print(guidance)
```

### React Native集成

```python
from photo_guide_agent import PhotoGuideAgent, ReactNativeInterface

agent = PhotoGuideAgent(api_key="your_api_key")
rn_interface = ReactNativeInterface(agent)

# 从base64分析图片
result = rn_interface.analyze_photo_from_base64(base64_image)
if result['success']:
    print(result['guidance'])

# 获取快速技巧
tips = rn_interface.get_quick_tips("portrait")
```

## 详细使用说明

### 1. 图像技术参数分析

系统会自动分析图片的各种技术参数：

```python
tech_params = agent.analyze_image_technical_params("photo.jpg")

# 基本信息
print(f"分辨率: {tech_params['basic_info']['width']} x {tech_params['basic_info']['height']}")
print(f"宽高比: {tech_params['basic_info']['aspect_ratio']}")

# 曝光信息
print(f"亮度: {tech_params['exposure']['brightness']}")
print(f"对比度: {tech_params['exposure']['contrast']}")

# 构图分析
print(f"主要兴趣区域: {tech_params['composition']['rule_of_thirds']['primary_interest']}")
print(f"重心位置: {tech_params['composition']['center_of_mass']}")

# 光线分析
print(f"光线方向: {tech_params['lighting']['direction']}")
print(f"色温: {tech_params['lighting']['color_temperature']}")
```

### 2. 拍摄指导格式

Agent会按照以下格式提供建议：

```
**即时建议：**
画面偏暗，主体不够突出

**位置调整：**
向前走2步，让主体在画面中更大

**角度调整：**
蹲下30cm，采用低角度仰拍

**技术设置：**
打开HDR模式，提升暗部细节
```

### 3. 配置定制

可以通过 `config.py` 调整各种参数：

```python
from config import get_config

config = get_config()

# 修改亮度阈值
config['image_analysis']['brightness_thresholds']['dark'] = 90

# 修改构图容差
config['image_analysis']['composition_config']['rule_of_thirds_tolerance'] = 60
```

## 摄影知识库

系统整合了以下专业摄影书籍的知识：

1. **拿起手机，人人都是摄影师** - 基础拍摄技巧
2. **小手机玩转大摄影** - 进阶构图方法
3. **手机影像学** - 技术原理与算法
4. **手机摄影技法** - 专业拍摄技巧
5. **拿起手机拍大片** - 创意拍摄方法

这些知识被智能地融入到Agent的分析和建议中，确保建议的专业性和实用性。

## API说明

### PhotoGuideAgent类

**主要方法：**

- `analyze_image_technical_params(image_path)`: 分析图片技术参数
- `get_photo_guidance(image_path)`: 获取完整的拍摄指导
- `batch_analyze_images(image_paths)`: 批量分析多张图片

### ReactNativeInterface类

**移动端友好的接口：**

- `analyze_photo_from_base64(base64_image)`: 从base64分析图片
- `get_quick_tips(scene_type)`: 获取快速拍摄技巧

### 支持的场景类型

- `general`: 通用拍摄
- `portrait`: 人像拍摄
- `landscape`: 风景拍摄
- `architecture`: 建筑拍摄

## 技术架构

```
用户拍照 → OpenCV图像分析 → 摄影知识匹配 → Minimax-01模型 → 具体指导建议
```

### 核心组件

1. **图像分析引擎**: 基于OpenCV的技术参数提取
2. **知识库系统**: 专业摄影书籍的结构化知识
3. **AI引导模型**: Minimax-01多模态大模型
4. **移动端接口**: React Native集成层

### 分析维度

- **曝光**: 亮度、对比度、直方图、动态范围
- **构图**: 三分法、对称性、重心、线条
- **光线**: 方向、阴影、高光、色温
- **质量**: 清晰度、模糊度、噪点
- **颜色**: 色彩平衡、主导色、饱和度

## 使用场景

### 1. 实时拍摄指导
在React Native应用中实时分析相机预览，提供即时的拍摄建议。

### 2. 照片后评估
分析已拍摄的照片，提供改进建议用于下次拍摄。

### 3. 摄影教学
作为摄影教学工具，帮助用户理解和改进拍摄技巧。

### 4. 批量图片优化
分析大量图片，统计拍摄习惯并提供系统性改进建议。

## 注意事项

1. **API密钥**: 需要有效的OpenRouter API密钥
2. **图片格式**: 支持JPG、JPEG、PNG格式
3. **图片大小**: 建议不超过10MB
4. **网络环境**: 需要稳定的网络连接调用AI模型

## 示例效果

输入一张光线不足、构图居中的照片，Agent可能会给出：

```
**即时建议：**
光线不足影响画质，主体居中显得平淡

**位置调整：**
向窗户方向移动1米，寻找更好的自然光

**角度调整：**
保持当前高度，手机略向左倾斜10度

**技术设置：**
开启夜景模式，使用三分法将主体放在右侧三分线上
```

## 开发者

该项目整合了专业摄影知识和现代AI技术，旨在让每个人都能拍出更好的照片。

## 许可证

请查看LICENSE文件了解详细信息。