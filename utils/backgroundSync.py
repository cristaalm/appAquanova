import time

def background_sync(historial_controller):
    while True:
        historial_controller.sync_pending_historial()
        time.sleep(60)  # Espera 60 segundos antes de volver a intentar