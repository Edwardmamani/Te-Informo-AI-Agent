from src.tools.tools import NewsSearchTool

# 1. El agente solicita búsqueda
tool = NewsSearchTool()
result = tool._run(
    query="inteligencia artificial medicina",
    max_results=3
)

print(result)