import requests
import subprocess
import time
from pathlib import Path

URLS = [
    "http://127.0.0.1:8000/divide?a=10&b=0"
]

MIN_LOGS = 10
CHECK_INTERVAL = 2  # segundos entre intentos

def read_file(filepath):
    path = Path(filepath)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""

def count_log_lines(filepath="server_errors.log"):
    path = Path(filepath)
    if not path.exists():
        return 0

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return 0

    return len(content.splitlines())

def generate_report_manually(failed_url, total_logs):
    logs = read_file("server_errors.log")
    app_code = read_file("app.py")

    report = f"""DIAGNOSTICO:
Se ha detectado un error HTTP 500 en el endpoint monitorizado: {failed_url}

El monitor ha esperado hasta acumular al menos {MIN_LOGS} registros en server_errors.log.
Actualmente se han detectado {total_logs} líneas de log.

El análisis de los logs indica que la API está lanzando una excepción no controlada
o provocada por una entrada inválida. Esto genera un fallo interno del servidor
y queda registrado en server_errors.log.

CORRECCION PROPUESTA:
- Añadir validación previa de los parámetros de entrada.
- Controlar explícitamente las excepciones en los endpoints.
- Devolver respuestas HTTP controladas mediante HTTPException.
- Mantener el registro del error en el archivo de logs para trazabilidad.

INFORME DE REFACTORIZACION:
- Separar la lógica de negocio de los endpoints para mejorar mantenibilidad.
- Añadir más pruebas unitarias para casos límite y entradas inválidas.
- Mejorar el detalle de los mensajes de log para facilitar el diagnóstico.
- Evitar repetir bloques try/except si se puede centralizar el manejo de errores.

LOGS ANALIZADOS:
{logs}

CODIGO ANALIZADO:
{app_code}
"""
    Path("proposed_fix.txt").write_text(report, encoding="utf-8")
    print("Informe guardado en proposed_fix.txt")

def run_pytest():
    result = subprocess.run(
        ["pytest"],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    output = f"""=== STDOUT ===
{result.stdout}

=== STDERR ===
{result.stderr}

=== RETURN CODE ===
{result.returncode}
"""
    Path("pytest_result.txt").write_text(output, encoding="utf-8")

    print("Resultado de pytest guardado en pytest_result.txt")
    return result.returncode == 0

def monitor_until_10_logs():
    print("Iniciando monitor de salud...")
    print(f"Objetivo: acumular al menos {MIN_LOGS} logs antes de generar el informe.")

    last_failed_url = None

    while True:
        for url in URLS:
            try:
                response = requests.get(url, timeout=5)
                print(f"{url} -> {response.status_code}")

                if response.status_code >= 500:
                    last_failed_url = url
                    total_logs = count_log_lines()

                    print(f"Fallo detectado en {url}")
                    print(f"Logs acumulados: {total_logs}/{MIN_LOGS}")

                    if total_logs >= MIN_LOGS:
                        print("Se ha alcanzado el mínimo de logs requerido.")
                        generate_report_manually(last_failed_url, total_logs)

                        print("Ejecutando pruebas...")
                        tests_ok = run_pytest()

                        if tests_ok:
                            print("Las pruebas pasan correctamente.")
                        else:
                            print("Las pruebas fallan.")

                        return

            except Exception as e:
                error_report = f"""DIAGNOSTICO:
Se produjo un error durante la monitorización del endpoint: {url}

DETALLE DEL ERROR:
{str(e)}

CORRECCION PROPUESTA:
- Verificar que el servidor FastAPI está levantado.
- Comprobar que la URL es correcta.
- Revisar conectividad local y puerto 8000.
"""
                Path("proposed_fix.txt").write_text(error_report, encoding="utf-8")
                print(f"Error monitorizando {url}: {e}")
                print("Informe de error guardado en proposed_fix.txt")
                return

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_until_10_logs()