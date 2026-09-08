# Papaya Python SDK

SDK oficial de Papaya para Python. Cliente HTTP síncrono (usando `requests`) y validación segura de Webhooks.

## Requisitos
- Python 3.8+

## Instalación

```bash
# 1. Crear entorno virtual (Recomendado)
python3 -m venv venv
source venv/bin/activate

# 2. Instalación para desarrollo local:
pip install -e .

# 3. Instalación de dependencias del ejemplo:
pip install fastapi uvicorn
```

## Uso

### 1. Cliente API (Checkouts)
```python
from papaya_pay_client import PapayaClient

papaya = PapayaClient(api_key="sk_live_...")

checkout = papaya.checkouts.get("ID_DEL_CHECKOUT")
print(checkout.items)
```

### 2. Validación de Webhooks
```python
from papaya_pay_client import construct_event

# raw_body debe ser `bytes`
event = construct_event(raw_body, signature_header, "tu_webhook_secret")
```

## Correr el Ejemplo (FastAPI)

```bash
cd libs/python
uvicorn examples.fastapi_app:app --host 0.0.0.0 --port 8181 --reload
```
