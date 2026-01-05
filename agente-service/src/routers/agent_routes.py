import json
from flask import Blueprint, request, Response
from src.controllers.news_controller import handle_news_generation

# Crear un blueprint para las rutas del agente
agent_bp = Blueprint('agent', __name__, url_prefix='/agent')

@agent_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de salud"""
    response = {
        "status": "ok",
        "message": "Servidor de agente IA funcionando"
    }
    return Response(
        json.dumps(response, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )


@agent_bp.route('/generate-news', methods=['POST'])
def generate_news():
    """
    Endpoint para generar noticias usando el flujo completo de agentes
    Body esperado: {
        "solicitud": "tema de la noticia a generar",
        "max_iterations": 3 (opcional),
        "quality_threshold": 0.8 (opcional)
    }
    """
    data = request.get_json() or {}
    solicitud = data.get('solicitud')
    max_iterations = data.get('max_iterations')
    quality_threshold = data.get('quality_threshold')

    if solicitud is None or str(solicitud).strip() == "":
        error_response = {
            "error": "No se proporcionó solicitud para generación de noticia.",
            "detail": "El campo 'solicitud' es obligatorio y no debe estar vacío."
        }
        return Response(
            json.dumps(error_response, ensure_ascii=False),
            mimetype='application/json; charset=utf-8'
        ), 400

    # Valores por defecto si no fueron provistos
    if max_iterations is None:
        max_iterations = 3
    if quality_threshold is None:
        quality_threshold = 0.8
    
    response, status_code = handle_news_generation(solicitud, max_iterations, quality_threshold)
    # Usar json.dumps con ensure_ascii=False para preservar caracteres UTF-8
    return Response(
        json.dumps(response, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    ), status_code

