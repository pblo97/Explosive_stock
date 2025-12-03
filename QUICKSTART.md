# ⚡ Quick Start Guide

## 5 Minutos para Empezar

### 1. Obtén tu API Key (2 minutos)

1. Ve a https://financialmodelingprep.com
2. Crea cuenta gratis
3. Copia tu API key del dashboard

### 2. Configura el Proyecto (1 minuto)

```bash
# Instala dependencias
pip install -r requirements.txt

# Edita config.py
nano config.py
```

En `config.py`, cambia:
```python
FMP_API_KEY = "pega_tu_api_key_aqui"
```

### 3. Ejecuta la App (1 minuto)

```bash
streamlit run app.py
```

Se abrirá en tu navegador: `http://localhost:8501`

### 4. Encuentra Acciones Explosivas (1 minuto)

1. En la app, ve a tab "🔍 Market Scan"
2. Click en "🚀 Start Scan"
3. ¡Listo! Verás las acciones con mayor potencial

## 🎯 Interpretación Rápida

### Qué Buscar

✅ **Score 70+** = Señal FUERTE
✅ **RVOL 2-4x** = Volumen ideal (NO >5x)
✅ **OBV trending UP** = Acumulación
✅ **RSI 40-70** = No sobrecomprado
✅ **Sin risk flags** = Más seguro

### Qué Evitar

❌ Score <30
❌ RVOL >5x (posible pump & dump)
❌ RSI >80 (muy sobrecomprado)
❌ Risk flag: "PUMP RISK"
❌ Baja liquidez (<$500K dollar volume)

## 📱 Uso Diario Recomendado

### Mañana (9:30 AM - apertura del mercado)

```bash
streamlit run app.py
```

1. Ejecuta market scan
2. Revisa top 5-10 picks
3. Verifica risk flags
4. Anota símbolos con score >70

### Durante el Día

1. Tab "📊 Analyze Symbol"
2. Ingresa símbolos de tu watchlist
3. Verifica si score sigue alto
4. Observa cambios en RVOL y OBV

### Tips

- **Mejor hora**: Primera hora de trading (9:30-10:30 AM EST)
- **Volumen**: Busca RVOL aumentando progresivamente
- **OBV**: Si OBV sube pero precio no = momento ideal
- **Stop-loss**: SIEMPRE usa stop loss al 5-7% abajo de entrada

## 🔥 Ejemplo de Señal Perfecta

```
TICKER: XYZ
Score: 82/100 🚀 STRONG

✅ RVOL: 3.1x (volumen fuerte entrando)
✅ OBV: Trending UP (acumulación)
✅ RSI: 55 (zona neutral, espacio para subir)
✅ Precio $3.20 vs VWAP $3.05 (sobre soporte)
✅ Float: 25M (fácil de mover)
✅ Sin risk flags

ACCIÓN: Agregar a watchlist, esperar confirmación
```

## ⚠️ Ejemplo de EVITAR

```
TICKER: SCAM
Score: 40/100 📊 WEAK

❌ RVOL: 8.5x (EXTREMO - posible pump)
❌ OBV: Trending DOWN (distribución)
❌ RSI: 92 (MUY sobrecomprado)
⚠️  Risk: PUMP RISK - Ultra low float + extreme volume
⚠️  Risk: Extremely overbought

ACCIÓN: EVITAR - demasiadas red flags
```

## 🛠️ Troubleshooting Rápido

**"No API key" error**
→ Edita `config.py` con tu API key real

**No encuentra acciones**
→ Baja el "Minimum Score" a 30-40

**Muy lento**
→ Reduce "Max Stocks to Analyze" a 20-30

**Error de conexión**
→ Verifica internet y que API key sea válida

## 📚 Siguiente Paso

Lee el `README.md` completo para entender:
- Metodología detallada
- Por qué funcionan estos indicadores
- Cómo interpretar cada métrica
- Estrategias de riesgo

## 💡 Consejo de Oro

> **El mejor movimiento explosivo es el que atrapas TEMPRANO.**
> Busca: OBV trending UP + RVOL 2-3x + Precio AÚN NO explotó = 💎

---

**¿Listo?** Ejecuta `streamlit run app.py` y empieza a detectar! 🚀
