# Herramientas de API de Noticias

Este módulo proporciona herramientas para que los agentes de CrewAI puedan interactuar con los servicios de noticias del backend TypeScript.

## Descripción

Las herramientas permiten al agente investigador buscar noticias en múltiples fuentes y extraer contenido completo de artículos específicos.

## Endpoints del Backend

El backend expone los siguientes endpoints:

- `POST /api/news/search` - Busca noticias en múltiples fuentes
- `POST /api/news/aggregate` - Obtiene noticias agregadas (método simplificado)
- `POST /api/news/extract` - Extrae contenido completo de un artículo
- `GET /api/news/health` - Verifica el estado del servicio

## Herramientas Disponibles

### 1. `search_news_tool(query, user_interests="")`

Busca noticias en múltiples fuentes:
- Google News
- BBC News
- CNN
- El País
- YouTube (videos de noticias)

**Parámetros:**
- `query` (str, requerido): Término de búsqueda
- `user_interests` (str, opcional): Intereses separados por comas para filtrar resultados

**Ejemplo:**
```python
from src.tools.news_api_tool import search_news_tool

result = search_news_tool("inteligencia artificial", "tecnología,IA")
print(result)
```

### 2. `extract_content_tool(url)`

Extrae el contenido completo de un artículo específico.

**Parámetros:**
- `url` (str, requerido): URL del artículo a extraer

**Ejemplo:**
```python
from src.tools.news_api_tool import extract_content_tool

content = extract_content_tool("https://example.com/article")
print(content)
```

## Uso en Agentes

Las herramientas están integradas en el agente investigador:

```python
from src.agents.investigador_agent import create_investigador_agent

agente = create_investigador_agent()
# El agente ya tiene acceso a las herramientas automáticamente
```

## Configuración

Asegúrate de configurar la variable de entorno `BACKEND_URL` en tu archivo `.env`:

```
BACKEND_URL=http://localhost:3001
```

Por defecto, se usa `http://localhost:3001` si no está configurada.

## Clase NewsAPITool

También puedes usar la clase directamente para más control:

```python
from src.tools.news_api_tool import NewsAPITool

tool = NewsAPITool(base_url="http://localhost:3001")
result = tool.search_news("cambio climático", ["medio ambiente"])
```

## Respuestas de la API

### Búsqueda de Noticias

```json
{
  "status": "success",
  "data": {
    "articles": [
      {
        "title": "Título del artículo",
        "url": "https://example.com/article",
        "snippet": "Resumen del artículo...",
        "source": "BBC News",
        "imageUrl": "https://example.com/image.jpg",
        "type": "article",
        "publishedDate": "2024-01-01"
      }
    ],
    "count": 15,
    "query": "término de búsqueda",
    "userInterests": []
  }
}
```

### Extracción de Contenido

```json
{
  "status": "success",
  "data": {
    "url": "https://example.com/article",
    "content": "Contenido completo del artículo...",
    "contentLength": 2000
  }
}
```

