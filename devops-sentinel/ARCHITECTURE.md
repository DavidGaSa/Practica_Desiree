# Arquitectura del proyecto DevOps Sentinel

## Componentes principales

### 1. app.py
Servidor FastAPI con fallos intencionales.
Registra errores en `server_errors.log`.

Endpoints:
- `/` : estado del servidor
- `/divide` : división de dos números
- `/square` : cálculo del cuadrado

### 2. test_app.py
Suite de pruebas unitarias con Pytest.
Define el comportamiento esperado de la aplicación.

### 3. monitor.py
Monitoriza la salud de la API.
Si detecta un error HTTP 500:
- consulta los logs
- invoca un modelo local mediante Ollama
- solicita diagnóstico y propuesta de corrección
- ejecuta `pytest` como barrera de validación

### 4. server_errors.log
Archivo de logs generado por la API cuando se produce una excepción.

### 5. proposed_fix.txt
Archivo donde el modelo deja una propuesta de corrección técnica.

## Flujo de autoreparación

1. El monitor llama a los endpoints críticos.
2. Si detecta un error HTTP 500, activa el análisis.
3. Ollama analiza el log y el archivo `app.py`.
4. Se genera una propuesta de corrección.
5. Se ejecuta `pytest`.
6. Solo si las pruebas pasan, el cambio puede darse por válido.