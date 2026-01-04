from flask import Blueprint, jsonify, request
from src.controllers.agent_controller import handle_query, handle_suggestions

# Crear un blueprint para las rutas del agente
agent_bp = Blueprint('agent', __name__, url_prefix='/agent')

@agent_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de salud"""
    return jsonify({
        "status": "ok",
        "message": "Servidor de agente IA funcionando"
    })

@agent_bp.route('/query', methods=['POST'])
def query():
    """
    Endpoint principal para consultar al agente
    Body esperado: {"query": "tu pregunta aquí"}
    """
    data = request.get_json()
    query_text = data.get('query', '') if data else ''
    
    response, status_code = handle_query(query_text)
    return jsonify(response), status_code

@agent_bp.route('/suggestions', methods=['POST'])
def suggestions():
    """
    Endpoint para obtener sugerencias relacionadas con una consulta
    Body esperado: {"query": "tema principal", "context": ["contexto previo"]}
    """
    data = request.get_json()
    if data:
        query_text = data.get('query', '')
        context = data.get('context', [])
    else:
        query_text = ''
        context = []
    
    response, status_code = handle_suggestions(query_text, context)
    return jsonify(response), status_code

