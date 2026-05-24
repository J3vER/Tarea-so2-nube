from flask import Flask
import psycopg2

app = Flask(__name__)

# Tu cadena de conexión de Supabase (¡Borra los corchetes al poner tu contraseña!)
DB_URL = "postgresql://postgres:Taller1212.*@1@db.hlhuqkmiojiaffmxdqdc.supabase.co:5432/postgres"

@app.route('/')
def index():
    try:
        # 1. Conectarnos a la Capa 2 (Base de Datos)
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        
        # 2. Ejecutar la consulta
        cursor.execute("SELECT * FROM entradas_soporte;")
        registros = cursor.fetchall()
        
        # 3. Cerrar conexión
        cursor.close()
        conn.close()
        
        # 4. Construir la Capa 1 (Interfaz Web en HTML)
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
            <h1>Sistema de Tickets de Soporte Técnico (Capa 1)</h1>
            <p>Conectado exitosamente a la base de datos PostgreSQL en la nube (Capa 2).</p>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Usuario</th>
                    <th>Problema</th>
                    <th>Estado</th>
                </tr>
        """
        
        # Insertar los datos de la base de datos en la tabla HTML
        for fila in registros:
            html += f"<tr><td>{fila[0]}</td><td>{fila[1]}</td><td>{fila[2]}</td><td>{fila[3]}</td></tr>"
            
        html += """
            </table>
        </body>
        </html>
        """
        return html

    except Exception as e:
        return f"<h1>Error de conexión:</h1> <p>{e}</p>"

# Esta línea es para pruebas locales, en PythonAnywhere no interferirá
if __name__ == '__main__':
    app.run(debug=True)