import streamlit as st
import pandas as pd
from utils import color_compound, get_data, render_pilot_box, color_time, format_gap_to_leader, team_colors
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=7000, key="datarefresh")

# Obtener la sesión más reciente
df_sessions = get_data("sessions")
df_sessions["date_start"] = pd.to_datetime(df_sessions["date_start"], errors='coerce')
latest_session = df_sessions.sort_values("date_start").iloc[-1]

df_meetings = get_data("meetings")
latest_meeting = df_meetings[df_meetings["meeting_key"] == latest_session["meeting_key"]].iloc[0]

session_key = latest_session["session_key"]
meeting_key = latest_session["meeting_key"]
params = {"session_key": session_key}
driver_params = {"meeting_key": meeting_key}

# Título del dashboard
st.markdown(f"""
<h1 style='text-align: center; font-size: 30px; font-weight: bold;'>
    Dashboard F1 – {latest_session['year']} {latest_meeting['meeting_name']} ({latest_session['session_name']})
</h1>
""", unsafe_allow_html=True)

# Carga de datos
df_drivers = get_data("drivers", params=driver_params).drop_duplicates(subset=["name_acronym"])
df_laps = get_data("laps", params=params)
df_positions = get_data("position", params=params)
df_stints = get_data("stints", params=params)

# Verificar si la sesión es una carrera
is_race = latest_session["session_type"] == "Race"

# Solo cargar intervalos si es carrera
if is_race:
    df_intervals = get_data("intervals", params=params)
    if df_intervals.empty:
        st.info("No hay datos de intervalos disponibles para esta carrera.")
    else:
        df_intervals["date"] = pd.to_datetime(df_intervals["date"], errors="coerce")
        df_intervals = df_intervals.sort_values(by="date", ascending=False)
        df_intervals = df_intervals.drop_duplicates(subset=["driver_number"], keep="first")
else:
    df_intervals = pd.DataFrame()
    st.info("La sesión seleccionada no es una carrera. Intervalos no disponibles.")

# Preprocesar df_laps
df_laps["date_start"] = pd.to_datetime(df_laps["date_start"], errors="coerce")
df_laps = df_laps.dropna(subset=["lap_number", "date_start", "duration_sector_1"])

# Calcular vueltas completadas por piloto
laps_completed = df_laps.groupby("driver_number")["lap_number"].max().reset_index()
laps_completed.rename(columns={"lap_number": "laps_completed"}, inplace=True)
max_laps = laps_completed["laps_completed"].max()

# Cálculo de mejor vuelta por piloto
df_best_laps = df_laps.sort_values(by="lap_duration").drop_duplicates(subset="driver_number", keep="first")
df_best_laps = df_best_laps[["driver_number", "lap_duration"]].rename(columns={"lap_duration": "best_lap_time"})

# Cálculo de última vuelta por piloto
df_last_laps = df_laps.sort_values(by=["driver_number", "lap_number", "date_start"], ascending=[True, False, False])
df_last_laps = df_last_laps.drop_duplicates(subset="driver_number", keep="first")
df_last_laps = df_last_laps[["driver_number", "lap_duration"]].rename(columns={"lap_duration": "last_lap_time"})

# Última vuelta válida (para compuestos y sectores)
df_laps_sorted = df_laps.sort_values(by=["lap_number", "date_start"], ascending=[False, True])
df_laps = df_laps_sorted.drop_duplicates(subset="driver_number", keep="first")

# Merge con vueltas completadas
df_drivers = df_drivers.merge(laps_completed, on="driver_number", how="left")

# Verificación y merge
if all("driver_number" in df.columns for df in [df_laps, df_positions, df_stints]):
    df_positions["date_start"] = pd.to_datetime(df_positions["date"], errors="coerce")
    df_positions = df_positions.sort_values(by="date_start", ascending=False)
    df_positions = df_positions.drop_duplicates(subset=["driver_number"], keep="first")
    df_stints = df_stints.drop_duplicates(subset=["driver_number"])

    df_merged = df_drivers.merge(df_laps, on="driver_number", how="left")
    df_merged = df_merged.merge(df_positions, on="driver_number", how="left", suffixes=("", "_pos"))
    df_merged = df_merged.merge(df_stints, on="driver_number", how="left", suffixes=("", "_stint"))
    df_merged = df_merged.merge(df_best_laps, on="driver_number", how="left")
    df_merged = df_merged.merge(df_last_laps, on="driver_number", how="left")

    if is_race and not df_intervals.empty:
        df_merged = df_merged.merge(df_intervals, on=["driver_number"], how="left", suffixes=("", "_interval"))

    df_merged = df_merged.sort_values(by=["position", "lap_number", "date_start"], ascending=[True, False, True])
    df_merged = df_merged.drop_duplicates(subset="driver_number", keep="first")

    # Aplicar formato si existe gap_to_leader
    if "gap_to_leader" in df_merged.columns:
        df_merged["gap_to_leader"] = df_merged.apply(
            lambda row: format_gap_to_leader(row["gap_to_leader"], row["laps_completed"], max_laps), axis=1)

    columnas_deseadas = [
        "name_acronym", "driver_number", "position", "compound",
        "best_lap_time", "last_lap_time",
        "duration_sector_1", "duration_sector_2", "duration_sector_3",
        "team_name", "laps_completed", "gap_to_leader"
    ]
    columnas_disponibles = df_merged.columns.tolist()
    columnas_finales = [col for col in columnas_deseadas if col in columnas_disponibles]

    # Eliminar pilotos con datos críticos vacíos
    columnas_criticas = ["team_name", "laps_completed", "compound"]
    df_merged = df_merged.dropna(subset=[col for col in columnas_criticas if col in df_merged.columns])

    df = df_merged[columnas_finales]

    # Aplicar colores
    df["compound"] = df["compound"].apply(color_compound)

    if "best_lap_time" in df.columns:
        df["best_lap_time"] = color_time(df, "best_lap_time", convertir_formato=True)
    if "last_lap_time" in df.columns:
        df["last_lap_time"] = color_time(df, "last_lap_time", convertir_formato=True)

    for col in ["duration_sector_1", "duration_sector_2", "duration_sector_3"]:
        if col in df.columns:
            df[col] = color_time(df, col)

    df["pilot"] = df.apply(lambda row: render_pilot_box(row["driver_number"], row["name_acronym"], row["team_name"]), axis=1)


    # Ordenar columnas
    columnas = ["pilot"] + [col for col in df.columns if col not in ["pilot", "name_acronym", "driver_number"]]
    df = df[columnas]

    # Renombrar columnas para mostrar
    df = df.rename(columns={
        'pilot': 'DRIVER',
        'position': 'POSITION',
        'compound': 'TYRE',
        'duration_sector_1': 'S1',
        'duration_sector_2': 'S2',
        'duration_sector_3': 'S3',
        'team_name': 'TEAM',
        'best_lap_time': 'Best Lap',
        'last_lap_time': 'Last Lap'
    })

# Estilo HTML para la tabla
st.markdown("""
<style>
table, thead, tbody, tr, th, td {
    border: none !important;
}
table {
    border-collapse: collapse !important;
    border-spacing: 0 !important;
    margin: 0 auto !important;
}
td, th {
    text-align: center !important;
    vertical-align: middle !important;
    white-space: nowrap !important;
    background-color: transparent !important;
    padding: 6px 10px !important;
    font-size: 20px;
}
.table-container {
    display: flex;
    justify-content: center;
    width: 100%;
}
@media screen and (max-width: 1024px) {
    td, th {
        font-size: 12px !important;
        padding: 4px 6px !important;
    }
    .table-container {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch;
    }
    .responsive-table-inner {
        min-width: 600px;
    }
}
</style>
""", unsafe_allow_html=True)

# Renderizar tabla
st.markdown(f"""
<div class="table-container">
    <div class="responsive-table-inner">
        {df.to_html(escape=False, index=False, border=0)}
    </div>
</div>
""", unsafe_allow_html=True)
