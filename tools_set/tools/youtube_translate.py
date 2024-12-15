from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
import re
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
os.environ['HTTPS_PROXY'] = 'https://127.0.0.1:10809'

def get_video_id(url):
    """从YouTube URL中提取视频ID"""
    # 支持几种常见的YouTube URL格式
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu.be\/)([\w-]+)',
        r'(?:youtube\.com\/embed\/)([\w-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("无效的YouTube URL")

def translate_captions(url):
    """获取YouTube视频字幕并翻译成中文"""
    try:
        # 获取视频ID
        video_id = get_video_id(url)
        
        # 获取字幕
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # 初始化翻译器
        translator = Translator()
        
        # 存储翻译结果
        translated_captions = []
        
        # 逐条翻译字幕
        for transcript in transcript_list:
            text = transcript['text']
            # 翻译成中文
            translation = translator.translate(text, dest='zh-cn')
            
            translated_captions.append({
                'start': transcript['start'],
                'duration': transcript['duration'],
                'original': text,
                'translated': translation.text
            })
            
        return translated_captions
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

def main():
    # 示例用法
    # url = input("请输入YouTube视频URL: ")
    url = "https://www.youtube.com/watch?v=WQQdd6qGxNs"
    captions = translate_captions(url)
    
    if captions:
        print("\n字幕翻译结果:")
        for caption in captions:
            print(f"\n时间: {caption['start']:.2f}s")
            print(f"原文: {caption['original']}")
            print(f"译文: {caption['translated']}")

if __name__ == "__main__":
    main()