"""
Servidor simple con un agente IA usando CrewAI
Ejemplo básico de un agente que puede responder preguntas y realizar tareas
Estructura refactorizada con separación de responsabilidades
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from src.config.settings import SERVER_CONFIG
from src.utils.env_loader import get_openai_api_key
from src.routers.agent_routes import agent_bp

app = Flask(__name__)
CORS(app)  # Permitir CORS para conectar con el frontend

# Registrar los blueprints (rutas)
app.register_blueprint(agent_bp)

# Ruta raíz de salud (mantener compatibilidad)
@app.route('/', methods=['GET'])
def root():
    """Endpoint raíz"""
    return jsonify({"status": "ok", "message": "Servidor de agente IA funcionando"})

if __name__ == '__main__':
    # Verificar que la API key esté configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  ADVERTENCIA: OPENAI_API_KEY no está configurada")
        print("   Configúrala en el archivo .env antes de ejecutar")
    
    print(f"🚀 Iniciando servidor de agente IA en puerto {SERVER_CONFIG['port']}")
    print(f"📡 Endpoints disponibles:")
    print(f"   - GET  /")
    print(f"   - GET  /agent/health")
    print(f"   - POST /agent/query")
    print(f"   - POST /agent/suggestions")
    
    app.run(
        host=SERVER_CONFIG['host'],
        port=SERVER_CONFIG['port'],
        debug=SERVER_CONFIG['debug']
    )

