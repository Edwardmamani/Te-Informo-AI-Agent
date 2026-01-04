from crewai import Agent
from src.config.settings import get_llm

llm = get_llm()

def create_manager_agent():
    """
    Crea y retorna un agente Manager (Jefe de Redacción) configurado
    
    El Manager es responsable de:
    - Recibir solicitud de noticia
    - Analizar objetivo global
    - Descomponer en plan jerárquico (HTN) con planificación de orden parcial
    - Delegar tareas de búsqueda
    - Realizar revisión final
    - Publicar noticia
    
    Returns:
        Agent: Un agente Manager configurado con el LLM
    """
    return Agent(
        role='Jefe de Redacción',
        goal='Coordinar y supervisar el proceso completo de generación de noticias, desde la planificación hasta la publicación',
        backstory=(
            'Eres un experimentado jefe de redacción con años de experiencia en periodismo. '
            'Tu trabajo consiste en recibir solicitudes de noticias, analizar el objetivo global, '
            'descomponer la tarea en un plan jerárquico (HTN) usando planificación de orden parcial, '
            'delegar tareas específicas a los miembros del equipo, revisar el trabajo final y aprobar '
            'la publicación. Tienes una visión estratégica y capacidad de coordinación excepcional.'
        ),
        llm=llm,
        verbose=True,
        allow_delegation=True
    )
