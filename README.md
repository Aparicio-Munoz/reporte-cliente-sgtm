# Reporte interactivo de clientes SGTM

Aplicación académica de Streamlit para explorar un expediente de servicio. Incluye filtros, métricas, gráficos y exportación CSV, HTML y JSON. Toda la información del CSV es ficticia.

## Archivos necesarios

- `main.py`: aplicación Streamlit.
- `datos_ficticios_sgtm.csv`: registros sintéticos de clientes, motos y órdenes.
- `requirements.txt`: dependencias fijadas a las versiones usadas en el Mac.
- `.streamlit/config.toml`: tema claro.

No subas `.venv`, `datos.csv` ni información real de clientes al repositorio.

## Ejecutar en macOS

En VS Code, abre la terminal en esta carpeta. Activa el entorno si no aparece `(.venv)` en la terminal:

```bash
source .venv/bin/activate
```

Inicia la aplicación:

```bash
python -m streamlit run main.py
```

## Exportaciones

Tras escoger cliente, fechas y estados, descarga el resultado filtrado en tres formatos:

- **CSV**: abre en Excel o Numbers.
- **HTML**: informe estilizado que se abre en Safari o Brave y puede imprimirse como PDF.
- **JSON**: datos estructurados con filtros, resumen y registros.

El HTML presenta los valores para lectura; el JSON conserva números y fechas para reutilizarlos en otros sistemas.

## Publicar en Streamlit Community Cloud

1. Crea un repositorio GitHub para este proyecto.
2. Sube `main.py`, `datos_ficticios_sgtm.csv`, `requirements.txt`, `.gitignore`, `README.md` y `.streamlit/config.toml`.
3. Entra en `https://share.streamlit.io/` con GitHub y selecciona **Create app**.
4. Elige el repositorio, la rama `main` y `main.py` como archivo de entrada.
5. En **Advanced settings**, selecciona Python 3.14 para que coincida con el entorno local.
6. Pulsa **Deploy** y guarda el enlace `.streamlit.app` para compartirlo con la profesora.

El repositorio y la aplicación publicada usan exclusivamente datos ficticios de demostración.
