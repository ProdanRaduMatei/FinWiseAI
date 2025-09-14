from finwiseai.ml_service.celery_worker import celery_app
import time

@celery_app.task
def train_lstm_task(csv_path: str):
    # Simulate long-running training
    time.sleep(5)
    return {"message": "Training complete", "details": {"csv": csv_path}}