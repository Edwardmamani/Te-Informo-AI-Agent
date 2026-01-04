from crewai import Task
from src.agents.manager_agent import create_manager_agent
from src.agents.watchdog_agent import create_watchdog_agent
from src.agents.critic_agent import create_critic_agent
from src.agents.writer_agent import create_writer_agent

def create_planning_task(solicitud_noticia: str):
    """
    Crea una tarea para que el Manager analice y planifique la noticia
    
    Args:
        solicitud_noticia: La solicitud de noticia del usuario
        
    Returns:
        Task: Una tarea configurada para planificación HTN
    """
    manager = create_manager_agent()
    
    return Task(
        description=f"""
        Analiza la siguiente solicitud de noticia:
        {solicitud_noticia}
        
        Realiza las siguientes acciones:
        1. Analiza el objetivo global de la noticia solicitada
        2. Descompón la tarea en un plan jerárquico (HTN) usando planificación de orden parcial
        3. Identifica los subtemas y aspectos que deben investigarse
        4. Crea un plan de acción estructurado para el investigador
        
        Tu salida debe incluir:
        - Objetivo global de la noticia
        - Plan jerárquico descompuesto en subtareas
        - Aspectos clave a investigar
        - Criterios de relevancia para la información
        """,
        agent=manager,
        expected_output="Un plan jerárquico estructurado con el objetivo global, subtareas y criterios de investigación"
    )

def create_investigation_task(solicitud_noticia: str, plan_context: str = ""):
    """
    Crea una tarea para que el Watchdog investigue y recopile información
    
    Args:
        solicitud_noticia: La solicitud de noticia original
        plan_context: El contexto del plan generado por el Manager
        
    Returns:
        Task: Una tarea configurada para investigación
    """
    watchdog = create_watchdog_agent()
    
    return Task(
        description=f"""
        Realiza una investigación exhaustiva sobre la siguiente noticia solicitada:
        {solicitud_noticia}
        
        {f"Contexto del plan: {plan_context}" if plan_context else ""}
        
        Realiza las siguientes acciones:
        1. Activa sensores y herramientas de búsqueda para recopilar información
        2. Busca información de múltiples fuentes confiables y diversas
        3. Recopila información cruda sobre el tema
        4. Filtra la información por relevancia según los criterios establecidos
        5. Organiza la información en un informe preliminar estructurado
        
        Tu informe preliminar debe incluir:
        - Hechos principales verificados
        - Fuentes utilizadas
        - Contexto relevante
        - Información adicional importante
        - Nota sobre la calidad y confiabilidad de las fuentes
        """,
        agent=watchdog,
        expected_output="Un informe preliminar estructurado con información relevante, fuentes y evaluación de calidad"
    )

def create_critique_task(informe_preliminar: str, solicitud_noticia: str):
    """
    Crea una tarea para que el Critic analice y valide la información
    
    Args:
        informe_preliminar: El informe generado por el Watchdog
        solicitud_noticia: La solicitud original para contexto
        
    Returns:
        Task: Una tarea configurada para análisis crítico
    """
    critic = create_critic_agent()
    
    return Task(
        description=f"""
        Analiza el siguiente informe preliminar del investigador:
        {informe_preliminar}
        
        Contexto de la solicitud original: {solicitud_noticia}
        
        Ejecuta una vigilancia exhaustiva de ejecución y evalúa:
        
        1. DETECCIÓN DE PROBLEMAS (CODE01):
           - ¿Existen sesgos en la información presentada?
           - ¿Hay falacias lógicas en el razonamiento?
           - ¿Se detectan datos falsos o no verificados?
           - ¿La calidad de las fuentes cumple con el umbral requerido?
           
        2. Si DETECTAS PROBLEMAS (CODE01):
           - Genera un reporte detallado de errores identificados
           - Especifica qué tipo de problemas se encontraron (sesgos, falacias, datos falsos, baja calidad)
           - Indica qué correcciones o fuentes adicionales se requieren
           - Proporciona recomendaciones para mejorar la búsqueda
           
        3. Si NO DETECTAS PROBLEMAS (CODE02):
           - Aprueba los hechos como válidos
           - Confirma que la información cumple con estándares de calidad
           - Prepara los datos limpios para pasar al redactor
           
        Tu respuesta debe ser clara sobre si se detectaron problemas (CODE01) o si todo está aprobado (CODE02).
        """,
        agent=critic,
        expected_output="Un análisis crítico con código CODE01 (problemas detectados) o CODE02 (aprobado), incluyendo detalles del análisis"
    )

def create_reinvestigation_task(solicitud_noticia: str, reporte_error: str, plan_context: str = ""):
    """
    Crea una tarea para que el Watchdog replanifique y busque fuentes alternativas
    
    Args:
        solicitud_noticia: La solicitud de noticia original
        reporte_error: El reporte de errores del Critic
        plan_context: El contexto del plan original
        
    Returns:
        Task: Una tarea configurada para reinvestigación con backtracking
    """
    watchdog = create_watchdog_agent()
    
    return Task(
        description=f"""
        Se detectaron problemas en el informe preliminar. Debes replanificar la búsqueda (backtracking).
        
        Solicitud original: {solicitud_noticia}
        {f"Plan original: {plan_context}" if plan_context else ""}
        
        Reporte de errores del Analista de Sesgos:
        {reporte_error}
        
        Realiza las siguientes acciones:
        1. Analiza el reporte de errores detalladamente
        2. Replanifica la estrategia de búsqueda (backtracking)
        3. Busca fuentes alternativas y adicionales
        4. Enfócate en corregir los problemas específicos identificados
        5. Recopila nueva información que aborde las deficiencias
        6. Verifica la calidad de las nuevas fuentes antes de incluirlas
        
        Genera un nuevo informe preliminar corregido que:
        - Aborde todos los problemas identificados en el reporte de errores
        - Incluya fuentes alternativas y adicionales
        - Demuestre mejor calidad y veracidad
        - Cumpla con los estándares requeridos
        """,
        agent=watchdog,
        expected_output="Un nuevo informe preliminar corregido que aborde los problemas identificados con fuentes mejoradas"
    )

def create_writing_task(hechos_validados: str, solicitud_noticia: str):
    """
    Crea una tarea para que el Writer redacte el artículo final
    
    Args:
        hechos_validados: Los hechos aprobados por el Critic
        solicitud_noticia: La solicitud original para contexto
        
    Returns:
        Task: Una tarea configurada para redacción
    """
    writer = create_writer_agent()
    
    return Task(
        description=f"""
        Redacta un artículo de noticia basado en los siguientes hechos validados:
        
        Hechos validados y aprobados:
        {hechos_validados}
        
        Solicitud original: {solicitud_noticia}
        
        Realiza las siguientes acciones (acción primitiva de redacción):
        1. Estructura el artículo con formato periodístico profesional
        2. Presenta la información de manera clara, objetiva y equilibrada
        3. Usa un estilo periodístico estándar (quién, qué, cuándo, dónde, por qué, cómo)
        4. Asegúrate de que el artículo sea libre de opiniones personales
        5. Cita las fuentes de manera apropiada
        6. Mantén un tono profesional y objetivo
        
        FORMATO DE SALIDA REQUERIDO - HTML:
        Debes retornar ÚNICAMENTE el contenido en formato HTML, envuelto en un tag <article>.
        La estructura debe ser exactamente así:
        
        <article>
            <header>
                <h1>Título llamativo pero preciso del artículo</h1>
                <p class="entradilla">Entradilla o introducción atractiva que resuma los puntos clave</p>
            </header>
            
            <section class="cuerpo">
                <p>Primer párrafo del cuerpo del artículo...</p>
                <p>Segundo párrafo con información relevante...</p>
                <p>Continúa desarrollando el contenido de manera estructurada...</p>
                <!-- Agrega más párrafos según sea necesario -->
            </section>
            
            <footer>
                <p class="conclusion">Conclusión apropiada que cierre el artículo</p>
                <div class="fuentes">
                    <h3>Fuentes:</h3>
                    <ul>
                        <li>Fuente 1</li>
                        <li>Fuente 2</li>
                        <!-- Lista todas las fuentes utilizadas -->
                    </ul>
                </div>
            </footer>
        </article>
        
        IMPORTANTE:
        - Retorna SOLO el HTML, sin texto adicional antes o después
        - El tag <article> debe ser el elemento raíz
        - Usa etiquetas HTML semánticas apropiadas (header, section, footer, h1, p, ul, li)
        - El HTML debe ser válido y bien formateado
        - No incluyas explicaciones, comentarios fuera del HTML, o texto adicional
        
        El artículo debe estar listo para revisión final del Jefe de Redacción.
        """,
        agent=writer,
        expected_output="Un artículo de noticia completo en formato HTML, envuelto en un tag <article>, bien estructurado con header, cuerpo y footer, y listo para revisión final"
    )

def create_final_review_task(articulo: str, solicitud_noticia: str, plan_context: str = ""):
    """
    Crea una tarea para que el Manager haga la revisión final y apruebe la publicación
    
    Args:
        articulo: El artículo redactado por el Writer
        solicitud_noticia: La solicitud original
        plan_context: El plan original para verificar cumplimiento
        
    Returns:
        Task: Una tarea configurada para revisión final
    """
    manager = create_manager_agent()
    
    return Task(
        description=f"""
        Realiza la revisión final del artículo y aprueba su publicación.
        
        Solicitud original: {solicitud_noticia}
        {f"Plan original: {plan_context}" if plan_context else ""}
        
        Artículo redactado:
        {articulo}
        
        Realiza una revisión final como Jefe de Redacción:
        1. Verifica que el artículo cumpla con el objetivo global establecido
        2. Revisa la calidad periodística general
        3. Confirma que la información esté completa y bien estructurada
        4. Asegúrate de que cumpla con los estándares editoriales
        5. Verifica el formato y presentación
        
        6. Si el artículo es aprobado:
           - Aprueba la publicación
           - Genera la noticia final lista para publicar
           
        7. Si requiere ajustes menores:
           - Indica qué ajustes se necesitan
           - Genera versión corregida
        
        Tu salida debe ser la noticia final aprobada y lista para publicación, o indicar que se requiere revisión adicional.
        """,
        agent=manager,
        expected_output="La noticia final aprobada y lista para publicación, o indicación de ajustes necesarios"
    )
