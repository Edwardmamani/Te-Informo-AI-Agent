from flask import Blueprint, jsonify, request
from src.controllers.news_controller import handle_news_generation

# Crear un blueprint para las rutas del agente
agent_bp = Blueprint('agent', __name__, url_prefix='/agent')

@agent_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de salud"""
    return jsonify({
        "status": "ok",
        "message": "Servidor de agente IA funcionando"
    })


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
        return jsonify({
            "error": "No se proporcionó solicitud para generación de noticia.",
            "detail": "El campo 'solicitud' es obligatorio y no debe estar vacío."
        }), 400

    # Valores por defecto si no fueron provistos
    if max_iterations is None:
        max_iterations = 3
    if quality_threshold is None:
        quality_threshold = 0.8
    
    response, status_code = handle_news_generation(solicitud, max_iterations, quality_threshold)
    return jsonify(response), status_code

