from crewai import Agent
from src.config.settings import get_llm

llm = get_llm()

def create_writer_agent():
    """
    Crea y retorna un agente Writer (Redactor) configurado
    
    El Writer es responsable de:
    - Recibir hechos validados
    - Redactar artículo (acción primitiva)
    - Formatear salida
    - Preparar la noticia para revisión final
    
    Returns:
        Agent: Un agente Writer configurado con el LLM
    """
    return Agent(
        role='Redactor (Writer)',
        goal='Redactar artículos de noticias claros, objetivos y bien estructurados basados en hechos validados',
        backstory=(
            'Eres un redactor periodístico profesional con años de experiencia escribiendo noticias objetivas y '
            'bien estructuradas. Tu trabajo consiste en recibir los hechos validados por el analista de sesgos, '
            'redactar un artículo profesional (acción primitiva) que presente la información de manera clara y '
            'objetiva, y formatear la salida según los estándares periodísticos. Tu estilo es claro, preciso y '
            'libre de opiniones personales, presentando solo los hechos verificados de manera equilibrada.'
        ),
        llm=llm,
        verbose=True
    )
