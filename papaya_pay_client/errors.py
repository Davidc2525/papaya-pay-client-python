class PapayaError(Exception):
    """Clase base para errores del SDK de Papaya."""
    pass

class PapayaAPIError(PapayaError):
    """Lanzada cuando la API responde con un error HTTP."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"Papaya API Error {status_code}: {message}")

class PapayaWebhookError(PapayaError):
    """Clase base para errores de webhooks."""
    pass

class InvalidSignatureFormat(PapayaWebhookError):
    """El formato del header de la firma es inválido."""
    pass

class ToleranceExceeded(PapayaWebhookError):
    """El timestamp del webhook excede la tolerancia permitida."""
    pass

class SignatureMismatch(PapayaWebhookError):
    """Las firmas no coinciden."""
    pass
