import os


class DirReader:
    name = "dir_reader" 
    description = "搜索微信公众号上相关主题的文章"
    inputs = {
        "dirs": {
            "type": "list",
            "description": "需要读取的文件夹路径列表"
            }
    }
    outputs = {
        "results": {
            "type": "list",
            "description": "目录下文件的内容列表"
            }
    }
    props = {}

    async def run(dirs=[], params_format=False):
        if params_format:
            return ['code', 'code_params']
        try:
            results = []
            for dir in dirs:
                for file in os.listdir(dir):
                    with open(os.path.join(dir, file), 'r', encoding='utf-8') as f:
                        results.append(f.read())
            return results
        except:
            raise Exception("文件夹内容读取出错！")
    
"""
"dir_reader":{
    "object":dir_reader,
    "describe":"读取一个文件夹下的全部文件的内容，需要参数{'dirs':待读取的文件夹路径，格式为[dir1, dir22, ...]}",
}
"""