# =============================================================
# CardioRisk — Diagnóstico Cardiovascular
# Streamlit App · Heart Disease UCI Dataset
# Especialización Diseño e IA
# =============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Configuración de página ─────────────────────────────────
st.set_page_config(
    page_title="CardioRisk · Diagnóstico Cardiovascular",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Paleta clínica ──────────────────────────────────────────
COLORS = {
    "BAJO":     "#2A9D8F",
    "MODERADO": "#457B9D",
    "ALTO":     "#E07A3A",
    "CRÍTICO":  "#C0444A",
}
BG_COLORS = {
    "BAJO":     "#EAF7F5",
    "MODERADO": "#EBF2F8",
    "ALTO":     "#FDF1E8",
    "CRÍTICO":  "#FBEAEA",
}
TEXT_COLORS = {
    "BAJO":     "#1B7A6E",
    "MODERADO": "#2C5F7A",
    "ALTO":     "#A85520",
    "CRÍTICO":  "#8B2A2E",
}

# ── Estilos globales ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Header principal */
.cardio-header {
    background: linear-gradient(135deg, #0F4C6A 0%, #1A6B8A 60%, #2A9D8F 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
}
.cardio-header h1 {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 2.2rem;
    color: white;
    margin: 0;
    letter-spacing: -0.5px;
    line-height: 1.1;
}
.cardio-header p {
    color: rgba(255,255,255,0.75);
    font-size: 0.9rem;
    margin: 6px 0 0;
    font-weight: 300;
}
.header-icon {
    font-size: 3rem;
    line-height: 1;
}
.header-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.9);
    font-size: 0.7rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 8px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* Métrica card */
.metric-card {
    background: white;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    border-top: 3px solid var(--top-color, #2A9D8F);
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    height: 100%;
}
.metric-card .label {
    font-size: 0.7rem;
    font-weight: 500;
    color: #8A97A8;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 8px;
}
.metric-card .value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #0D1B2A;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-card .note {
    font-size: 0.75rem;
    color: #8A97A8;
    font-weight: 300;
}

/* Nivel resultado */
.nivel-card {
    border-radius: 14px;
    padding: 1.75rem;
    text-align: center;
    margin-bottom: 1rem;
}
.nivel-card .nivel-label {
    font-size: 0.7rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
    opacity: 0.7;
}
.nivel-card .nivel-value {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    line-height: 1;
    margin-bottom: 8px;
    letter-spacing: -1px;
}
.nivel-card .nivel-score {
    font-size: 0.85rem;
    opacity: 0.65;
    font-weight: 300;
}

/* Desglose paso */
.step-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    border-bottom: 1px solid rgba(0,0,0,0.06);
    font-size: 0.82rem;
}
.step-row:last-child { border-bottom: none; }
.step-name { flex: 1; color: #4A5568; }
.step-pts { font-weight: 500; color: #0D1B2A; min-width: 28px; text-align: right; }

/* Recomendación */
.rec-box {
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.82rem;
    line-height: 1.55;
    margin-bottom: 1rem;
    font-weight: 400;
}

/* Footer */
.footer-bar {
    background: white;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 0.75rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.75rem;
    color: #8A97A8;
    margin-top: 2rem;
}
.footer-pill {
    background: #EAF7F5;
    color: #1B7A6E;
    font-size: 0.65rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Sección títulos */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: #0D1B2A;
    letter-spacing: -0.3px;
    margin-bottom: 0.25rem;
}
.section-sub {
    font-size: 0.8rem;
    color: #8A97A8;
    font-weight: 300;
    margin-bottom: 1.5rem;
}

/* Ocultar elementos Streamlit */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 0; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# LÓGICA DEL ALGORITMO
# ══════════════════════════════════════════════════════════════

def clasificar_riesgo(edad, presion, colesterol, fc_max, angina):
    """
    Clasifica el riesgo cardiovascular usando estructuras if/elif/else.
    Retorna nivel, puntaje y desglose paso a paso.
    """
    puntos = 0
    steps = []

    # --- Edad ---
    if edad >= 65:
        puntos += 3; steps.append(("Edad ≥ 65 años", 3, 3))
    elif edad >= 50:
        puntos += 2; steps.append(("Edad 50–64 años", 2, 3))
    elif edad >= 40:
        puntos += 1; steps.append(("Edad 40–49 años", 1, 3))
    else:
        steps.append(("Edad < 40 años", 0, 3))

    # --- Presión arterial ---
    if presion > 160:
        puntos += 3; steps.append(("Presión > 160 mmHg", 3, 3))
    elif presion > 140:
        puntos += 2; steps.append(("Presión 141–160 mmHg", 2, 3))
    elif presion > 120:
        puntos += 1; steps.append(("Presión 121–140 mmHg", 1, 3))
    else:
        steps.append(("Presión ≤ 120 mmHg", 0, 3))

    # --- Colesterol ---
    if colesterol > 280:
        puntos += 2; steps.append(("Colesterol > 280 mg/dl", 2, 2))
    elif colesterol > 200:
        puntos += 1; steps.append(("Colesterol 201–280 mg/dl", 1, 2))
    else:
        steps.append(("Colesterol ≤ 200 mg/dl", 0, 2))

    # --- Frecuencia cardíaca máxima ---
    if fc_max < 100:
        puntos += 2; steps.append(("FC máx < 100 bpm", 2, 2))
    elif fc_max < 130:
        puntos += 1; steps.append(("FC máx 100–129 bpm", 1, 2))
    else:
        steps.append(("FC máx ≥ 130 bpm", 0, 2))

    # --- Angina ---
    if angina == 1:
        puntos += 2; steps.append(("Angina por ejercicio: sí", 2, 2))
    else:
        steps.append(("Angina por ejercicio: no", 0, 2))

    # --- Clasificación final ---
    if puntos <= 2:
        nivel = "BAJO"
    elif puntos <= 5:
        nivel = "MODERADO"
    elif puntos <= 8:
        nivel = "ALTO"
    else:
        nivel = "CRÍTICO"

    return nivel, puntos, steps


def procesar_dataset(df):
    """Aplica el clasificador a todo el dataset con un bucle for."""
    resultados = []
    for _, fila in df.iterrows():
        nivel, _, _ = clasificar_riesgo(
            fila["age"], fila["trestbps"],
            fila["chol"], fila["thalach"], fila["exang"]
        )
        resultados.append(nivel)
    df = df.copy()
    df["riesgo"] = resultados
    return df


# ══════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════

@st.cache_data
def cargar_datos():
    df = pd.read_csv("heart.csv")
    df = procesar_dataset(df)
    bins   = [0, 40, 50, 60, 70, 100]
    labels = ["< 40", "40–49", "50–59", "60–69", "70+"]
    df["grupo_edad"] = pd.cut(df["age"], bins=bins, labels=labels)
    return df

try:
    df = cargar_datos()
    data_ok = True
except FileNotFoundError:
    data_ok = False


# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div class="cardio-header">
  <div class="header-icon">🫀</div>
  <div>
    <h1>CardioRisk</h1>
    <p>Sistema de diagnóstico cardiovascular · Heart Disease UCI Dataset · Kaggle</p>
    <span class="header-badge">🟢 &nbsp;Especialización Diseño e IA · 2025</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# NAVEGACIÓN
# ══════════════════════════════════════════════════════════════

tab1, tab2 = st.tabs(["📊  Dashboard del dataset", "🩺  Simulador de diagnóstico"])


# ══════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════

with tab1:
    st.markdown('<p class="section-title">Análisis de riesgo cardiovascular</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">303 pacientes clasificados por el algoritmo de puntuación clínica · Heart Disease UCI</p>', unsafe_allow_html=True)

    if not data_ok:
        st.error("⚠️  No se encontró **heart.csv**. Coloca el archivo en la misma carpeta que `app.py` y recarga la página.")
        st.stop()

    # ── Métricas ──────────────────────────────────────────────
    conteos = df["riesgo"].value_counts()
    alto_critico = conteos.get("ALTO", 0) + conteos.get("CRÍTICO", 0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card" style="--top-color:#1A6B8A">
            <div class="label">Total pacientes</div>
            <div class="value">{len(df)}</div>
            <div class="note">Dataset Heart Disease UCI</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card" style="--top-color:#C0444A">
            <div class="label">Riesgo Alto + Crítico</div>
            <div class="value">{alto_critico}</div>
            <div class="note">{alto_critico/len(df)*100:.1f}% del dataset</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card" style="--top-color:#2A9D8F">
            <div class="label">Edad promedio</div>
            <div class="value">{df['age'].mean():.1f}</div>
            <div class="note">Rango: {df['age'].min()} — {df['age'].max()} años</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        con_enfermedad = int(df["target"].sum())
        st.markdown(f"""<div class="metric-card" style="--top-color:#E07A3A">
            <div class="label">Con enfermedad cardíaca</div>
            <div class="value">{con_enfermedad}</div>
            <div class="note">{con_enfermedad/len(df)*100:.1f}% — target = 1</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Fila 1: Dona + Barras edad ───────────────────────────
    c1, c2 = st.columns(2)

    with c1:
        orden = ["BAJO", "MODERADO", "ALTO", "CRÍTICO"]
        valores = [conteos.get(n, 0) for n in orden]
        colores = [COLORS[n] for n in orden]

        fig_dona = go.Figure(go.Pie(
            labels=orden,
            values=valores,
            hole=0.62,
            marker=dict(colors=colores, line=dict(color="white", width=3)),
            hovertemplate="<b>%{label}</b><br>%{value} pacientes (%{percent})<extra></extra>",
            textinfo="none",
        ))
        fig_dona.update_layout(
            title=dict(text="Distribución por nivel de riesgo", font=dict(size=13, color="#4A5568"), x=0),
            showlegend=True,
            legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center",
                        font=dict(size=11, color="#4A5568")),
            margin=dict(t=40, b=40, l=10, r=10),
            height=300,
            paper_bgcolor="white",
            plot_bgcolor="white",
            annotations=[dict(text=f"<b>{len(df)}</b><br><span style='font-size:10px'>pacientes</span>",
                              x=0.5, y=0.5, font_size=16, showarrow=False,
                              font=dict(color="#0D1B2A"))]
        )
        st.plotly_chart(fig_dona, use_container_width=True)

    with c2:
        grupos = ["< 40", "40–49", "50–59", "60–69", "70+"]
        data_edad = df.groupby(["grupo_edad", "riesgo"], observed=True).size().reset_index(name="n")

        fig_edad = go.Figure()
        for nivel in orden:
            sub = data_edad[data_edad["riesgo"] == nivel]
            vals = []
            for g in grupos:
                row = sub[sub["grupo_edad"] == g]
                vals.append(int(row["n"].values[0]) if len(row) else 0)
            fig_edad.add_trace(go.Bar(
                name=nivel, x=grupos, y=vals,
                marker_color=COLORS[nivel],
                hovertemplate=f"<b>{nivel}</b><br>%{{x}}: %{{y}} pacientes<extra></extra>"
            ))
        fig_edad.update_layout(
            barmode="stack",
            title=dict(text="Riesgo por grupo de edad", font=dict(size=13, color="#4A5568"), x=0),
            showlegend=True,
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                        font=dict(size=11, color="#4A5568")),
            margin=dict(t=40, b=50, l=10, r=10),
            height=300,
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#8A97A8"),
                       linecolor="rgba(0,0,0,0)"),
            yaxis=dict(gridcolor="rgba(0,0,0,0.05)", tickfont=dict(size=11, color="#8A97A8"),
                       linecolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_edad, use_container_width=True)

    # ── Fila 2: Barras sexo + Tabla promedios ────────────────
    c3, c4 = st.columns(2)

    with c3:
        data_sexo = df.groupby(["sex", "riesgo"]).size().reset_index(name="n")
        sexos = [0, 1]
        labels_sexo = ["Mujer (0)", "Hombre (1)"]

        fig_sexo = go.Figure()
        for nivel in orden:
            sub = data_sexo[data_sexo["riesgo"] == nivel]
            vals = []
            for s in sexos:
                row = sub[sub["sex"] == s]
                vals.append(int(row["n"].values[0]) if len(row) else 0)
            fig_sexo.add_trace(go.Bar(
                name=nivel, x=labels_sexo, y=vals,
                marker_color=COLORS[nivel],
                hovertemplate=f"<b>{nivel}</b><br>%{{x}}: %{{y}} pacientes<extra></extra>"
            ))
        fig_sexo.update_layout(
            barmode="stack",
            title=dict(text="Riesgo por sexo biológico", font=dict(size=13, color="#4A5568"), x=0),
            showlegend=True,
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center",
                        font=dict(size=11, color="#4A5568")),
            margin=dict(t=40, b=50, l=10, r=10),
            height=280,
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(showgrid=False, tickfont=dict(size=12, color="#8A97A8"),
                       linecolor="rgba(0,0,0,0)"),
            yaxis=dict(gridcolor="rgba(0,0,0,0.05)", tickfont=dict(size=11, color="#8A97A8"),
                       linecolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_sexo, use_container_width=True)

    with c4:
        st.markdown("**Promedios clínicos por nivel de riesgo**")
        st.markdown("<br>", unsafe_allow_html=True)
        avg = (df.groupby("riesgo")[["age", "trestbps", "chol", "thalach"]]
               .mean().round(1).reindex(orden).reset_index())
        avg.columns = ["Nivel", "Edad", "Presión", "Colesterol", "FC máx"]

        def color_nivel(val):
            c = TEXT_COLORS.get(val, "#4A5568")
            bg = BG_COLORS.get(val, "#F4F6F8")
            return f'background-color:{bg};color:{c};font-weight:500;border-radius:20px;padding:3px 10px;font-size:0.75rem'

        styled = avg.style.map(color_nivel, subset=["Nivel"]).format({
            "Edad": "{:.1f}", "Presión": "{:.1f}",
            "Colesterol": "{:.1f}", "FC máx": "{:.1f}"
        }).set_properties(**{
            "font-size": "13px", "color": "#4A5568"
        }).set_table_styles([
            {"selector": "th", "props": [("font-size", "11px"), ("color", "#8A97A8"),
                                          ("font-weight", "500"), ("text-transform", "uppercase"),
                                          ("letter-spacing", "0.06em")]}
        ])
        st.dataframe(styled, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# TAB 2 — SIMULADOR
# ══════════════════════════════════════════════════════════════

with tab2:
    st.markdown('<p class="section-title">Simulador de diagnóstico</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Ajusta los parámetros clínicos y el algoritmo if/elif/else clasifica el nivel de riesgo en tiempo real</p>', unsafe_allow_html=True)

    col_in, col_out = st.columns([1, 1], gap="large")

    with col_in:
        st.markdown("##### Datos del paciente")

        edad     = st.slider("Edad (años)", 25, 80, 54, 1)
        presion  = st.slider("Presión arterial en reposo (mmHg — trestbps)", 90, 200, 130, 1)
        colest   = st.slider("Colesterol sérico (mg/dl — chol)", 120, 400, 240, 1)
        fc_max   = st.slider("Frecuencia cardíaca máxima (bpm — thalach)", 70, 210, 155, 1)
        angina   = st.radio(
            "Angina inducida por ejercicio (exang)",
            options=[0, 1],
            format_func=lambda x: "No (0)" if x == 0 else "Sí (1)",
            horizontal=True,
        )

        evaluar = st.button("🫀  Evaluar riesgo cardiovascular", use_container_width=True, type="primary")

    with col_out:
        st.markdown("##### Resultado del algoritmo")

        if evaluar or True:   # muestra resultado desde el inicio
            nivel, puntos, steps = clasificar_riesgo(edad, presion, colest, fc_max, angina)
            color   = COLORS[nivel]
            bg      = BG_COLORS[nivel]
            txt_col = TEXT_COLORS[nivel]

            RECS = {
                "BAJO":     "✅  Mantener hábitos saludables. Control preventivo anual recomendado.",
                "MODERADO": "ℹ️  Consultar médico en los próximos meses. Revisar dieta y actividad física.",
                "ALTO":     "⚠️  Se recomienda atención médica pronta. Evaluar tratamiento preventivo.",
                "CRÍTICO":  "🚨  Requiere atención urgente. Consultar a un especialista de inmediato.",
            }

            # Hero nivel
            st.markdown(f"""
            <div class="nivel-card" style="background:{bg}">
                <div class="nivel-label" style="color:{txt_col}">nivel de riesgo</div>
                <div class="nivel-value" style="color:{color}">{nivel}</div>
                <div class="nivel-score" style="color:{txt_col}">Puntaje: {puntos} / 12 puntos</div>
            </div>
            """, unsafe_allow_html=True)

            # Recomendación
            st.markdown(f"""
            <div class="rec-box" style="background:{bg};color:{txt_col}">
                {RECS[nivel]}
            </div>
            """, unsafe_allow_html=True)

            # Gauge de puntaje
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=puntos,
                number={"suffix": " pts", "font": {"size": 24, "color": color}},
                gauge={
                    "axis": {"range": [0, 12], "tickwidth": 1, "tickcolor": "#8A97A8",
                             "tickfont": {"size": 10}},
                    "bar": {"color": color, "thickness": 0.25},
                    "bgcolor": "#F4F6F8",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 2],  "color": "#EAF7F5"},
                        {"range": [2, 5],  "color": "#EBF2F8"},
                        {"range": [5, 8],  "color": "#FDF1E8"},
                        {"range": [8, 12], "color": "#FBEAEA"},
                    ],
                    "threshold": {"line": {"color": color, "width": 3},
                                  "thickness": 0.8, "value": puntos}
                }
            ))
            fig_gauge.update_layout(
                height=160, margin=dict(t=10, b=0, l=20, r=20),
                paper_bgcolor="white"
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Desglose if/elif/else
            st.markdown("**Desglose del algoritmo** `if / elif / else`")
            rows_html = ""
            for nombre, pts, maximo in steps:
                pct = int(pts / maximo * 100) if maximo > 0 else 0
                bar_color = color if pts > 0 else "#E2E8F0"
                rows_html += f"""
                <div class="step-row">
                    <span class="step-name">{nombre}</span>
                    <div style="width:80px;height:5px;background:#EEF1F5;border-radius:3px;overflow:hidden">
                        <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:3px"></div>
                    </div>
                    <span class="step-pts" style="color:{''+color if pts>0 else '#8A97A8'}">+{pts}</span>
                </div>"""
            st.markdown(f"""
            <div style="background:white;border:1px solid rgba(0,0,0,0.07);border-radius:12px;padding:1rem 1.25rem">
                {rows_html}
                <div style="display:flex;justify-content:space-between;padding:10px 0 0;
                            font-size:0.85rem;font-weight:500;color:#0D1B2A;
                            border-top:1px solid rgba(0,0,0,0.1);margin-top:6px">
                    <span>Total de puntos</span><span>{puntos} / 12</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    <span>Dataset: Heart Disease UCI · Kaggle · 303 pacientes · 14 variables</span>
    <span class="footer-pill">⚕ Algoritmo académico — no uso clínico</span>
    <span>Especialización Diseño e IA · 2025</span>
</div>
""", unsafe_allow_html=True)
