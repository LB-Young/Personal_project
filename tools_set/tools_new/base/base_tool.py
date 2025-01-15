from typing import Any, Dict, Optional

class BaseTool:
    """所有工具的基类"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = self.__doc__ or ""

    async def run(self, *args, **kwargs) -> Any:
        """运行工具的主要方法"""
        raise NotImplementedError
    
    def get_config(self) -> Dict:
        """获取工具配置"""
        return {}

    @property
    def tool_info(self) -> Dict:
        """获取工具信息"""
        return {
            "name": self.name,
            "description": self.description,
            "config": self.get_config()
        } 