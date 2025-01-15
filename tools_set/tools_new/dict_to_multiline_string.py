
class DictToMultilineString:
    name = "dict_to_multiline_string" 
    description = "搜索微信公众号上相关主题的文章"
    inputs = {
        "dict_data": {
            "type": "dict",
            "description": "需要转换成字符串的字典"
            },
        "indent": {
            "type": "int",
            "description": "dict转换成string的打印模式，默认为1"
            }
    }
    outputs = {
        "result": {
            "type": "string",
            "description": "dict转换后的string"
            }
    }
    props = {}

    async def run(dict_data, indent=0, params_format=False):

        if params_format:
            return ['dict_data', 'indent']
        result = ""
        for key, value in dict_data.items():
            if isinstance(value, dict):  # 如果值是字典，递归处理
                inner = await dict_to_multiline_string(value, indent + 4)
                result += " " * indent + f"{key}:\n" + inner
            else:  # 否则直接添加键值对
                result += " " * indent + f"{key}: {value}\n"
        return result