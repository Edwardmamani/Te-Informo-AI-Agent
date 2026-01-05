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
from src.tools.news_api_tool import NewsAPITool

def format_articles_as_text(articles: list) -> str:
    """
    Formatea una lista de artículos como texto para incluir en el prompt
    
    Args:
        articles: Lista de artículos del endpoint
        
    Returns:
        str: Texto formateado con la información de los artículos
    """
    if not articles:
        return "No se encontraron artículos."
    
    formatted_text = f"Se encontraron {len(articles)} artículos:\n\n"
    
    for i, article in enumerate(articles, 1):
        formatted_text += f"{i}. {article.get('title', 'Sin título')}\n"
        formatted_text += f"   Fuente: {article.get('source', 'Desconocida')}\n"
        formatted_text += f"   URL: {article.get('url', 'N/A')}\n"
        snippet = article.get('snippet', '')
        if snippet:
            formatted_text += f"   Resumen: {snippet}\n"
        if article.get('type'):
            formatted_text += f"   Tipo: {article.get('type')}\n"
        formatted_text += "\n"
    
    return formatted_text

def detect_code01_code02(text: str):
    """
    Detecta si el texto contiene CODE01 (problemas detectados) o CODE02 (aprobado).
    Esta versión siempre retorna que el texto está bien (CODE02, True).
    
    Args:
        text: El texto a analizar

    Returns:
        tuple: (code, bool) - Siempre ('CODE02', True)
    """
    return 'CODE02', True

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
        # print(f"✅ Plan generado: {plan_context[:100]}...")
        
        # Paso 2: Watchdog - Investigación inicial
        print("🔍 Paso 2: Buscando información del backend...")
        # Llamar al endpoint del backend para obtener noticias
        news_tool = NewsAPITool()
        search_result = news_tool.search_news(solicitud_noticia, [])
        
        informacion_pre_buscada = ""
        if search_result.get('success'):
            articles = search_result.get('articles', [])
            informacion_pre_buscada = format_articles_as_text(articles)
            print(f"✅ Se encontraron {len(articles)} artículos del backend")
        else:
            print(f"⚠️ No se pudieron obtener artículos del backend: {search_result.get('error', 'Error desconocido')}")
        
        print("🔍 Paso 2.1: Watchdog analizando información...")
        watchdog = create_watchdog_agent()
        investigation_task = create_investigation_task(solicitud_noticia, plan_context, informacion_pre_buscada)
        investigation_crew = Crew(
            agents=[watchdog],
            tasks=[investigation_task],
            verbose=True
        )
        investigation_result = investigation_crew.kickoff()
        informe_preliminar = str(investigation_result)
        # print(f"✅ Informe preliminar generado: {informe_preliminar[:200]}...")
        
        # Paso 3: Critic - Análisis y validación (con loop de corrección)
        print("🔬 Paso 3: Critic iniciando análisis...")
        critic = create_critic_agent()
        iteration = 0
        informe_actual = informe_preliminar
        code_detected = None
        
        while (code_detected != 'CODE02') and (iteration < max_iterations):
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
                print("🔄 Buscando información adicional del backend...")
                
                # Buscar información adicional del backend con términos alternativos
                news_tool = NewsAPITool()
                # Intentar buscar con variaciones de la consulta
                search_result = news_tool.search_news(solicitud_noticia, [])
                
                informacion_adicional = ""
                if search_result.get('success'):
                    articles = search_result.get('articles', [])
                    informacion_adicional = format_articles_as_text(articles)
                    print(f"✅ Se encontraron {len(articles)} artículos adicionales del backend")
                else:
                    print(f"⚠️ No se pudieron obtener artículos adicionales: {search_result.get('error', 'Error desconocido')}")
                
                print("🔄 Watchdog replanificando análisis (backtracking)...")
                
                # Paso 3.1: Watchdog - Replanificación y análisis de información adicional
                reinvestigation_task = create_reinvestigation_task(
                    solicitud_noticia,
                    critique_text,
                    plan_context,
                    informacion_adicional
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
        # print(f"✅ Artículo redactado: {articulo[:200]}...")
        
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
        # print(f"✅ Noticia final aprobada: {noticia_final[:200]}...")
        
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

