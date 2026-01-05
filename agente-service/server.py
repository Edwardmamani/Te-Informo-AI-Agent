"""
Servidor simple con un agente IA usando CrewAI
Ejemplo básico de un agente que puede responder preguntas y realizar tareas
Estructura refactorizada con separación de responsabilidades
"""

import os
import json
from flask import Flask, Response
from flask_cors import CORS
from src.config.settings import SERVER_CONFIG
from src.routers.agent_routes import agent_bp

app = Flask(__name__)
CORS(app)  # Permitir CORS para conectar con el frontend

# Configurar Flask para usar UTF-8 y no escapar caracteres Unicode
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Configurar el encoder JSON personalizado para asegurar UTF-8
class UTF8JSONEncoder(json.JSONEncoder):
    def encode(self, o):
        return super().encode(o)

app.json_encoder = UTF8JSONEncoder

# Registrar los blueprints (rutas)
app.register_blueprint(agent_bp)

# Ruta raíz de salud (mantener compatibilidad)
@app.route('/', methods=['GET'])
def root():
    """Endpoint raíz"""
    response = {"status": "ok", "message": "Servidor de agente IA funcionando"}
    return Response(
        json.dumps(response, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )

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
    print(f"   - POST /agent/generate-news")
    
    app.run(
        host=SERVER_CONFIG['host'],
        port=SERVER_CONFIG['port'],
        debug=SERVER_CONFIG['debug']
    )

