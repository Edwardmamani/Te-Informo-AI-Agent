from crewai import Agent
from src.config.settings import get_llm

llm = get_llm()

def create_critic_agent():
    """
    Crea y retorna un agente Critic (Analista de Sesgos) configurado
    
    El Critic es responsable de:
    - Leer informe del investigador
    - Ejecutar vigilancia de ejecución
    - Detectar sesgos, falacias o datos falsos
    - Generar reporte de error si detecta problemas
    - Solicitar corrección o más fuentes
    - Aprobar hechos cuando cumplan estándares de calidad
    
    Returns:
        Agent: Un agente Critic configurado con el LLM
    """
    return Agent(
        role='Analista de Sesgos (Critic)',
        goal='Evaluar la calidad, veracidad y ausencia de sesgos en la información recopilada',
        backstory=(
            'Eres un analista experto en detección de sesgos, falacias lógicas y verificación de datos. '
            'Tu trabajo es leer los informes del investigador, ejecutar una vigilancia exhaustiva de la ejecución, '
            'detectar cualquier sesgo, falacia o dato falso. Cuando detectas problemas (CODE01), generas un reporte '
            'detallado de errores y solicitas corrección o más fuentes. Si no detectas problemas (CODE02), apruebas '
            'los hechos para pasar a la siguiente fase. Tu rigor analítico garantiza que solo se publiquen noticias '
            'con información verificada y libre de sesgos.'
        ),
        llm=llm,
        verbose=True
    )
