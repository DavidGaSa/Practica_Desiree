from fastapi import FastAPI, HTTPException
import logging

app = FastAPI()

logging.basicConfig(
    filename="server_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.get("/")
def home():
    return {"message": "Servidor activo"}

@app.get("/divide")
def divide(a: int, b: int):
    try:
        result = a / b
        return {"result": result}
    except Exception as e:
        logging.error(f"Error en /divide con a={a}, b={b}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno en divide")

@app.get("/square")
def square(x: int):
    try:
        if x < 0:
            raise ValueError("No se permiten valores negativos")
        return {"result": x * x}
    except Exception as e:
        logging.error(f"Error en /square con x={x}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno en square")