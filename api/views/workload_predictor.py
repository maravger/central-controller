from api.models import App
from django.conf import settings


def predict():
    predicted_workload = []
    for app_id in settings.GLOBAL_SETTINGS['APPS']:
        app = App.objects.get(app_id=app_id)
        predicted_workload.append(app.predict_next_rr())
    return predicted_workload
