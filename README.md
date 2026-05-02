# CardioRisk 🫀
### Sistema de Diagnóstico Cardiovascular
**Heart Disease UCI Dataset · Especialización Diseño e IA**

---

## Archivos del proyecto

```
cardiorisk/
├── app.py            ← App principal Streamlit
├── heart.csv         ← Dataset Heart Disease UCI (Kaggle)
├── requirements.txt  ← Dependencias Python
└── README.md
```

---

## Ejecutar localmente

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar
streamlit run app.py
```

La app abre en `http://localhost:8501`

---

## Publicar en Streamlit Cloud (gratis)

1. Crea un repositorio en GitHub con los 4 archivos
2. Ve a **[share.streamlit.io](https://share.streamlit.io)**
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio y el archivo `app.py`
5. Clic en **Deploy** → tu URL pública queda lista en ~2 min

---

## Funcionalidades

| Pestaña | Contenido |
|---|---|
| 📊 Dashboard | Métricas, gráfica de dona, barras por edad y sexo, tabla de promedios |
| 🩺 Simulador | Sliders interactivos + clasificación en tiempo real con desglose if/elif/else |

## Paleta clínica

| Nivel | Color | Hex |
|---|---|---|
| BAJO | Teal clínico | `#2A9D8F` |
| MODERADO | Azul acero | `#457B9D` |
| ALTO | Ámbar cálido | `#E07A3A` |
| CRÍTICO | Rojo desaturado | `#C0444A` |

---

*Algoritmo académico — no tiene uso clínico real.*
