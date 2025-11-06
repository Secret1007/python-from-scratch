"""
内容审核工具模块
"""
import re


def contains_sensitive_words(content: str) -> bool:
    """
    检查内容是否包含敏感词
    
    使用单词边界检测，避免误判：
    - "assess" 不会被误判为包含 "ass"
    - "classical" 不会被误判
    
    Args:
        content: 要检查的内容
        
    Returns:
        bool: 如果包含敏感词返回 True，否则返回 False
    """
    # 敏感词列表（示例）
    # 实际项目中可以从配置文件或数据库读取
    sensitive_words = [
        "porn", "fuck", "shit", "bitch", 
        "cunt", "damn", "cock", "pussy"
    ]
    
    # 转换为小写进行检测
    content_lower = content.lower()
    
    # 使用单词边界 \b 进行精确匹配
    for word in sensitive_words:
        # \b 确保是独立单词，不是其他单词的一部分
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, content_lower):
            return True
    
    return False

