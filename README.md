# 🏎️ F1_DASHBOARD
[**F1_DASHBOARD**](https://f1dashhboard.streamlit.app/) is a web application built with **Streamlit** that uses real-time data from the [OpenF1 API](https://www.openf1.org/) to display up-to-date statistics about drivers and teams during Formula 1 sessions (qualifying, races, etc.). The dashboard refreshes every 5 seconds to provide the most recent results possible.

```
F1_DASHBOARD/
│
├── main.py # Main dashboard code
├── utils.py # Helper functions (colors, data, driver rendering)
├── README.md # This file
└── requirements.txt # Project dependencies
```
---

## Preview

The app features a **real-time dashboard** displaying:

- Driver name and number with team color  
- Tyre compound used  
- Lap and sector times  
- Track position  
- Gap to the leader (`gap_to_leader`)  
- Laps completed  

---

## Technologies used

- [Streamlit](https://streamlit.io/) to run and periodically refresh the app  
- [Pandas](https://pandas.pydata.org/) to clean, filter, and structure the data  
- HTML + CSS to build and style the main dashboard table  

---

## Run the project locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jacobo010/F1_DASHBOARD.git
   cd F1_DASHBOARD

2. **Install the dependencies from requirements.txt**:

    ```bash
    pip install -r requirements.txt

3. **Run the app from the terminal**

    ```bash
    streamlit run main.py


---


# 🏎️ F1_DASHBOARD

[**F1_DASHBOARD**](https://f1dashhboard.streamlit.app/) es una aplicación desarrollada con **Streamlit** que utiliza datos en tiempo real desde la [API OpenF1](https://www.openf1.org/), con el objetivo de mostrar estadísticas actualizadas de pilotos y equipos durante las sesiones de Fórmula 1 (qualis, carreras, etc.). El dashboard se actualiza cada 5 segundos para obtener los resultados más recientes posibles.

```
F1_DASHBOARD/
│
├── main.py           # Código principal del dashboard
├── utils.py          # Funciones auxiliares (colores, datos, render de pilotos)
├── README.md         # Este archivo
└── requirements.txt  # Dependencias del proyecto
```
---

## Vista previa

La aplicación presenta un **dashboard en tiempo real** con:

- Nombre y número de piloto, con su color de equipo
- Compuesto de neumáticos usado
- Tiempos de vuelta y de sectores
- Posición en pista
- Diferencia con el líder (`gap_to_leader`)
- Vueltas completadas

---

## Tecnologías utilizadas

- [Streamlit](https://streamlit.io/) para poder ejecutar la app y actulizarla cada cierto tiempo.
- [Pandas](https://pandas.pydata.org/) para limpiar, filtrar y estructurar los datos.
- HTML + CSS para la creación de la tabla principal del dashboard y estilo visual de la misma.

---

## Ejecutar el proyecto en local

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/jacobo010/F1_DASHBOARD.git
   cd F1_DASHBOARD

2. **Descarga las dependencias de requirements.txt**

    ```bash
    pip install -r requirements.txt

3. **Ejecutar el programa en la terminal**

    ```bash
    streamlit run main.py