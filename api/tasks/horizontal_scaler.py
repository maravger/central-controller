from __future__ import absolute_import, unicode_literals
from logging import Logger
from api.views import optimizer
from api.views import workload_predictor
from django.conf import settings
from api.models import App
from django.core.exceptions import ObjectDoesNotExist
import requests
import logging
from celery import task

# Get an instance of a logger
logger = logging.getLogger(__name__)  # type: Logger

@task()
def scale_horizontally():
    print "Scaling Horizontally (task)"
    # TODO find a better way to initiate app creation
    for app_id in settings.GLOBAL_SETTINGS['APPS']:
        try:
            App.objects.get(app_id=app_id)
        except ObjectDoesNotExist:
            temp = App(app_id=app_id)
            temp.save()
    if len(settings.GLOBAL_SETTINGS['HOST_IPS'])>2 :
	print "pame lig"
	total_combinations = optimizer.permutate_ntua()
    else:
	total_combinations = optimizer.permutate()
    print "Total available combinations: " + str(total_combinations)
    predicted_workload = workload_predictor.predict()
    print "Predicted Workload for apps: " + str(predicted_workload)
    # set fire_optimizer = None if for both apps previous predicted rr does not differ from next predicted by a Threshold
    fire_optimizer = next ((app_id for app_id in (settings.GLOBAL_SETTINGS['APPS']) if (abs(App.objects.get(app_id=app_id).next_predicted_rr - App.objects.get(app_id=app_id).previous_predicted_rr) >= settings.GLOBAL_SETTINGS['OPTIMIZER_THRESHOLD']) ), None)
    if (fire_optimizer != None) or (App.objects.get(app_id="0").containers_op_list=="NaN"):
	print "fire!" 
        if App.objects.get(app_id="0").containers_op_list != "NaN": 
	    if sum(App.objects.get(app_id="0").get_containers_op_list())==0 :
	        print "Set [4,4] beacause of first use!!"
	        selected_combinations = []
	        selected_combinations.append([4,4])
	        for i in range (len(settings.GLOBAL_SETTINGS['HOST_IPS'])-1):
	            selected_combinations.append([0,0])
         
	if len(settings.GLOBAL_SETTINGS['HOST_IPS'])>2 :
    	    selected_combinations = optimizer.optimize_ntua(total_combinations, predicted_workload)
    	else:
    	    selected_combinations = optimizer.optimize(total_combinations, predicted_workload)
	print "Selected combination: " + str(selected_combinations)
    elif (sum(predicted_workload)==0):
        print "Zero Predicted Workload"
	selected_combinations = []
	for i in range (len(settings.GLOBAL_SETTINGS['HOST_IPS'])):
	    selected_combinations.append([0,0])
    else:
	print "use previous combinations"
	selected_combinations = []
	for i in range (len(settings.GLOBAL_SETTINGS['HOST_IPS'])):
	    temp = []
	    for app_id in (settings.GLOBAL_SETTINGS['APPS']):
	        temp.append(App.objects.get(app_id=app_id).get_containers_op_list()[i])
	    selected_combinations.append(temp)
    print selected_combinations
    # Save combination choices to each app object.
    for app_id in (settings.GLOBAL_SETTINGS['APPS']):
        containers_op_list = []
        for combination in selected_combinations:
            containers_op_list.append(combination[app_id])
        app = App.objects.get(app_id=app_id)
        app.set_containers_op_list(containers_op_list)
        app.save()
    # Deploy the combinations in a FCFS manner.
    # Selected combinations always << than available servers (guaranteed by the optimizer).
    # Edgy controller expected to be running in :8001.
    host = iter(settings.GLOBAL_SETTINGS['HOST_IPS'])
    for combination in selected_combinations:
        # print("Scaling Host with IP: " + host)
        headers = {'Content-Type': 'application/json', }
        data = '{"combination":' + str(combination) + '}'
        try:
            response = requests.post('http://' + next(host) + ':8003/edgy_controller/vertical_scaling/', headers=headers, data=data, timeout=5.5)
            print 'Vertical Scaling Response: ' + str(response)
        except (requests.Timeout, requests.ConnectionError):
            print('Host unavailable.')
            pass
    # !!! DEPRECATED !!! selected_combinations variable now contains shutdown hosts as [0,0]
    # Now shutdown the unused containers in the rest of the Hosts.
    # for i in range(len(settings.GLOBAL_SETTINGS['HOST_IPS']) - len(selected_combinations)):
    #     print 'Shutting down rest of Hosts'
    #     headers = {'Content-Type': 'application/json', }
    #     data = '{"combination": [0,0]}'
    #     # Catch "end of list" exception
    #     try:
    #         response = requests.post('http://' + next(host) + ':8001/edgy_controller/vertical_scaling/', headers=headers, data=data, timeout=1.5)
    #         print response
    #     except StopIteration:
    #         break
    #     except requests.Timeout:
    #         print('Host unavailable.')
    #         pass
    print("Finished scaling Hosts.")
    
