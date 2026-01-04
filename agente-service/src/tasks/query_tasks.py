from crewai import Task
from src.agents.investigador_agent import create_investigador_agent

def create_query_task(query: str):
    """
    Crea una tarea para responder una consulta del usuario
    
    Args:
        query: La consulta del usuario
        
    Returns:
        Task: Una tarea configurada para responder la consulta
    """
    investigador = create_investigador_agent()
    
    return Task(
        description=f"""
        Analiza y responde la siguiente consulta del usuario:
        {query}
        
        Proporciona una respuesta clara, concisa y útil.
        Si es sobre noticias o información actual, intenta ser específico y relevante.
        """,
        agent=investigador,
        expected_output="Una respuesta clara y bien estructurada sobre el tema consultado"
    )

def create_suggestions_task(query: str, context: list = None):
    """
    Crea una tarea para generar sugerencias relacionadas con una consulta
    
    Args:
        query: El tema principal de interés
        context: Lista de contexto previo de la conversación
        
    Returns:
        Task: Una tarea configurada para generar sugerencias
    """
    investigador = create_investigador_agent()
    context_str = "\n".join(context) if context else "Sin contexto previo"
    
    return Task(
        description=f"""
        El usuario está interesado en: {query}
        
        Contexto de la conversación:
        {context_str}
        
        Genera 3-5 sugerencias de temas relacionados o subtemas interesantes 
        que el usuario podría querer explorar. Las sugerencias deben ser:
        - Relevantes al tema principal
        - Específicas y accionables
        - Variadas y complementarias
        
        Responde SOLO con una lista de sugerencias, una por línea.
        """,
        agent=investigador,
        expected_output="Una lista de 3-5 sugerencias de temas relacionados"
    )

