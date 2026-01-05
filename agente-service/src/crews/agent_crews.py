from crewai import Crew
from src.tasks.query_tasks import create_query_task, create_suggestions_task
from src.agents.investigador_agent import create_investigador_agent
from src.tasks.news_tasks import (
    create_planning_task,
    create_investigation_task,
    create_critique_task,
    create_reinvestigation_task,
    create_writing_task,
    create_final_review_task
)
from src.agents.manager_agent import create_manager_agent
from src.agents.watchdog_agent import create_watchdog_agent
from src.agents.critic_agent import create_critic_agent
from src.agents.writer_agent import create_writer_agent


def create_news_generation_crew(solicitud_noticia: str):
    """
    Crea un crew para generar noticias siguiendo el flujo completo:
    Manager -> Watchdog -> Critic -> Writer -> Manager (revisión final)
    
    Implementa el flujo con manejo de CODE01 (problemas detectados) y CODE02 (aprobado)
    
    Args:
        solicitud_noticia: La solicitud de noticia del usuario
        
    Returns:
        Crew: Un crew configurado para generar noticias
    """
    # Crear los agentes
    manager = create_manager_agent()
    watchdog = create_watchdog_agent()
    critic = create_critic_agent()
    writer = create_writer_agent()
    
    # Crear las tareas en orden secuencial
    # La lógica condicional (CODE01/CODE02) se manejará en el controlador
    planning_task = create_planning_task(solicitud_noticia)
    investigation_task = create_investigation_task(solicitud_noticia)
    critique_task = create_critique_task("", solicitud_noticia)  # Se actualizará con el informe
    writing_task = create_writing_task("", solicitud_noticia)  # Se actualizará con hechos validados
    final_review_task = create_final_review_task("", solicitud_noticia)
    
    # Configurar dependencias entre tareas (usando context para pasar datos)
    investigation_task.context = [planning_task]
    critique_task.context = [investigation_task]
    writing_task.context = [critique_task]
    final_review_task.context = [writing_task, planning_task]
    
    return Crew(
        agents=[manager, watchdog, critic, writer],
        tasks=[planning_task, investigation_task, critique_task, writing_task, final_review_task],
        verbose=True,
        process="sequential"  # Ejecutar tareas en secuencia
    )

