from flask import Flask
from supabase import create_client
import os

app = Flask(__name__)

# Variables de entorno
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("⚠️ SUPABASE_URL y SUPABASE_KEY no están configuradas")

# Conectar a Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    try:
        # Consultar la tabla
        response = supabase.table('entradas_soporte').select('*').execute()
        registros = response.data
        
        # Construir HTML
        html = """
        <html>
        <head>
            <title>Sistema de Soporte</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
                h1 { color: #333; }
                table { border-collapse: collapse; width: 100%; background: white; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
            </style>
        </head>
        <body>
            <h1>Sistema de Tickets de Soporte Técnico</h1>
            <p>Conectado exitosamente a Supabase</p>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Usuario</th>
                    <th>Problema</th>
                    <th>Estado</th>
                </tr>
        """
        
        for fila in registros:
            html += f"<tr><td>{fila['id']}</td><td>{fila['usuario']}</td><td>{fila['problema']}</td><td>{fila['estado']}</td></tr>"
            
        html += """
            </table>
        </body>
        </html>
        """
        return html
    except Exception as e:
        return f"<h1>Error:</h1> <p>{str(e)}</p>"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
