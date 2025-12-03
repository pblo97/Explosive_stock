# 🚀 Explosive Penny Stock Detector

Detecta penny stocks (chicharros) con potencial explosivo de +20% usando análisis basado en evidencia científica y experiencia real de traders.

## 🎯 Características

### Análisis Basado en Evidencia Real

Este sistema NO usa indicadores tradicionales que no funcionan. Usa lo que **realmente funciona** según investigación de 2024:

✅ **Volumen Relativo (RVOL)** - El indicador #1 más importante
✅ **On-Balance Volume (OBV)** - Detecta acumulación temprana
✅ **Análisis de Float** - Float bajo = más fácil mover el precio
✅ **VWAP** - Usado por casi todos los traders profesionales
✅ **RSI** - Solo para evitar sobrecompra (81% precisión)

❌ **MACD** - Eliminado (solo 56% precisión, demasiado lento)

### Sistema de Puntuación (0-100)

**Tier 1 - Crítico (60 puntos):**
- RVOL 2-4x: 25 pts
- OBV trending up: 20 pts
- Float < 50M: 15 pts

**Tier 2 - Importante (30 puntos):**
- Precio sobre VWAP: 15 pts
- Volume Spike: 10 pts
- Dollar Volume >$1M: 5 pts

**Tier 3 - Complementario (10 puntos):**
- RSI 40-70: 7 pts
- Price Momentum +5-20%: 3 pts

### Detección de Pump & Dump

El sistema identifica automáticamente señales de riesgo:
- ⚠️ Float ultra bajo (<10M) + RVOL extremo (>5x)
- ⚠️ Movimientos parabólicos (+50% en un día)
- ⚠️ RSI extremo (>80)
- ⚠️ Divergencia OBV vs Precio
- ⚠️ Baja liquidez (Dollar Volume <$500K)

## 📋 Requisitos

- Python 3.8+
- API Key de Financial Modeling Prep (FMP)
  - Obtén una gratis en: https://financialmodelingprep.com

## 🚀 Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/explosive_stock.git
cd explosive_stock

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API Key
# Edita config.py y añade tu API key de FMP
nano config.py
# Cambia: FMP_API_KEY = "tu_api_key_aqui"
```

## 💻 Uso

### Iniciar la Aplicación Streamlit

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

### 1. Market Scanner

Escanea el mercado completo buscando acciones explosivas:

1. Configura filtros en la barra lateral:
   - Exchange (NASDAQ, NYSE, AMEX, OTC o todos)
   - Score mínimo (recomendado: 40-50)
   - Máximo de acciones a analizar

2. Click en "🚀 Start Scan"

3. Revisa los resultados ordenados por score

4. El "Top Pick" muestra análisis detallado + gráfico

### 2. Analyze Symbol

Analiza un símbolo específico:

1. Ingresa el símbolo (ej: "AAPL")
2. Click en "Analyze"
3. Revisa score, breakdown y métricas clave

### 3. Interpretar Resultados

**Señales de Fuerza:**
- 🚀 **STRONG (70+)**: Alto potencial explosivo - VIGILAR
- 📈 **MODERATE (50-69)**: Vale la pena monitorear
- 📊 **WEAK (30-49)**: Setup marginal
- ⛔ **AVOID (<30)**: Sin señal clara

**Qué Buscar:**
1. RVOL entre 2-4x (NO más de 5x = riesgo de pump)
2. OBV trending UP mientras precio aún no explotó
3. RSI entre 40-70 (evitar >80)
4. Float < 50M acciones
5. Pocas o ninguna risk flag

## 📊 Ejemplos de Uso

### Caso Ideal

```
Symbol: XYZZ
Score: 85/100 🚀 STRONG

Tier 1 (55/60):
- RVOL: 3.2x ✅
- OBV: Trending UP ✅
- Float: 18M shares ✅

Tier 2 (25/30):
- Price $2.15 above VWAP $2.05 ✅
- Volume spike: +250% ✅
- Dollar volume: $2.3M ✅

Tier 3 (5/10):
- RSI: 58 ✅
- 5D change: +8% ✅

Risk Flags: None ✅
```

**Interpretación:** Setup perfecto. Volumen entrando, OBV acumulando, no sobrecomprado. Alta probabilidad de movimiento explosivo.

### Caso de Pump & Dump (EVITAR)

```
Symbol: SCAM
Score: 45/100 📊 WEAK

Tier 1 (25/60):
- RVOL: 8.5x ⚠️ EXTREMO
- OBV: Trending DOWN ❌
- Float: 5M shares ⚠️ ULTRA BAJO

Risk Flags:
⚠️ PUMP RISK: Ultra low float + extreme volume
⚠️ Extremely overbought (RSI: 92)
⚠️ Parabolic move - might be too late
```

**Interpretación:** Evitar. Señales claras de pump & dump.

## 🏗️ Estructura del Proyecto

```
explosive_stock/
├── app.py                    # Aplicación Streamlit principal
├── config.py                 # Configuración y API keys
├── requirements.txt          # Dependencias
├── modules/
│   ├── fmp_api.py           # Cliente API de FMP
│   ├── screener.py          # Lógica principal de screening
│   ├── indicators.py        # Cálculo de indicadores técnicos
│   └── scorer.py            # Sistema de puntuación
└── utils/
    └── helpers.py           # Funciones de formato y utilidades
```

## 📚 Metodología y Fundamentos

### ¿Por qué estos indicadores?

Basado en investigación académica y consenso de traders 2024-2025:

1. **Volumen es el Rey**
   - "Volume is THE most important indicator for penny stocks" (PennyStocks.com, 2024)
   - RVOL >2x usado por traders profesionales (Warrior Trading)
   - Volumen + precio = 90% más confiable que otros indicadores

2. **OBV - Señal Temprana**
   - Detecta acumulación institucional
   - OBV up antes que precio = mejor momento de entrada
   - Más efectivo que MACD para penny stocks

3. **Float Analysis**
   - Float <20M = alta volatilidad
   - Float <10M = riesgo pump & dump
   - Consenso entre traders activos

4. **VWAP**
   - "Almost every trader uses VWAP" (análisis 2024)
   - Precio sobre VWAP = zona de soporte institucional

5. **RSI (uso limitado)**
   - 81% precisión según estudio 2024
   - Solo para evitar sobrecompra (>80)
   - NO como señal principal de entrada

### ¿Por qué NO MACD?

- Solo 56% precisión en estudio académico 2024
- Indicador retrasado (lagging)
- En penny stocks que se mueven 20-50% en minutos, MACD llega tarde
- Traders profesionales no lo usan como indicador principal

## ⚠️ Advertencias y Riesgos

### Este NO es Consejo Financiero

Esta herramienta es para análisis educativo. Penny stocks son **EXTREMADAMENTE RIESGOSOS**:

❌ Pueden perder 50% tan rápido como suben
❌ Baja liquidez - difícil salir de posiciones
❌ Alto riesgo de manipulación (pump & dump)
❌ Muchas quiebran o valen $0

### Recomendaciones

✅ Usa solo capital que puedas perder
✅ SIEMPRE usa stop-loss
✅ No inviertas más del 1-2% de tu capital por acción
✅ Haz tu propia investigación (DYOR)
✅ Entiende que score alto ≠ garantía de ganancia

## 🔧 Personalización

### Modificar Pesos del Score

Edita `config.py`:

```python
WEIGHTS = {
    'rvol': 25,           # Ajusta estos valores
    'obv': 20,            # Total debe sumar 100
    'float': 15,
    'vwap': 15,
    'volume_spike': 10,
    'dollar_volume': 5,
    'rsi': 7,
    'price_momentum': 3
}
```

### Modificar Filtros Base

```python
MIN_PRICE = 0.50          # Precio mínimo
MAX_PRICE = 10.0          # Precio máximo
MAX_MARKET_CAP = 300_000_000  # Market cap máximo
MIN_VOLUME = 100_000      # Volumen mínimo
```

## 🐛 Troubleshooting

### Error: "No quote data"
- Verifica que tu API key sea válida
- Algunos símbolos no tienen datos en FMP
- Verifica límites de rate de tu plan FMP

### Escaneo muy lento
- Reduce `max_stocks` en la configuración
- Upgrade a plan FMP premium para más requests/minuto

### No encuentra acciones
- Baja el `min_score`
- Cambia filtros de exchange
- Verifica que existan penny stocks activas ese día

## 📈 Roadmap Futuro

- [ ] Alertas por email/Telegram cuando score >70
- [ ] Backtesting histórico
- [ ] Machine learning para mejorar pesos
- [ ] Integración con más exchanges
- [ ] Modo paper trading

## 📄 Licencia

MIT License - Usa bajo tu propio riesgo

## 🙏 Créditos

Basado en investigación y consenso de:
- PennyStocks.com (2024 research)
- Warrior Trading (RVOL methodology)
- ResearchGate studies on RSI/MACD effectiveness
- Financial Modeling Prep API

---

**⚡ Remember:** The best explosive move is the one you catch early. Volume + OBV = Your edge.

**⚠️ Disclaimer:** Past performance doesn't guarantee future results. Trade responsibly.
