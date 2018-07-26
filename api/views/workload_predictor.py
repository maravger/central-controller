from api.models import App
from django.conf import settings
import requests


def predict():
    predicted_workload = []
    # Gather app stats.
    for host_ip in settings.GLOBAL_SETTINGS['HOST_IPS']:
        print('Gathering app stats from host with IP: ' + host_ip)
        try:
            response = requests.get('http://' + host_ip + ':8003/edgy_controller/app_stats/', timeout=1.5)
            new_apps_stats = response.json()
            # Sum apps stats per App. You won't understand this line tomorrow :)
            try:
                apps_stats = {k: {l: apps_stats.get(k).get(l) + new_apps_stats.get(k).get(l)
                     for l in set(apps_stats.get(k))} for k in set(apps_stats)}
            # If this is the first time apps_stats is used, assign the data received to it.
            except NameError:
                apps_stats = new_apps_stats
        except (requests.Timeout, requests.ConnectionError):
            print('Host unavailable.')
            continue
        print apps_stats
    for app_id in settings.GLOBAL_SETTINGS['APPS']:
        app = App.objects.get(app_id=app_id)
        try:
            predicted_workload.append(app.predict_next_rr(apps_stats['app' + str(app_id)]))
        except KeyError as e:
            print('Stats unavailable for ' + str(e))
            predicted_workload.append(0)
    return predicted_workload