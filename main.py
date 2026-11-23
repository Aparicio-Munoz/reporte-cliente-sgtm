from html import escape
import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).with_name("datos_ficticios_sgtm.csv")
GOLD = "#A98242"
JADE = "#658572"
PAPER = "#F7F5EF"
INK = "#29312C"
MUTED = "#69736B"
GRAPHITE = "#F6F4EF"

st.set_page_config(
    page_title="SGTM | Expediente de servicio",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        --sgtm-gold: #A98242;
        --sgtm-jade: #658572;
        --sgtm-bg: var(--background-color, #F8F7F2);
        --sgtm-panel: var(--secondary-background-color, #F0EEE7);
        --sgtm-ink: var(--text-color, #29312C);
        --sgtm-muted: color-mix(in srgb, var(--sgtm-ink) 68%, var(--sgtm-bg));
        --sgtm-line: color-mix(in srgb, var(--sgtm-ink) 18%, var(--sgtm-bg));
        --sgtm-soft-gold: color-mix(in srgb, var(--sgtm-gold) 13%, var(--sgtm-bg));
        background: var(--sgtm-bg);
        color: var(--sgtm-ink);
        font-family: "Avenir Next", "Segoe UI", sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background: var(--sgtm-bg);
        color: var(--sgtm-ink);
    }

    [data-testid="stHeader"] { background: transparent; }

    .block-container {
        max-width: 1540px;
        padding-top: 1.35rem;
        padding-bottom: 3.2rem;
    }

    [data-testid="stSidebar"] {
        background: var(--sgtm-panel);
        border-right: 1px solid var(--sgtm-line);
    }

    [data-testid="stSidebar"] * { color: var(--sgtm-ink); }

    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {
        background: var(--sgtm-bg) !important;
        color: var(--sgtm-ink) !important;
        border-color: var(--sgtm-line) !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
        background: var(--sgtm-bg);
        border: 1px solid var(--sgtm-line);
    }

    [data-baseweb="popover"], [role="listbox"] {
        background: var(--sgtm-panel) !important;
        color: var(--sgtm-ink) !important;
        border-color: var(--sgtm-line) !important;
    }

    [role="option"] { color: var(--sgtm-ink) !important; }
    [role="option"]:hover { background: var(--sgtm-bg) !important; }

    h1, h2, h3 {
        color: var(--sgtm-ink);
        font-family: "Avenir Next", "Segoe UI", sans-serif;
        letter-spacing: -0.025em;
    }

    .brand-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.8rem;
        padding-bottom: 0.9rem;
        margin-bottom: 1.1rem;
        border-bottom: 1px solid var(--sgtm-line);
    }

    .brand-mark {
        width: 2.45rem;
        height: 2.45rem;
        display: grid;
        place-items: center;
        border: 1px solid var(--sgtm-gold);
        border-radius: 0.25rem;
        background: var(--sgtm-soft-gold);
        color: var(--sgtm-gold);
        font-family: Georgia, serif;
        font-size: 1.25rem;
        font-weight: 700;
    }

    .brand-name {
        color: var(--sgtm-ink);
        font-size: 0.94rem;
        font-weight: 800;
        letter-spacing: 0.16em;
    }

    .brand-subtitle {
        color: var(--sgtm-muted);
        font-size: 0.82rem;
        margin-left: 0.55rem;
    }

    .demo-tag {
        margin-left: 0;
        border: 1px solid var(--sgtm-line);
        border-radius: 999px;
        background: var(--sgtm-soft-gold);
        padding: 0.38rem 0.7rem;
        color: var(--sgtm-gold);
        font-size: 0.75rem;
        letter-spacing: 0.04em;
    }

    .page-title {
        color: var(--sgtm-ink);
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(2.3rem, 4vw, 3.45rem);
        font-weight: 500;
        letter-spacing: -0.045em;
        line-height: 1.05;
        margin: 0;
    }

    .page-deck {
        color: var(--sgtm-muted);
        font-size: 0.98rem;
        margin: 0.55rem 0 1.2rem;
    }

    .profile-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
        padding: 1.55rem 1.8rem;
        background: var(--sgtm-panel);
        border: 1px solid var(--sgtm-line);
        border-top: 2px solid var(--sgtm-gold);
        border-radius: 0.7rem;
        margin: 1.1rem 0 1rem;
    }

    .profile-label {
        color: var(--sgtm-gold);
        font-size: 0.72rem;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .profile-name {
        color: var(--sgtm-ink);
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(1.9rem, 3.2vw, 2.8rem);
        font-weight: 500;
        letter-spacing: -0.035em;
        line-height: 1.05;
        margin: 0 0 0.8rem;
    }

    .profile-facts {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem 1.3rem;
        color: var(--sgtm-muted);
        font-size: 0.88rem;
    }

    .profile-facts strong {
        color: var(--sgtm-ink);
        font-weight: 700;
        margin-right: 0.25rem;
    }

    .profile-subline {
        color: var(--sgtm-muted);
        font-size: 0.84rem;
        margin-top: 0.72rem;
    }

    .plate {
        min-width: 205px;
        padding: 0.8rem 1.15rem 0.9rem;
        border: 2px solid var(--sgtm-gold);
        border-radius: 0.45rem;
        background: var(--sgtm-soft-gold);
        color: var(--sgtm-ink);
        text-align: center;
    }

    .plate-label {
        display: block;
        font-size: 0.6rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        margin-bottom: 0.18rem;
        text-transform: uppercase;
    }

    .plate-value {
        display: block;
        font-family: "SFMono-Regular", Consolas, monospace;
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: 0.12em;
    }

    .section-heading {
        color: var(--sgtm-ink);
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.35rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        margin: 0 0 0.2rem;
    }

    .section-note {
        color: var(--sgtm-muted);
        font-size: 0.82rem;
        margin: 0 0 0.8rem;
    }

    .sidebar-heading {
        color: var(--sgtm-gold);
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.3rem;
        margin: 0.45rem 0 0.15rem;
    }

    .sidebar-copy {
        color: var(--sgtm-muted);
        font-size: 0.82rem;
        line-height: 1.45;
        margin-bottom: 1.1rem;
    }

    .mini-label {
        color: var(--sgtm-muted);
        font-size: 0.72rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }

    .mini-value {
        color: var(--sgtm-ink);
        font-size: 1rem;
        font-weight: 650;
    }

    div[data-testid="stMetric"] {
        background: var(--sgtm-panel);
        border: 1px solid var(--sgtm-line);
        border-top: 2px solid var(--sgtm-gold);
        border-radius: 0.65rem;
        padding: 0.8rem 0.9rem 0.55rem;
        min-height: 98px;
    }

    div[data-testid="stMetric"] label {
        color: var(--sgtm-muted) !important;
        font-size: 0.76rem !important;
        font-weight: 650 !important;
    }

    div[data-testid="stMetricValue"] {
        color: var(--sgtm-gold) !important;
        font-family: "Avenir Next", "Segoe UI", sans-serif;
        font-size: 1.45rem !important;
        font-weight: 700;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--sgtm-panel);
        border: 1px solid var(--sgtm-line);
        border-radius: 0.7rem;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--sgtm-line);
        border-radius: 0.45rem;
    }

    .maintenance-callout {
        border-left: 3px solid var(--sgtm-jade);
        border-radius: 0 0.45rem 0.45rem 0;
        background: color-mix(in srgb, var(--sgtm-jade) 14%, var(--sgtm-bg));
        padding: 1rem 1.1rem;
        margin: 0.5rem 0;
    }

    .maintenance-callout strong {
        color: color-mix(in srgb, var(--sgtm-jade) 70%, var(--sgtm-ink));
    }

    .demo-footnote {
        color: var(--sgtm-muted);
        font-size: 0.76rem;
        margin-top: 1.1rem;
        padding-top: 0.8rem;
        border-top: 1px solid var(--sgtm-line);
    }

    .stButton button, .stDownloadButton button {
        background: var(--sgtm-gold) !important;
        border: 1px solid var(--sgtm-gold) !important;
        color: #232720 !important;
        font-weight: 750 !important;
        border-radius: 0.45rem !important;
    }

    .stButton button:hover, .stDownloadButton button:hover {
        background: #8F6F35 !important;
        border-color: #8F6F35 !important;
    }

    [data-testid="stAlert"] {
        background: var(--sgtm-panel);
        border: 1px solid var(--sgtm-line);
        color: var(--sgtm-ink);
    }

    @media (max-width: 760px) {
        .profile-card {
            align-items: flex-start;
            flex-direction: column;
            padding: 1.2rem;
        }
        .plate { min-width: 175px; }
        .brand-subtitle {
            display: block;
            margin-left: 0;
        }
        .demo-tag { display: none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def escape_value(value) -> str:
    return escape(str(value))


def normalize_column(value: str) -> str:
    return str(value).strip().lower().replace(" ", "_")


def money(value: float) -> str:
    return f"$ {value:,.0f}".replace(",", ".")


def km(value: float) -> str:
    return f"{value:,.0f} km".replace(",", ".")


def spanish_date(value) -> str:
    if pd.isna(value):
        return "Sin fecha"
    months = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ]
    return f"{value.day} de {months[value.month - 1]} de {value.year}"


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        st.error("Falta datos_ficticios_sgtm.csv junto a main.py.")
        st.stop()

    data = pd.read_csv(
        DATA_PATH,
        dtype={"documento": str, "telefono": str, "placa": str},
    )
    data.columns = [normalize_column(column) for column in data.columns]

    required = {
        "cliente_id", "nombre", "documento", "telefono", "placa", "motocicleta",
        "anio_moto", "cilindraje", "color_moto", "kilometraje", "orden", "fecha",
        "servicio", "estado", "tecnico", "mano_obra", "costo_repuestos", "valor",
        "pagado", "proximo_servicio_fecha", "proximo_servicio_km", "observacion",
    }
    missing = required.difference(data.columns)
    if missing:
        st.error("El CSV necesita estas columnas: " + ", ".join(sorted(missing)))
        st.stop()

    data["fecha"] = pd.to_datetime(data["fecha"], format="%Y-%m-%d", errors="coerce")
    data["proximo_servicio_fecha"] = pd.to_datetime(
        data["proximo_servicio_fecha"], format="%Y-%m-%d", errors="coerce"
    )
    numeric_columns = [
        "anio_moto", "cilindraje", "kilometraje", "mano_obra", "costo_repuestos",
        "valor", "pagado", "proximo_servicio_km",
    ]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce").fillna(0)

    data = data.dropna(subset=["fecha", "cliente_id", "nombre"]).copy()
    data["saldo"] = (data["valor"] - data["pagado"]).clip(lower=0)
    return data


data = load_data()
clients = (
    data[["cliente_id", "nombre"]]
    .drop_duplicates(subset=["cliente_id"])
    .sort_values("nombre")
)
client_names = dict(zip(clients["cliente_id"], clients["nombre"]))

st.sidebar.markdown('<div class="sidebar-heading">Expediente</div>', unsafe_allow_html=True)
st.sidebar.markdown(
    '<div class="sidebar-copy">Explora el historial de servicio de un cliente.</div>',
    unsafe_allow_html=True,
)

selected_id = st.sidebar.selectbox(
    "Cliente",
    options=clients["cliente_id"].tolist(),
    format_func=lambda client_id: client_names[client_id],
)

client_data = data.loc[data["cliente_id"] == selected_id].copy().sort_values("fecha")
min_date = client_data["fecha"].min().date()
max_date = client_data["fecha"].max().date()

date_range = st.sidebar.date_input(
    "Período de servicio",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY",
)

states = sorted(client_data["estado"].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "Estado de órdenes",
    options=states,
    default=states,
)
only_balance = st.sidebar.toggle("Mostrar solo con saldo pendiente", value=False)
st.sidebar.markdown("---")
st.sidebar.caption("Demostración académica · todos los registros son ficticios")

st.markdown(
    """
    <div class="brand-row">
        <div class="brand-mark">S</div>
        <div>
            <span class="brand-name">SGTM</span>
            <span class="brand-subtitle">Servicio para tu moto</span>
        </div>
        <span class="demo-tag">Expediente de demostración</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<h1 class="page-title">Expediente de servicio</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-deck">Historial, mantenimiento y cartera del cliente en una sola vista.</p>',
    unsafe_allow_html=True,
)

if len(date_range) != 2:
    st.info("Selecciona una fecha inicial y una final.")
    st.stop()

start_date, end_date = date_range
filtered = client_data.loc[
    client_data["fecha"].dt.date.between(start_date, end_date)
    & client_data["estado"].isin(selected_states)
].copy()
if only_balance:
    filtered = filtered.loc[filtered["saldo"] > 0].copy()

latest = client_data.iloc[-1]
open_count = int((~client_data["estado"].isin(["Entregada", "Cancelada"])).sum())
plate_values = sorted(client_data["placa"].dropna().astype(str).unique().tolist())
plate_text = " / ".join(escape_value(value) for value in plate_values)

st.markdown(
    f"""
    <div class="profile-card">
        <div>
            <div class="profile-label">Perfil seleccionado · registro ficticio</div>
            <div class="profile-name">{escape_value(latest['nombre'])}</div>
            <div class="profile-facts">
                <span><strong>Documento</strong> {escape_value(latest['documento'])}</span>
                <span><strong>Teléfono</strong> {escape_value(latest['telefono'])}</span>
                <span><strong>Código</strong> {escape_value(latest['cliente_id'])}</span>
            </div>
            <div class="profile-subline">
                {escape_value(latest['motocicleta'])} · {int(latest['anio_moto'])} · {int(latest['cilindraje'])} cc
                &nbsp;&nbsp;|&nbsp;&nbsp; {open_count} órdenes abiertas en el historial
            </div>
        </div>
        <div class="plate">
            <span class="plate-label">Placa de demostración</span>
            <span class="plate-value">{plate_text}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

fact_columns = st.columns(4)
facts = [
    ("Año", str(int(latest["anio_moto"]))),
    ("Cilindraje", f"{int(latest['cilindraje'])} cc"),
    ("Color", str(latest["color_moto"])),
    ("Kilometraje registrado", km(latest["kilometraje"])),
]
for column, (label, value) in zip(fact_columns, facts):
    with column:
        st.markdown(
            f'<div class="mini-label">{escape_value(label)}</div><div class="mini-value">{escape_value(value)}</div>',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)
metric_columns = st.columns(5)
order_count = len(filtered)
invoice_total = float(filtered["valor"].sum())
paid_total = float(filtered["pagado"].sum())
balance_total = float(filtered["saldo"].sum())
average_ticket = invoice_total / order_count if order_count else 0
metric_columns[0].metric("Órdenes", f"{order_count}")
metric_columns[1].metric("Valor de servicio", money(invoice_total))
metric_columns[2].metric("Abonado", money(paid_total))
metric_columns[3].metric("Saldo pendiente", money(balance_total))
metric_columns[4].metric("Ticket promedio", money(average_ticket))

st.markdown("<br>", unsafe_allow_html=True)
chart_column, status_column = st.columns([1.35, 0.85], gap="large")

with chart_column:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Actividad financiera</div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-note">Órdenes generadas y abonos recibidos por mes.</p>',
            unsafe_allow_html=True,
        )
        if filtered.empty:
            st.info("No hay órdenes en este período con esos filtros.")
        else:
            monthly = (
                filtered.assign(mes=filtered["fecha"].dt.to_period("M").dt.to_timestamp())
                .groupby("mes", as_index=False)
                .agg(Facturado=("valor", "sum"), Abonado=("pagado", "sum"))
                .melt(id_vars="mes", var_name="tipo", value_name="monto")
            )
            financial_chart = (
                alt.Chart(monthly)
                .mark_bar(size=18, cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
                .encode(
                    x=alt.X("mes:T", title=None, axis=alt.Axis(format="%b %Y", labelAngle=-25)),
                    xOffset=alt.XOffset("tipo:N"),
                    y=alt.Y("monto:Q", title=None, axis=alt.Axis(format=",.0f")),
                    color=alt.Color(
                        "tipo:N",
                        title=None,
                        scale=alt.Scale(domain=["Facturado", "Abonado"], range=[GOLD, JADE]),
                    ),
                    tooltip=[
                        alt.Tooltip("mes:T", title="Mes", format="%Y-%m"),
                        alt.Tooltip("tipo:N", title="Concepto"),
                        alt.Tooltip("monto:Q", title="Valor", format="$,.0f"),
                    ],
                )
                .properties(height=280)
                .configure_view(strokeOpacity=0)
            )
            st.altair_chart(financial_chart, width="stretch")

with status_column:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Órdenes por estado</div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-note">Distribución del período seleccionado.</p>',
            unsafe_allow_html=True,
        )
        if filtered.empty:
            st.info("Sin órdenes para resumir.")
        else:
            status_summary = (
                filtered["estado"].value_counts().rename_axis("estado").reset_index(name="ordenes")
            )
            status_domain = status_summary["estado"].tolist()
            status_palette = [JADE, GOLD, "#B97869", "#8794A0", "#9C83A6"]
            status_chart = (
                alt.Chart(status_summary)
                .mark_arc(innerRadius=62, outerRadius=105, strokeWidth=3)
                .encode(
                    theta=alt.Theta("ordenes:Q", stack=True),
                    color=alt.Color(
                        "estado:N",
                        title=None,
                        scale=alt.Scale(domain=status_domain, range=status_palette[: len(status_domain)]),
                        legend=alt.Legend(orient="bottom", labelLimit=180),
                    ),
                    tooltip=[
                        alt.Tooltip("estado:N", title="Estado"),
                        alt.Tooltip("ordenes:Q", title="Órdenes"),
                    ],
                )
                .properties(height=280)
                .configure_view(strokeOpacity=0)
            )
            st.altair_chart(status_chart, width="stretch")

maintenance_column, cost_column = st.columns([1, 1], gap="large")

with maintenance_column:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Próximo mantenimiento</div>', unsafe_allow_html=True)
        due_date = spanish_date(latest["proximo_servicio_fecha"])
        st.markdown(
            f"""
            <div class="maintenance-callout">
                <div class="mini-label">Recomendado para</div>
                <div class="mini-value">{escape_value(due_date)}</div>
                <div class="profile-subline">Al llegar a {escape_value(km(latest['proximo_servicio_km']))}</div>
            </div>
            <div class="profile-subline">
                Última visita: <strong>{escape_value(spanish_date(latest['fecha']))}</strong>
                &nbsp;&nbsp;·&nbsp;&nbsp; Técnico: <strong>{escape_value(latest['tecnico'])}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

with cost_column:
    with st.container(border=True):
        st.markdown('<div class="section-heading">Composición de costos</div>', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-note">Mano de obra frente a repuestos en el período.</p>',
            unsafe_allow_html=True,
        )
        if filtered.empty:
            st.info("Sin costos para mostrar.")
        else:
            costs = pd.DataFrame(
                {
                    "concepto": ["Mano de obra", "Repuestos"],
                    "valor": [float(filtered["mano_obra"].sum()), float(filtered["costo_repuestos"].sum())],
                }
            )
            cost_chart = (
                alt.Chart(costs)
                .mark_bar(color=GOLD, cornerRadiusEnd=4)
                .encode(
                    x=alt.X("valor:Q", title=None, axis=alt.Axis(format=",.0f")),
                    y=alt.Y("concepto:N", title=None, sort="-x"),
                    tooltip=[
                        alt.Tooltip("concepto:N", title="Concepto"),
                        alt.Tooltip("valor:Q", title="Valor", format="$,.0f"),
                    ],
                )
                .properties(height=145)
                .configure_view(strokeOpacity=0)
            )
            st.altair_chart(cost_chart, width="stretch")

st.markdown("<br>", unsafe_allow_html=True)
with st.container(border=True):
    st.markdown('<div class="section-heading">Historial de órdenes</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-note">Detalle operativo y financiero de cada visita.</p>',
        unsafe_allow_html=True,
    )
    if filtered.empty:
        st.info("Ajusta las fechas o los estados para mostrar órdenes.")
    else:
        ordered = filtered.sort_values("fecha", ascending=False).copy()
        display = pd.DataFrame(
            {
                "Fecha": ordered["fecha"].dt.strftime("%d/%m/%Y"),
                "Orden": ordered["orden"],
                "Placa": ordered["placa"],
                "Servicio": ordered["servicio"],
                "Técnico": ordered["tecnico"],
                "Estado": ordered["estado"],
                "Km ingreso": ordered["kilometraje"].map(lambda value: f"{value:,.0f}".replace(",", ".")),
                "Mano de obra": ordered["mano_obra"].map(money),
                "Repuestos": ordered["costo_repuestos"].map(money),
                "Total": ordered["valor"].map(money),
                "Abonado": ordered["pagado"].map(money),
                "Saldo": ordered["saldo"].map(money),
            }
        )
        st.dataframe(display, hide_index=True, width="stretch", height=390)

        with st.expander("Notas de servicio"):
            for _, row in ordered.iterrows():
                st.markdown(
                    f"**{escape_value(row['orden'])} · {escape_value(row['servicio'])}:** "
                    f"{escape_value(row['observacion'])}"
                )

        csv_data = ordered.to_csv(index=False).encode("utf-8-sig")
        json_payload = {
            "proyecto": "SGTM · reporte de cliente",
            "nota": "Datos ficticios para fines académicos.",
            "filtros": {
                "cliente_id": str(selected_id),
                "fecha_inicio": start_date.isoformat(),
                "fecha_fin": end_date.isoformat(),
                "estados": selected_states,
                "solo_saldos_pendientes": only_balance,
            },
            "resumen": {
                "ordenes": int(len(ordered)),
                "valor_total": float(ordered["valor"].sum()),
                "total_pagado": float(ordered["pagado"].sum()),
                "saldo_pendiente": float(ordered["saldo"].sum()),
            },
            "registros": json.loads(
                ordered.to_json(orient="records", force_ascii=False, date_format="iso")
            ),
        }
        json_data = json.dumps(json_payload, ensure_ascii=False, indent=2).encode("utf-8")

        html_name = escape_value(latest["nombre"])
        html_document = escape_value(latest["documento"])
        html_phone = escape_value(latest["telefono"])
        html_plate = escape_value(latest["placa"])
        html_table = display.to_html(index=False, escape=True, border=0, classes="orders")
        html_data = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Expediente SGTM · {html_name}</title>
<style>
    :root {{ color-scheme: light; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; padding: 36px 18px; background: #f5f3ed; color: #29312c; font-family: Arial, sans-serif; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 34px; background: #fff; border: 1px solid #e5e1d8; border-radius: 16px; box-shadow: 0 10px 32px #29312c0d; }}
    .eyebrow {{ color: #8f6f35; font-size: 12px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }}
    h1 {{ margin: 8px 0; font-family: Georgia, serif; font-size: clamp(30px, 5vw, 46px); font-weight: 500; }}
    .note {{ color: #69736b; }}
    .facts {{ display: flex; flex-wrap: wrap; gap: 10px 24px; margin: 22px 0; padding: 16px; background: #f6f4ef; border-radius: 10px; }}
    h2 {{ margin-top: 30px; font-family: Georgia, serif; font-weight: 500; }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ padding: 11px 10px; border-bottom: 1px solid #e6e2d9; text-align: left; white-space: nowrap; }}
    th {{ background: #f3f0e8; color: #4d574f; }}
    tr:nth-child(even) td {{ background: #fbfaf7; }}
    footer {{ margin-top: 24px; padding-top: 14px; border-top: 1px solid #e6e2d9; color: #737c74; font-size: 12px; }}
    @media print {{ body {{ padding: 0; background: #fff; }} main {{ max-width: none; border: 0; box-shadow: none; }} }}
</style>
</head>
<body>
<main>
    <p class="eyebrow">SGTM · Reporte de demostración</p>
    <h1>Expediente de {html_name}</h1>
    <p class="note">Historial de servicio y resumen financiero del período seleccionado.</p>
    <div class="facts">
        <span><strong>Documento:</strong> {html_document}</span>
        <span><strong>Teléfono:</strong> {html_phone}</span>
        <span><strong>Placa:</strong> {html_plate}</span>
        <span><strong>Período:</strong> {start_date.strftime("%d/%m/%Y")} – {end_date.strftime("%d/%m/%Y")}</span>
        <span><strong>Órdenes:</strong> {len(ordered)}</span>
    </div>
    <h2>Historial de órdenes</h2>
    <div class="table-wrap">{html_table}</div>
    <footer>Los datos de este reporte son ficticios y se usan solo con fines académicos.</footer>
</main>
</body>
</html>"""

        export_columns = st.columns(3)
        with export_columns[0]:
            st.download_button(
                "Descargar CSV",
                data=csv_data,
                file_name=f"expediente_{selected_id}.csv",
                mime="text/csv",
                width="stretch",
            )
        with export_columns[1]:
            st.download_button(
                "Descargar informe HTML",
                data=html_data,
                file_name=f"expediente_{selected_id}.html",
                mime="text/html",
                width="stretch",
            )
        with export_columns[2]:
            st.download_button(
                "Descargar datos JSON",
                data=json_data,
                file_name=f"expediente_{selected_id}.json",
                mime="application/json",
                width="stretch",
            )

st.markdown(
    '<div class="demo-footnote">Datos completamente ficticios para fines académicos. Los documentos, teléfonos, placas, técnicos y órdenes son marcadores de demostración.</div>',
    unsafe_allow_html=True,
)
