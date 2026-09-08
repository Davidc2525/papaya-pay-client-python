import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from papaya_pay_client import PapayaClient, construct_event, PapayaWebhookError

app = FastAPI()

# Inicializamos el cliente
papaya = PapayaClient(
    api_key=os.environ.get("PAPAYA_API_KEY", "sk_live_mi_api_key"),
    base_url="http://localhost:80" # Ajustar para pruebas locales
)

AMOUNT_SCALE = 10000.0

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Obtener el raw_body directamente antes de parsearlo a JSON (importante para validación)
    raw_body = await request.body()
    signature_header = request.headers.get("X-Papaya-Signature")
    
    if not signature_header:
        raise HTTPException(status_code=400, detail="Missing signature header")
        
    webhook_secret = os.environ.get("PAPAYA_WEBHOOK_SECRET", "mi_secreto_de_prueba")
    
    try:
        # Validar el evento (levanta excepción si es inválido)
        event = construct_event(raw_body, signature_header, webhook_secret)
        
        print(f"Recibido evento seguro para checkout_id: {event.checkout_id}")
        print(f"Estado: {event.status}")
        
        if event.status == "PAID":
            # Llamamos a la API para obtener los ítems usando el cliente asíncrono no-bloqueante
            # Nota: Al ser `requests` síncrono, para producción en FastAPI deberías usar threadpools (run_in_threadpool).
            # Para este ejemplo se hace de forma síncrona simple.
            print("Consultando API de Papaya...")
            checkout = papaya.checkouts.get(event.checkout_id)
            
            print(f"Pedido Interno (external_reference): {checkout.external_reference}")
            print("Ítems pagados:")
            for item in checkout.items:
                print(f" - {item.quantity}x {item.name} (VES: {item.unit_price_ves_cents / AMOUNT_SCALE} | USDC: {item.unit_price_usdc_cents / AMOUNT_SCALE})")
                
        return JSONResponse(content={"received": True})
        
    except PapayaWebhookError as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Internal error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
