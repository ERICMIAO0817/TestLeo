import cv2
import numpy as np
import json
import base64
import os
from typing import Dict, List, Tuple, Any, Union
import openai
from datetime import datetime
import logging

class PhotoGuideAgent:
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        """
        初始化拍照引导Agent
        
        Args:
            api_key: OpenRouter API密钥
            base_url: OpenRouter API地址
        """
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = "minimax/minimax-01"
        
        # 加载摄影知识库
        self.photography_knowledge = self._load_photography_books()
    
    def _load_photography_books(self) -> Dict[str, Any]:
        """加载摄影书籍知识库"""
        knowledge = {}
        
        json_files = [
            "拿起手机，人人都是摄影师.json",
            "手机摄影技法.json"
        ]
        
        for filename in json_files:
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        knowledge[filename] = json.load(f)
                    self.logger.info(f"已加载摄影知识: {filename}")
                except Exception as e:
                    self.logger.warning(f"无法加载 {filename}: {e}")
        
        return knowledge
    
    def _json_serializable(self, obj):
        """确保对象可以JSON序列化"""
        if isinstance(obj, dict):
            return {k: self._json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._json_serializable(item) for item in obj]
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bool):
            return bool(obj)
        elif obj is None:
            return None
        else:
            return obj
    
    def analyze_image_technical_params(self, image_path: str) -> Dict[str, Any]:
        """
        分析图片的技术参数
        
        Args:
            image_path: 图片路径
            
        Returns:
            包含技术参数的字典
        """
        try:
            # 读取图片
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"无法读取图片: {image_path}")
            
            # 基本信息
            height, width, channels = img.shape
            
            # 转换为灰度图进行分析
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # 1. 曝光分析
            exposure_analysis = self._analyze_exposure(gray)
            
            # 2. 图像质量评估
            quality_analysis = self._analyze_image_quality(gray)
            
            # 3. 颜色分析
            color_analysis = self._analyze_colors(img)
            
            # 4. 光线分析
            lighting_analysis = self._analyze_lighting(gray, img)
            
            # 5. 构图分析
            composition_analysis = self._analyze_composition(gray)
            
            # 整合所有分析结果
            tech_params = {
                "basic_info": {
                    "width": width,
                    "height": height,
                    "aspect_ratio": round(width / height, 2),
                    "total_pixels": width * height,
                    "channels": channels
                },
                "exposure": exposure_analysis,
                "quality": quality_analysis,
                "colors": color_analysis,
                "lighting": lighting_analysis,
                "composition": composition_analysis,
                "timestamp": datetime.now().isoformat()
            }
            
            return self._json_serializable(tech_params)
            
        except Exception as e:
            self.logger.error(f"图片分析失败: {e}")
            return {"error": str(e)}
    
    def _analyze_exposure(self, gray_img: np.ndarray) -> Dict[str, Any]:
        """分析曝光信息"""
        # 计算直方图
        hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
        
        # 基本统计
        mean_brightness = np.mean(gray_img)
        std_brightness = np.std(gray_img)
        min_val, max_val, _, _ = cv2.minMaxLoc(gray_img)
        
        # 动态范围
        dynamic_range = max_val - min_val
        
        # 分析亮度分布
        total_pixels = gray_img.shape[0] * gray_img.shape[1]
        shadows = np.sum(hist[:85]) / total_pixels * 100  # 0-85
        midtones = np.sum(hist[85:170]) / total_pixels * 100  # 85-170
        highlights = np.sum(hist[170:]) / total_pixels * 100  # 170-255
        
        # 找到峰值亮度
        peak_brightness = np.argmax(hist)
        
        # 判断曝光状态
        is_underexposed = mean_brightness < 100
        is_overexposed = mean_brightness > 200 and highlights > 20
        
        return {
            "mean_brightness": round(mean_brightness, 1),
            "std_brightness": round(std_brightness, 1),
            "contrast": round(std_brightness, 1),  # 标准差作为对比度指标
            "dynamic_range": float(dynamic_range),
            "shadows_percentage": round(shadows, 1),
            "midtones_percentage": round(midtones, 1),
            "highlights_percentage": round(highlights, 1),
            "peak_brightness": int(peak_brightness),
            "is_underexposed": bool(is_underexposed),
            "is_overexposed": bool(is_overexposed),
            "min_value": int(min_val),
            "max_value": int(max_val)
        }
    
    def _analyze_image_quality(self, gray_img: np.ndarray) -> Dict[str, Any]:
        """分析图像质量"""
        # 计算拉普拉斯算子用于评估清晰度
        laplacian = cv2.Laplacian(gray_img, cv2.CV_64F)
        laplacian_var = laplacian.var()
        
        # 边缘检测评估清晰度
        edges = cv2.Canny(gray_img, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # 噪点评估 (使用高斯模糊后的差异)
        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
        noise_level = np.std(gray_img.astype(float) - blurred.astype(float))
        
        # 评估清晰度等级
        if laplacian_var > 1000:
            sharpness_level = "非常清晰"
        elif laplacian_var > 500:
            sharpness_level = "清晰"
        elif laplacian_var > 200:
            sharpness_level = "一般"
        else:
            sharpness_level = "模糊"
        
        return {
            "edge_density": round(edge_density, 4),
            "blur_score": round(laplacian_var, 1),
            "noise_level": round(noise_level, 1),
            "sharpness_score": round(edge_density * 100, 2),
            "sharpness_level": sharpness_level
        }
    
    def _analyze_colors(self, img: np.ndarray) -> Dict[str, Any]:
        """分析颜色信息"""
        # 计算各通道均值
        b_mean = np.mean(img[:, :, 0])
        g_mean = np.mean(img[:, :, 1])
        r_mean = np.mean(img[:, :, 2])
        
        # 找到主导颜色 (简化版本)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pixels = img_rgb.reshape(-1, 3)
        
        # 使用KMeans找主导颜色 (简化为取均值)
        dominant_color = np.mean(pixels, axis=0).astype(int)
        
        return {
            "red_channel_mean": round(r_mean, 1),
            "green_channel_mean": round(g_mean, 1),
            "blue_channel_mean": round(b_mean, 1),
            "dominant_color_rgb": dominant_color.tolist()
        }
    
    def _analyze_lighting(self, gray_img: np.ndarray, img: np.ndarray) -> Dict[str, Any]:
        """分析光线条件"""
        height, width = gray_img.shape
        
        # 分析光线方向 (比较图像不同区域的亮度)
        left_brightness = np.mean(gray_img[:, :width//3])
        center_brightness = np.mean(gray_img[:, width//3:2*width//3])
        right_brightness = np.mean(gray_img[:, 2*width//3:])
        
        top_brightness = np.mean(gray_img[:height//3, :])
        bottom_brightness = np.mean(gray_img[2*height//3:, :])
        
        # 判断光线方向
        if left_brightness > center_brightness and left_brightness > right_brightness:
            light_direction = "左侧光"
        elif right_brightness > center_brightness and right_brightness > left_brightness:
            light_direction = "右侧光"
        elif top_brightness > bottom_brightness:
            light_direction = "顶光"
        elif bottom_brightness > top_brightness:
            light_direction = "底光"
        else:
            light_direction = "均匀光"
        
        # 色温分析 (简化版)
        b_mean = np.mean(img[:, :, 0])
        r_mean = np.mean(img[:, :, 2])
        
        if r_mean > b_mean + 20:
            color_temperature = "暖色调"
        elif b_mean > r_mean + 20:
            color_temperature = "冷色调"
        else:
            color_temperature = "中性色调"
        
        # 阴影分析
        shadow_threshold = 80
        shadow_mask = gray_img < shadow_threshold
        shadow_percentage = np.sum(shadow_mask) / gray_img.size * 100
        
        # 高光分析
        highlight_threshold = 200
        highlight_mask = gray_img > highlight_threshold
        highlight_percentage = np.sum(highlight_mask) / gray_img.size * 100
        
        # 检测阴影区域
        contours, _ = cv2.findContours(shadow_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        shadow_regions = len([c for c in contours if cv2.contourArea(c) > 100])
        
        # 过曝区域
        overexposed_mask = gray_img > 245
        overexposed_percentage = np.sum(overexposed_mask) / gray_img.size * 100
        
        return {
            "light_direction": light_direction,
            "color_temperature": color_temperature,
            "shadow_percentage": round(shadow_percentage, 1),
            "shadow_regions": int(shadow_regions),
            "has_strong_shadows": bool(shadow_percentage > 15),
            "highlight_percentage": round(highlight_percentage, 1),
            "overexposed_percentage": round(overexposed_percentage, 1),
            "has_highlight_clipping": bool(overexposed_percentage > 5)
        }
    
    def _analyze_composition(self, gray_img: np.ndarray) -> Dict[str, Any]:
        """分析构图"""
        height, width = gray_img.shape
        
        # 计算视觉重心
        moments = cv2.moments(gray_img)
        if moments['m00'] != 0:
            center_x = int(moments['m10'] / moments['m00'])
            center_y = int(moments['m01'] / moments['m00'])
        else:
            center_x, center_y = width // 2, height // 2
        
        # 图像中心
        image_center_x, image_center_y = width // 2, height // 2
        
        # 重心偏移
        offset_x = center_x - image_center_x
        offset_y = center_y - image_center_y
        
        # 三分法分析
        third_x = width // 3
        third_y = height // 3
        
        # 判断主体位置
        if center_x < third_x:
            horizontal_position = "left"
        elif center_x > 2 * third_x:
            horizontal_position = "right"
        else:
            horizontal_position = "center"
        
        if center_y < third_y:
            vertical_position = "top"
        elif center_y > 2 * third_y:
            vertical_position = "bottom"
        else:
            vertical_position = "middle"
        
        main_subject_area = f"{vertical_position}_{horizontal_position}"
        
        # 活跃区域分析 (使用边缘密度)
        regions = {}
        for i, v_pos in enumerate(["top", "middle", "bottom"]):
            for j, h_pos in enumerate(["left", "center", "right"]):
                y_start = i * third_y
                y_end = (i + 1) * third_y if i < 2 else height
                x_start = j * third_x
                x_end = (j + 1) * third_x if j < 2 else width
                
                region = gray_img[y_start:y_end, x_start:x_end]
                edges = cv2.Canny(region, 50, 150)
                edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
                regions[f"{v_pos}_{h_pos}"] = edge_density
        
        most_active_region = max(regions, key=regions.get)
        most_active_density = regions[most_active_region]
        
        # 线条检测
        edges = cv2.Canny(gray_img, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        horizontal_lines = 0
        vertical_lines = 0
        
        if lines is not None:
            for line in lines:
                rho, theta = line[0]
                angle = theta * 180 / np.pi
                
                if 80 <= angle <= 100 or -10 <= angle <= 10:  # 水平线
                    horizontal_lines += 1
                elif 170 <= angle <= 180 or 0 <= angle <= 10:  # 垂直线
                    vertical_lines += 1
        
        # 地平线检测
        has_horizon = horizontal_lines > 0
        
        # 对称性分析
        left_half = gray_img[:, :width//2]
        right_half = cv2.flip(gray_img[:, width//2:], 1)
        
        # 确保两半大小相同
        min_width = min(left_half.shape[1], right_half.shape[1])
        left_half = left_half[:, :min_width]
        right_half = right_half[:, :min_width]
        
        horizontal_symmetry = cv2.matchTemplate(left_half, right_half, cv2.TM_CCOEFF_NORMED)[0][0]
        
        top_half = gray_img[:height//2, :]
        bottom_half = cv2.flip(gray_img[height//2:, :], 0)
        
        min_height = min(top_half.shape[0], bottom_half.shape[0])
        top_half = top_half[:min_height, :]
        bottom_half = bottom_half[:min_height, :]
        
        vertical_symmetry = cv2.matchTemplate(top_half, bottom_half, cv2.TM_CCOEFF_NORMED)[0][0]
        
        is_symmetric = horizontal_symmetry > 0.7 or vertical_symmetry > 0.7
        
        return {
            "visual_center": [int(center_x), int(center_y)],
            "image_center": [int(image_center_x), int(image_center_y)],
            "center_offset": [int(offset_x), int(offset_y)],
            "main_subject_area": main_subject_area,
            "most_active_region": most_active_region,
            "most_active_density": round(most_active_density, 4),
            "horizontal_lines": int(horizontal_lines),
            "vertical_lines": int(vertical_lines),
            "has_horizon": bool(has_horizon),
            "vertical_symmetry": round(float(vertical_symmetry), 2),
            "horizontal_symmetry": round(float(horizontal_symmetry), 2),
            "is_symmetric": bool(is_symmetric)
        }
    
    def generate_guidance(self, image_path: str, scene_type: str = "通用", user_intent: str = "") -> Dict[str, Any]:
        """
        生成拍摄指导建议
        
        Args:
            image_path: 图片路径
            scene_type: 场景类型 (人像/风景/建筑/美食等)
            user_intent: 用户拍摄意图
            
        Returns:
            包含具体指导建议的字典
        """
        try:
            # 1. 分析技术参数
            tech_params = self.analyze_image_technical_params(image_path)
            
            if "error" in tech_params:
                return tech_params
            
            # 2. 生成基础建议
            basic_suggestions = self._generate_basic_suggestions(tech_params)
            
            # 3. 调用AI模型生成专业建议
            ai_suggestions = self._generate_ai_suggestions(image_path, tech_params, scene_type, user_intent)
            
            # 4. 整合所有建议
            guidance = {
                "technical_analysis": tech_params,
                "basic_suggestions": basic_suggestions,
                "ai_suggestions": ai_suggestions,
                "scene_type": scene_type,
                "user_intent": user_intent,
                "timestamp": datetime.now().isoformat()
            }
            
            return self._json_serializable(guidance)
            
        except Exception as e:
            self.logger.error(f"生成指导建议失败: {e}")
            return {"error": str(e)}
    
    def _generate_basic_suggestions(self, tech_params: Dict[str, Any]) -> List[str]:
        """基于技术参数生成基础建议"""
        suggestions = []
        
        # 曝光建议
        exposure = tech_params.get("exposure", {})
        if exposure.get("is_underexposed"):
            suggestions.append("光线不足，建议寻找更亮的拍摄位置或开启夜景模式")
        elif exposure.get("is_overexposed"):
            suggestions.append("画面过亮，建议降低曝光或寻找阴影区域拍摄")
        
        if exposure.get("shadows_percentage", 0) > 30:
            suggestions.append("阴影过多，尝试改变拍摄角度或补充光线")
        
        # 构图建议
        composition = tech_params.get("composition", {})
        if composition.get("main_subject_area") == "middle_center":
            suggestions.append("主体居中，可以尝试用三分法构图增加动感")
        
        offset = composition.get("center_offset", [0, 0])
        if abs(offset[0]) > 50:
            direction = "左" if offset[0] > 0 else "右"
            steps = abs(offset[0]) // 20
            suggestions.append(f"主体偏{direction}，建议向{'右' if offset[0] > 0 else '左'}移动{steps}步")
        
        # 清晰度建议
        quality = tech_params.get("quality", {})
        if quality.get("sharpness_level") == "模糊":
            suggestions.append("图像模糊，请保持手机稳定或检查对焦")
        elif quality.get("noise_level", 0) > 10:
            suggestions.append("噪点较多，建议在光线更好的环境拍摄")
        
        # 光线建议
        lighting = tech_params.get("lighting", {})
        if lighting.get("light_direction") in ["顶光", "底光"]:
            suggestions.append("光线角度不佳，尝试侧面光源")
        
        return suggestions
    
    def _generate_ai_suggestions(self, image_path: str, tech_params: Dict[str, Any], scene_type: str, user_intent: str) -> Dict[str, Any]:
        """使用AI模型生成专业建议"""
        try:
            # 编码图片为base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # 构建提示词
            prompt = self._build_guidance_prompt(tech_params, scene_type, user_intent)
            
            # 调用Minimax模型
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # 解析AI响应为结构化建议
            return self._parse_ai_response(ai_response)
            
        except Exception as e:
            self.logger.error(f"AI建议生成失败: {e}")
            return {
                "position_adjustments": ["AI建议暂不可用"],
                "angle_adjustments": [],
                "technical_settings": [],
                "composition_tips": [],
                "error": str(e)
            }
    
    def _build_guidance_prompt(self, tech_params: Dict[str, Any], scene_type: str, user_intent: str) -> str:
        """构建AI模型的提示词"""
        
        # 从摄影知识库提取相关信息
        relevant_knowledge = self._extract_relevant_knowledge(scene_type)
        
        prompt = f"""
你是一个专业的手机摄影指导师。请根据以下信息为用户提供具体的拍摄指导：

场景类型：{scene_type}
用户意图：{user_intent}

技术参数分析：
{json.dumps(tech_params, ensure_ascii=False, indent=2)}

摄影知识参考：
{relevant_knowledge}

请提供具体、可执行的建议，包括：

1. **位置调整** - 具体的移动方向和距离（如"向左2步"、"蹲下30cm"）
2. **角度调整** - 具体的角度变化（如"手机向上倾斜15度"、"逆时针旋转45度"）
3. **技术设置** - 手机设置建议（如"开启人像模式"、"调整曝光+1档"）
4. **构图技巧** - 具体的构图改进（如"将主体放在右侧三分线上"）

要求：
- 建议要具体可操作，不要说"可以考虑"这样的话
- 避免理论性的教学，直接说怎么做
- 每个建议都要有明确的数值或方向
- 语言要简洁直接，像在现场指导一样

请用JSON格式返回建议：
{{
  "position_adjustments": ["具体位置调整建议"],
  "angle_adjustments": ["具体角度调整建议"],
  "technical_settings": ["具体技术设置建议"],
  "composition_tips": ["具体构图改进建议"]
}}
"""
        
        return prompt
    
    def _extract_relevant_knowledge(self, scene_type: str) -> str:
        """从摄影知识库提取相关信息"""
        knowledge_text = ""
        
        for book_name, book_content in self.photography_knowledge.items():
            if isinstance(book_content, list):
                for section in book_content:
                    if isinstance(section, dict) and 'content' in section:
                        content = section['content']
                        # 简单的关键词匹配
                        if any(keyword in content for keyword in [scene_type, "构图", "光线", "角度"]):
                            knowledge_text += content + "\n"
        
        return knowledge_text[:1000]  # 限制长度
    
    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """解析AI响应为结构化建议"""
        try:
            # 尝试解析JSON
            if "{" in ai_response and "}" in ai_response:
                json_start = ai_response.find("{")
                json_end = ai_response.rfind("}") + 1
                json_str = ai_response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        # 如果JSON解析失败，使用简单文本解析
        return {
            "position_adjustments": [ai_response[:200]],
            "angle_adjustments": [],
            "technical_settings": [],
            "composition_tips": []
        }


class ReactNativeInterface:
    """React Native应用接口"""
    
    def __init__(self, agent: PhotoGuideAgent):
        self.agent = agent
    
    def analyze_camera_frame(self, base64_image: str, scene_type: str = "通用") -> Dict[str, Any]:
        """
        分析相机实时画面
        
        Args:
            base64_image: base64编码的图片数据
            scene_type: 场景类型
            
        Returns:
            分析结果和建议
        """
        try:
            # 解码base64图片并保存临时文件
            import tempfile
            import base64
            
            image_data = base64.b64decode(base64_image)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(image_data)
                temp_path = temp_file.name
            
            # 分析图片
            result = self.agent.generate_guidance(temp_path, scene_type)
            
            # 清理临时文件
            os.unlink(temp_path)
            
            # 格式化为React Native友好的格式
            return self._format_for_rn(result)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "suggestions": []
            }
    
    def _format_for_rn(self, guidance: Dict[str, Any]) -> Dict[str, Any]:
        """格式化结果为React Native友好的格式"""
        if "error" in guidance:
            return {
                "success": False,
                "error": guidance["error"],
                "suggestions": []
            }
        
        suggestions = []
        
        # 合并所有建议
        basic_suggestions = guidance.get("basic_suggestions", [])
        ai_suggestions = guidance.get("ai_suggestions", {})
        
        for suggestion in basic_suggestions:
            suggestions.append({
                "type": "basic",
                "text": suggestion,
                "priority": "medium"
            })
        
        # 添加AI建议
        for category, items in ai_suggestions.items():
            if isinstance(items, list):
                for item in items:
                    suggestions.append({
                        "type": category,
                        "text": item,
                        "priority": "high"
                    })
        
        return {
            "success": True,
            "technical_analysis": guidance.get("technical_analysis", {}),
            "suggestions": suggestions,
            "scene_type": guidance.get("scene_type", "通用"),
            "timestamp": guidance.get("timestamp")
        }
    
    def get_scene_specific_tips(self, scene_type: str) -> Dict[str, Any]:
        """获取特定场景的拍摄技巧"""
        tips = {
            "人像": [
                "使用人像模式获得背景虚化效果",
                "确保眼部对焦清晰",
                "注意光线照射在脸部的角度",
                "避免从低角度仰拍"
            ],
            "风景": [
                "使用三分法构图",
                "寻找前景、中景、远景的层次",
                "注意地平线的水平",
                "利用黄金时间的光线"
            ],
            "美食": [
                "使用45度俯拍角度",
                "注意食物的颜色搭配",
                "利用自然光拍摄",
                "添加道具增加层次感"
            ],
            "建筑": [
                "注意透视和垂直线条",
                "寻找独特的角度",
                "利用对称性构图",
                "注意光影效果"
            ]
        }
        
        return {
            "scene_type": scene_type,
            "tips": tips.get(scene_type, tips["人像"]),
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # 示例用法
    API_KEY = "your_openrouter_api_key_here"
    
    # 初始化agent
    agent = PhotoGuideAgent(API_KEY)
    
    # React Native接口
    rn_interface = ReactNativeInterface(agent)
    
    # 示例：分析图片
    # guidance = agent.get_photo_guidance("example.jpg")
    # print(guidance)
    
    print("拍照引导Agent已初始化完成！")
    print("主要功能：")
    print("1. analyze_image_technical_params() - 分析图片技术参数")
    print("2. get_photo_guidance() - 获取拍照指导建议") 
    print("3. ReactNativeInterface - 为RN应用提供接口")