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
        # 1. Consultar la tabla desde Supabase
        response = supabase.table('entradas_soporte').select('*').execute()
        registros = response.data
        
        # 2. Construir HTML con los datos
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sistema de Soporte</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    margin: 40px; 
                    background-color: #f4f4f9; 
                }
                h1 { 
                    color: #333; 
                    text-align: center;
                }
                .success {
                    background-color: #d4edda;
                    color: #155724;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    text-align: center;
                }
                table { 
                    border-collapse: collapse; 
                    width: 100%; 
                    background: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                th, td { 
                    border: 1px solid #ddd; 
                    padding: 12px; 
                    text-align: left; 
                }
                th { 
                    background-color: #4CAF50; 
                    color: white;
                    font-weight: bold;
                }
                tr:hover {
                    background-color: #f5f5f5;
                }
            </style>
        </head>
        <body>
            <h1>🎫 Sistema de Tickets de Soporte Técnico</h1>
            <div class="success">
                ✅ Conectado exitosamente a Supabase (Capa 2)
            </div>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Usuario</th>
                    <th>Problema</th>
                    <th>Estado</th>
                </tr>
        """
        
        # 3. Insertar registros en la tabla
        if registros:
            for fila in registros:
                html += f"""
                <tr>
                    <td>{fila.get('id', 'N/A')}</td>
                    <td>{fila.get('usuario', 'N/A')}</td>
                    <td>{fila.get('problema', 'N/A')}</td>
                    <td>{fila.get('estado', 'N/A')}</td>
                </tr>
                """
        else:
            html += "<tr><td colspan='4' style='text-align:center; color:#999;'>No hay registros disponibles</td></tr>"
        
        html += """
            </table>
            <p style='margin-top: 20px; text-align: center; color: #666;'>
                <small>Capa 1: Interfaz Web | Capa 2: Base de Datos PostgreSQL en Supabase</small>
            </p>
        </body>
        </html>
        """
        return html
        
    except Exception as e:
        return f"""
        <html>
        <head>
            <title>Error</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .error {{ background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>❌ Error de conexión:</h1>
                <p><strong>{str(e)}</strong></p>
            </div>
        </body>
        </html>
        """

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
