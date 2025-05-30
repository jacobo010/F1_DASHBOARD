# utils.py

import pandas as pd
import requests

# Función para obtener datos de la API
def get_data(endpoint, params=None):
    base_url = "https://api.openf1.org/v1/"
    response = requests.get(base_url + endpoint, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        return pd.DataFrame()

# Funcuón para aplicar color a los compuestos de neumáticos
# utils.py
def color_compound(val):
    color_map = {
        "SOFT": "red",
        "MEDIUM": "orange",
        "HARD": "grey",
        "INTERMEDIATE": "green",
        "WET": "blue"
    }
    color = color_map.get(val.upper().strip(), "grey")
    return f'<span style="color:{color}; font-weight:bold">{val}</span>'

# Diccionario de colores para los equipos
team_colors = {
    "Red Bull Racing": "#1E41FF",
    "Mercedes": "#00D2BE",
    "Ferrari": "#DC0000",
    "McLaren": "#FF8700",
    "Aston Martin": "#006F62",
    "Alpine": "#0090FF",
    "Williams": "#005AFF",
    "Racing Bulls": "#6692FF",
    "Kick Sauber": "#52E252",
    "Haas F1 Team": "#B6BABD"
}


# Función para renderizar el piloto con su número y nombre
def render_pilot_box(driver_number, name_acronym, team_name):
    color = team_colors.get(team_name, "#888")  # color gris por defecto
    return f"""<div style=" display: inline-flex; align-items: center; justify-content: center; width: 90px; height: 34px; padding: 0 8px; margin: 4px auto; border-radius: 11px; background-color: {color}; color: white; font-weight: bold; font-size: 14px; text-align: center; line-height: 1; font-family: sans-serif; ">{driver_number}&nbsp;&nbsp; {name_acronym}</div>"""


# Punción para pintar los tiempos de las vueltas y sectores. Función con formato de segundos o minutos:segundos.decimas para las vueltas
def color_time(df, columna, convertir_formato=False):
    mejor_global = df[columna].min()
    mejores_personales = df.groupby("driver_number")[columna].min()

    def pintar(valor, piloto):
        if pd.isna(valor):
            return ""
        if convertir_formato:
            minutos = int(valor // 60)
            segundos = int(valor % 60)
            decimas = int((valor - int(valor)) * 1000)
            tiempo_str = f"{minutos}:{segundos:02d}.{decimas:03d}"
        else:
            tiempo_str = f"{valor:.3f}"

        if valor == mejor_global:
            return f'<span style="color: #b300ff; font-weight: bold;">{tiempo_str}</span>'
        elif valor == mejores_personales.get(piloto):
            return f'<span style="color: #00cc44;">{tiempo_str}</span>'
        else:
            return tiempo_str

    return df.apply(lambda row: pintar(row[columna], row["driver_number"]), axis=1)


def format_gap_to_leader(gap, laps_completed, max_laps):
    """
    Formatea la diferencia con el líder:
    - Si es un número, lo devuelve con 3 decimales.
    - Si contiene 'LAP' (como '+1 LAP'), lo deja igual.
    - Si es None pero el piloto tiene menos vueltas que el líder, muestra '+X LAP'.
    - Si no aplica ninguno, devuelve cadena vacía.
    """
    if isinstance(gap, str) and 'LAP' in gap:
        return gap
    try:
        return f"{float(gap):.3f}"
    except:
        try:
            diff = max_laps - int(laps_completed)
            if diff > 0:
                return f"+{diff} LAP"
        except:
            pass
    return ""
