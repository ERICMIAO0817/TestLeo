# 配置文件
import os
from typing import Dict, Any

# API 配置
API_CONFIG = {
    "openrouter_api_key": os.getenv("OPENROUTER_API_KEY", ""),
    "base_url": "https://openrouter.ai/api/v1",
    "model": "minimax/minimax-01",
    "max_tokens": 1000,
    "temperature": 0.7
}

# 图像分析参数配置
IMAGE_ANALYSIS_CONFIG = {
    # 亮度阈值
    "brightness_thresholds": {
        "very_dark": 50,
        "dark": 100,
        "normal_low": 120,
        "normal_high": 180,
        "bright": 200,
        "very_bright": 220
    },
    
    # 对比度阈值
    "contrast_thresholds": {
        "very_low": 20,
        "low": 40,
        "normal": 60,
        "high": 80,
        "very_high": 100
    },
    
    # 模糊度阈值
    "blur_thresholds": {
        "very_blurry": 100,
        "blurry": 300,
        "acceptable": 800,
        "sharp": 1500,
        "very_sharp": 3000
    },
    
    # 噪点阈值
    "noise_thresholds": {
        "very_low": 5,
        "low": 10,
        "moderate": 15,
        "high": 20,
        "very_high": 30
    },
    
    # 曝光分析阈值
    "exposure_thresholds": {
        "underexposed_shadows": 0.6,
        "overexposed_highlights": 0.4,
        "clipping_threshold": 0.02
    },
    
    # 构图分析参数
    "composition_config": {
        "rule_of_thirds_tolerance": 50,  # 像素
        "symmetry_threshold": 0.7,
        "line_detection": {
            "threshold": 100,
            "min_line_length": 100,
            "max_line_gap": 10,
            "horizontal_angle_tolerance": 10,
            "vertical_angle_range": (80, 100)
        }
    }
}

# 摄影指导语言配置
GUIDANCE_LANGUAGE_CONFIG = {
    "movement_instructions": {
        "forward": ["向前走", "往前移动", "靠近一点"],
        "backward": ["向后退", "往后移动", "退远一点"],
        "left": ["向左移动", "往左走", "左移"],
        "right": ["向右移动", "往右走", "右移"],
        "up": ["抬高手机", "向上移动", "举高一点"],
        "down": ["降低手机", "向下移动", "放低一点"]
    },
    
    "angle_instructions": {
        "tilt_up": ["仰拍", "向上倾斜", "抬高角度"],
        "tilt_down": ["俯拍", "向下倾斜", "降低角度"],
        "rotate_left": ["向左旋转", "逆时针旋转"],
        "rotate_right": ["向右旋转", "顺时针旋转"],
        "squat": ["蹲下拍摄", "降低身体", "蹲低一点"],
        "stand": ["站起来拍摄", "抬高身体", "站高一点"]
    },
    
    "distance_references": {
        "very_close": "5-10cm",
        "close": "30-50cm", 
        "normal": "1-2米",
        "far": "3-5米",
        "very_far": "5米以上"
    },
    
    "angle_references": {
        "slight": "10-15度",
        "moderate": "20-30度", 
        "significant": "45度",
        "steep": "60度以上"
    }
}

# React Native 接口配置
REACT_NATIVE_CONFIG = {
    "max_image_size": 2048,  # 最大图片尺寸
    "jpeg_quality": 90,
    "response_timeout": 30,  # 秒
    "retry_attempts": 3,
    "supported_formats": ["jpeg", "jpg", "png"],
    "max_base64_size": 10 * 1024 * 1024  # 10MB
}

# 摄影知识库配置
PHOTOGRAPHY_KNOWLEDGE_CONFIG = {
    "book_files": [
        "拿起手机，人人都是摄影师.json",
        "小手机玩转大摄影.json",
        "手机影像学.json", 
        "手机摄影技法.json",
        "拿起手机拍大片.json"
    ],
    
    # 知识提取关键词
    "keywords": {
        "lighting": ["光线", "光影", "顶光", "侧光", "逆光", "顺光", "阴影", "高光"],
        "composition": ["构图", "三分法", "对称", "留白", "框架", "引导线", "重心"],
        "movement": ["移动", "位置", "角度", "距离", "蹲下", "站立", "仰拍", "俯拍"],
        "technical": ["曝光", "对比度", "清晰度", "模糊", "噪点", "白平衡", "色彩"],
        "scenarios": ["人像", "风景", "建筑", "街拍", "夜景", "逆光", "室内", "户外"]
    }
}

# 错误处理配置
ERROR_HANDLING_CONFIG = {
    "max_retries": 3,
    "retry_delay": 1,  # 秒
    "timeout": 30,
    "fallback_responses": {
        "analysis_failed": "图片分析失败，请检查图片质量后重试",
        "api_error": "网络连接失败，请稍后重试",
        "invalid_image": "无法识别的图片格式，请使用JPG或PNG格式",
        "file_too_large": "图片文件过大，请压缩后重试"
    }
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "photo_guide_agent.log",
    "max_file_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

def get_config() -> Dict[str, Any]:
    """获取完整配置"""
    return {
        "api": API_CONFIG,
        "image_analysis": IMAGE_ANALYSIS_CONFIG,
        "guidance_language": GUIDANCE_LANGUAGE_CONFIG,
        "react_native": REACT_NATIVE_CONFIG,
        "photography_knowledge": PHOTOGRAPHY_KNOWLEDGE_CONFIG,
        "error_handling": ERROR_HANDLING_CONFIG,
        "logging": LOGGING_CONFIG
    }

def validate_config() -> bool:
    """验证配置有效性"""
    if not API_CONFIG["openrouter_api_key"]:
        print("警告: 未设置 OPENROUTER_API_KEY 环境变量")
        return False
    
    # 检查摄影书籍文件
    missing_books = []
    for book_file in PHOTOGRAPHY_KNOWLEDGE_CONFIG["book_files"]:
        if not os.path.exists(book_file):
            missing_books.append(book_file)
    
    if missing_books:
        print(f"警告: 缺少摄影书籍文件: {missing_books}")
    
    return True

if __name__ == "__main__":
    config = get_config()
    print("配置文件加载完成")
    print(f"API模型: {config['api']['model']}")
    print(f"支持的图片格式: {config['react_native']['supported_formats']}")
    
    if validate_config():
        print("配置验证通过")
    else:
        print("配置验证失败，请检查设置")