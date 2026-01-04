import re
from src.crews.agent_crews import create_news_generation_crew
from src.tasks.news_tasks import (
    create_planning_task,
    create_investigation_task,
    create_critique_task,
    create_reinvestigation_task,
    create_writing_task,
    create_final_review_task
)
from crewai import Crew
from src.agents.manager_agent import create_manager_agent
from src.agents.watchdog_agent import create_watchdog_agent
from src.agents.critic_agent import create_critic_agent
from src.agents.writer_agent import create_writer_agent

def detect_code01_code02(text: str):
    """
    Detecta si el texto contiene CODE01 (problemas detectados) o CODE02 (aprobado)
    
    Args:
        text: El texto a analizar
        
    Returns:
        tuple: (code, bool) - El código detectado y si se encontró un código válido
    """
    text_upper = text.upper()
    
    # Buscar CODE01 o CODE02 en el texto
    if 'CODE01' in text_upper or 'PROBLEMAS DETECTADOS' in text_upper or 'ERRORES' in text_upper:
        return 'CODE01', True
    elif 'CODE02' in text_upper or 'APROBADO' in text_upper or 'NO DETECTA' in text_upper:
        return 'CODE02', True
    
    # Si no se encuentra explícitamente, buscar indicadores
    problem_indicators = ['sesgo', 'falacia', 'dato falso', 'error', 'problema', 'corrección']
    approve_indicators = ['aprobado', 'válido', 'correcto', 'sin problemas', 'cumple']
    
    has_problems = any(indicator in text_upper for indicator in problem_indicators)
    is_approved = any(indicator in text_upper for indicator in approve_indicators)
    
    if has_problems and not is_approved:
        return 'CODE01', True
    elif is_approved and not has_problems:
        return 'CODE02', True
    
    # Por defecto, si no está claro, asumir aprobado (CODE02)
    return 'CODE02', False

def handle_news_generation(solicitud_noticia: str, max_iterations: int = 3, quality_threshold: float = 0.8):
    """
    Maneja el flujo completo de generación de noticias con manejo de CODE01/CODE02
    
    Implementa el flujo:
    1. Manager: Recibe solicitud, analiza, planifica (HTN)
    2. Watchdog: Investiga y recopila información
    3. Critic: Analiza y detecta problemas (CODE01) o aprueba (CODE02)
    4. Si CODE01: Watchdog replanifica y busca fuentes alternativas (backtracking)
    5. Si CODE02: Writer redacta el artículo
    6. Manager: Revisión final y publicación
    
    Args:
        solicitud_noticia: La solicitud de noticia del usuario
        max_iterations: Número máximo de iteraciones para corrección
        quality_threshold: Umbral de calidad requerido (0.0 - 1.0)
        
    Returns:
        tuple: (dict, int) Un diccionario con el estado y la noticia generada, y el código de estado HTTP
    """
    try:
        if not solicitud_noticia:
            return {
                "status": "error",
                "message": "La solicitud de noticia es requerida"
            }, 400
        
        # Paso 1: Manager - Planificación
        print("📋 Paso 1: Manager iniciando planificación...")
        manager = create_manager_agent()
        planning_task = create_planning_task(solicitud_noticia)
        planning_crew = Crew(
            agents=[manager],
            tasks=[planning_task],
            verbose=True
        )
        plan_result = planning_crew.kickoff()
        plan_context = str(plan_result)
        print(f"✅ Plan generado: {plan_context[:200]}...")
        
        # Paso 2: Watchdog - Investigación inicial
        print("🔍 Paso 2: Watchdog iniciando investigación...")
        watchdog = create_watchdog_agent()
        investigation_task = create_investigation_task(solicitud_noticia, plan_context)
        investigation_crew = Crew(
            agents=[watchdog],
            tasks=[investigation_task],
            verbose=True
        )
        investigation_result = investigation_crew.kickoff()
        informe_preliminar = str(investigation_result)
        print(f"✅ Informe preliminar generado: {informe_preliminar[:200]}...")
        
        # Paso 3: Critic - Análisis y validación (con loop de corrección)
        print("🔬 Paso 3: Critic iniciando análisis...")
        critic = create_critic_agent()
        iteration = 0
        informe_actual = informe_preliminar
        code_detected = None
        
        while iteration < max_iterations:
            iteration += 1
            print(f"🔄 Iteración {iteration}/{max_iterations} - Analizando calidad...")
            
            critique_task = create_critique_task(informe_actual, solicitud_noticia)
            critique_crew = Crew(
                agents=[critic],
                tasks=[critique_task],
                verbose=True
            )
            critique_result = critique_crew.kickoff()
            critique_text = str(critique_result)
            
            # Detectar CODE01 o CODE02
            code, found = detect_code01_code02(critique_text)
            code_detected = code
            print(f"📊 Código detectado: {code}")
            
            if code == 'CODE01':
                print(f"⚠️ CODE01: Problemas detectados en iteración {iteration}")
                print("🔄 Watchdog replanificando búsqueda (backtracking)...")
                
                # Paso 3.1: Watchdog - Replanificación y búsqueda de fuentes alternativas
                reinvestigation_task = create_reinvestigation_task(
                    solicitud_noticia,
                    critique_text,
                    plan_context
                )
                reinvestigation_crew = Crew(
                    agents=[watchdog],
                    tasks=[reinvestigation_task],
                    verbose=True
                )
                reinvestigation_result = reinvestigation_crew.kickoff()
                informe_actual = str(reinvestigation_result)
                print(f"✅ Nuevo informe generado: {informe_actual[:200]}...")
                
                # Continuar al siguiente ciclo de validación
                continue
            elif code == 'CODE02':
                print(f"✅ CODE02: Información aprobada después de {iteration} iteración(es)")
                break
        
        # Si después de todas las iteraciones aún hay problemas, reportar
        if code_detected == 'CODE01':
            return {
                "status": "warning",
                "message": f"No se pudo alcanzar el umbral de calidad después de {max_iterations} iteraciones",
                "solicitud": solicitud_noticia,
                "plan": plan_context,
                "ultimo_informe": informe_actual,
                "ultimo_analisis": critique_text,
                "iteraciones": iteration
            }, 200
        
        # Paso 4: Writer - Redacción del artículo
        print("✍️ Paso 4: Writer iniciando redacción...")
        writer = create_writer_agent()
        writing_task = create_writing_task(critique_text, solicitud_noticia)
        writing_crew = Crew(
            agents=[writer],
            tasks=[writing_task],
            verbose=True
        )
        writing_result = writing_crew.kickoff()
        articulo = str(writing_result)
        print(f"✅ Artículo redactado: {articulo[:200]}...")
        
        # Paso 5: Manager - Revisión final y publicación
        print("👁️ Paso 5: Manager realizando revisión final...")
        final_review_task = create_final_review_task(articulo, solicitud_noticia, plan_context)
        final_review_crew = Crew(
            agents=[manager],
            tasks=[final_review_task],
            verbose=True
        )
        final_review_result = final_review_crew.kickoff()
        noticia_final = str(final_review_result)
        print(f"✅ Noticia final aprobada: {noticia_final[:200]}...")
        
        return {
            "status": "success",
            "message": "Noticia generada exitosamente",
            "solicitud": solicitud_noticia,
            "noticia": noticia_final,
            "plan": plan_context,
            "iteraciones_critica": iteration,
            "codigo_final": code_detected
        }, 200
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generando la noticia: {str(e)}"
        }, 500

