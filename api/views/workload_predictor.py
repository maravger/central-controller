from api.models import App
from django.conf import settings
import requests
import json
import csv
import os

def predict():
    predicted_workload = []
    # Gather app stats.
    for host_ip in settings.GLOBAL_SETTINGS['HOST_IPS']:
        print('Gathering app stats from host with IP: ' + host_ip)
        try:
            response = requests.get('http://' + host_ip + ':8003/edgy_controller/app_stats/', timeout=1.5)
            new_apps_stats = response.json()
	    print new_apps_stats
	    for app_key , app in new_apps_stats.iteritems():
		app["average_response_time"] = float(app["average_response_time"]) * float(app["requests_finished"])
		app["average_transmission_time"] = float(app["average_transmission_time"]) * float(app["requests_finished"])
		app["average_computation_time"] = float(app["average_computation_time"]) * float(app["requests_finished"])
            # Sum apps stats per App. You won't understand this line tomorrow :)
            try:
                apps_stats = {k: {l: apps_stats.get(k).get(l) + new_apps_stats.get(k).get(l)
                     for l in set(apps_stats.get(k))} for k in set(apps_stats)}
		apps_stats.get
            # If this is the first time apps_stats is used, assign the data received to it.
            except NameError:
                apps_stats = new_apps_stats
        except (requests.Timeout, requests.ConnectionError):
            print('Host unavailable.')
            continue
    for app_key , app in apps_stats.iteritems():
	if float(app["requests_finished"])== 0 :
	    continue
	app["average_response_time"] = float(app["average_response_time"]) / float(app["requests_finished"])
	app["average_transmission_time"] = float(app["average_transmission_time"]) / float(app["requests_finished"])
	app["average_computation_time"] = float(app["average_computation_time"]) / float(app["requests_finished"])
    print apps_stats
		
       
	####### save to csv file
    for app_key  , app in apps_stats.iteritems():
    	temp_json = app
    	filename = "./sum_stats_"+app_key
    	with open(filename, 'a') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            # If opened for the first time, insert header row
            if os.path.getsize(filename) == 0:
                wr.writerow(["requests_submitted", "requests_finished", "requests_rejected","average_response_time", "average_transmission_time", "average_computation_time","average_cpu_usage", "number_of_pes"])
            wr.writerow([temp_json.get("requests_submitted"),temp_json.get("requests_finished"),temp_json.get("requests_rejected"),temp_json.get("average_response_time"),temp_json.get("average_transmission_time"),temp_json.get("average_computation_time"),temp_json.get("average_cpu_usage"), temp_json.get("number_of_pes")])
        ########## end of saving to csv

    for app_id in settings.GLOBAL_SETTINGS['APPS']:
        app = App.objects.get(app_id=app_id)
        try:
            predicted_workload.append(app.predict_next_rr(apps_stats['app' + str(app_id)]))
        except KeyError as e:
            print('Stats unavailable for ' + str(e))
            predicted_workload.append(0)
    return predicted_workload
