from src.crews.agent_crews import create_query_crew, create_suggestions_crew

def handle_query(query: str):
    """
    Maneja una consulta del usuario y retorna la respuesta
    
    Args:
        query: La consulta del usuario
        
    Returns:
        tuple: (dict, int) Un diccionario con el estado y la respuesta, y el código de estado HTTP
    """
    try:
        if not query:
            return {
                "status": "error",
                "message": "El campo 'query' es requerido"
            }, 400
        
        crew = create_query_crew(query)
        result = crew.kickoff()
        
        return {
            "status": "success",
            "query": query,
            "response": str(result)
        }, 200
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error procesando la consulta: {str(e)}"
        }, 500

def handle_suggestions(query: str, context: list = None):
    """
    Maneja una solicitud de sugerencias y retorna las sugerencias generadas
    
    Args:
        query: El tema principal de interés
        context: Lista de contexto previo de la conversación
        
    Returns:
        tuple: (dict, int) Un diccionario con el estado y las sugerencias, y el código de estado HTTP
    """
    try:
        if not query:
            return {
                "status": "error",
                "message": "El campo 'query' es requerido"
            }, 400
        
        crew = create_suggestions_crew(query, context)
        result = crew.kickoff()
        
        # Parsear sugerencias (asumiendo que vienen una por línea)
        suggestions = [s.strip() for s in str(result).split('\n') if s.strip()]
        
        return {
            "status": "success",
            "query": query,
            "suggestions": suggestions[:5]  # Limitar a 5 sugerencias
        }, 200
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generando sugerencias: {str(e)}"
        }, 500

