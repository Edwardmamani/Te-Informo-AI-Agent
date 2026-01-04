"""
Herramientas para que el agente investigador pueda usar los servicios de noticias del backend
"""
import requests
from typing import List, Dict, Optional
import os

# URL del backend (debe estar configurada en las variables de entorno)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:3001')

class NewsAPITool:
    """
    Herramienta para interactuar con la API de noticias del backend
    """
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or BACKEND_URL
    
    def search_news(self, query: str, user_interests: List[str] = None) -> Dict:
        """
        Busca noticias en múltiples fuentes (Google News, BBC, CNN, El País, YouTube)
        
        Args:
            query: Término de búsqueda
            user_interests: Lista opcional de intereses del usuario para filtrar
            
        Returns:
            Dict con los artículos encontrados
        """
        try:
            url = f"{self.base_url}/api/news/search"
            payload = {
                "query": query,
                "userInterests": user_interests or []
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'success': True,
                    'articles': data.get('data', {}).get('articles', []),
                    'count': data.get('data', {}).get('count', 0)
                }
            else:
                return {
                    'success': False,
                    'error': data.get('message', 'Error desconocido')
                }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Error de conexión: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def aggregate_news(self, query: str) -> Dict:
        """
        Obtiene noticias agregadas de múltiples fuentes (método simplificado)
        
        Args:
            query: Término de búsqueda
            
        Returns:
            Dict con los artículos agregados
        """
        try:
            url = f"{self.base_url}/api/news/aggregate"
            payload = {"query": query}
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'success': True,
                    'articles': data.get('data', {}).get('articles', []),
                    'count': data.get('data', {}).get('count', 0)
                }
            else:
                return {
                    'success': False,
                    'error': data.get('message', 'Error desconocido')
                }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Error de conexión: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def extract_article_content(self, url: str) -> Dict:
        """
        Extrae el contenido completo de un artículo específico
        
        Args:
            url: URL del artículo a extraer
            
        Returns:
            Dict con el contenido extraído
        """
        try:
            api_url = f"{self.base_url}/api/news/extract"
            payload = {"url": url}
            
            response = requests.post(api_url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'success': True,
                    'url': data.get('data', {}).get('url', ''),
                    'content': data.get('data', {}).get('content', ''),
                    'contentLength': data.get('data', {}).get('contentLength', 0)
                }
            else:
                return {
                    'success': False,
                    'error': data.get('message', 'Error desconocido')
                }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Error de conexión: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def check_health(self) -> Dict:
        """
        Verifica el estado del servicio de noticias
        
        Returns:
            Dict con el estado del servicio
        """
        try:
            url = f"{self.base_url}/api/news/health"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            return {
                'success': True,
                'status': data.get('status'),
                'message': data.get('message', '')
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Servicio no disponible: {str(e)}'
            }


# Instancia global de la herramienta
news_api_tool = NewsAPITool()

# Funciones wrapper para usar con CrewAI
def search_news_tool(query: str, user_interests: str = "") -> str:
    """
    Busca noticias en múltiples fuentes (Google News, BBC, CNN, El País, YouTube).
    Esta herramienta te permite obtener información actualizada sobre cualquier tema
    desde fuentes periodísticas confiables.
    
    Args:
        query: El tema o término de búsqueda sobre el cual buscar noticias (requerido)
        user_interests: Intereses opcionales separados por comas para filtrar resultados.
                       Ejemplo: "tecnología,IA,ciencia" o "política,economía"
        
    Returns:
        String formateado con la lista de artículos encontrados, incluyendo título,
        fuente, URL, resumen y tipo (artículo o video). Si no se encuentran noticias,
        retorna un mensaje informativo.
    """
    # Convertir user_interests si es string
    if isinstance(user_interests, str) and user_interests.strip():
        interests_list = [i.strip() for i in user_interests.split(',') if i.strip()]
    elif isinstance(user_interests, list):
        interests_list = user_interests
    else:
        interests_list = []
    
    result = news_api_tool.search_news(query, interests_list)
    
    if result['success']:
        articles = result.get('articles', [])
        if not articles:
            return f"No se encontraron noticias para la consulta: {query}"
        
        formatted_result = f"✅ Se encontraron {result['count']} artículos sobre '{query}':\n\n"
        
        for i, article in enumerate(articles, 1):
            formatted_result += f"{i}. {article.get('title', 'Sin título')}\n"
            formatted_result += f"   Fuente: {article.get('source', 'Desconocida')}\n"
            formatted_result += f"   URL: {article.get('url', 'N/A')}\n"
            snippet = article.get('snippet', '')
            if snippet:
                formatted_result += f"   Resumen: {snippet[:200]}...\n"
            if article.get('type'):
                formatted_result += f"   Tipo: {article.get('type')}\n"
            formatted_result += "\n"
        
        return formatted_result
    else:
        return f"❌ Error al buscar noticias: {result.get('error', 'Error desconocido')}"


def extract_content_tool(url: str) -> str:
    """
    Extrae el contenido completo de un artículo de noticia específico.
    Usa esta herramienta cuando necesites leer el contenido completo de un artículo
    después de encontrarlo con la herramienta de búsqueda.
    
    Args:
        url: La URL completa del artículo del cual extraer el contenido (requerido)
        
    Returns:
        String con el contenido completo del artículo extraído, incluyendo su longitud
        en caracteres. Si hay un error, retorna un mensaje descriptivo del problema.
    """
    result = news_api_tool.extract_article_content(url)
    
    if result['success']:
        content = result.get('content', '')
        content_length = result.get('contentLength', 0)
        
        if content:
            return f"✅ Contenido extraído ({content_length} caracteres):\n\n{content}"
        else:
            return f"⚠️ No se pudo extraer contenido de la URL: {url}"
    else:
        return f"❌ Error al extraer contenido: {result.get('error', 'Error desconocido')}"


# Crear herramientas para CrewAI usando @tool decorator
try:
    from crewai.tools import tool
    
    @tool("Buscar Noticias")
    def search_news(query: str, user_interests: str = "") -> str:
        """
        Busca noticias en múltiples fuentes (Google News, BBC, CNN, El País, YouTube).
        Úsala cuando necesites información actualizada sobre un tema específico.
        
        Args:
            query: El tema o término de búsqueda sobre el cual buscar noticias
            user_interests: Intereses opcionales separados por comas para filtrar resultados (ej: "tecnología,IA,ciencia")
            
        Returns:
            Una lista formateada de artículos encontrados con título, fuente, URL y resumen
        """
        interests_list = [i.strip() for i in user_interests.split(',') if i.strip()] if user_interests else []
        return search_news_tool(query, interests_list)
    
    @tool("Extraer Contenido de Artículo")
    def extract_article(url: str) -> str:
        """
        Extrae el contenido completo de un artículo de noticia específico.
        Úsala cuando necesites leer el contenido completo de un artículo después de encontrarlo.
        
        Args:
            url: La URL completa del artículo del cual extraer el contenido
            
        Returns:
            El contenido completo del artículo extraído
        """
        return extract_content_tool(url)
        
except ImportError:
    # Si crewai.tools no está disponible, usar funciones simples
    print("⚠️ crewai.tools no está disponible. Usando funciones simples.")
    search_news = search_news_tool
    extract_article = extract_content_tool

