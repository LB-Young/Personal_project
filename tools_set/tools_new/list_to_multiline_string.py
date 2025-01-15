from .dict_to_multiline_string import dict_to_multiline_string

class ListToMultilineString:
    name = "list_to_multiline_string" 
    description = "搜索微信公众号上相关主题的文章"
    inputs = {
        "list_data": {
            "type": "list",
            "description": "需要转换成字符串的列表"
            }
    }
    outputs = {
        "result": {
            "type": "string",
            "description": "list转换后的string"
            }
    }
    props = {}

    async def run(list_data=[], params_format=False):
      if params_format:
        return ['list_data']
      
      result = ""
      for item in list_data:
        if isinstance(item, list):
          result += await ListToMultilineString.list_to_multiline_string(item) + "\n"
        elif isinstance(item, dict):
          result += await dict_to_multiline_string(item, 0) + "\n"
        else:
          result += str(item) + "\n"
      return result