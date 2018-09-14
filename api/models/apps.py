from django.db import models
from django.conf import settings
import json

SAMPLING_INTERVAL = settings.GLOBAL_SETTINGS['SAMPLING_INTERVAL']


class App(models.Model):
    s = models.FloatField(default=0)  # Predictor-specific value
    b = models.FloatField(default=0)  # Predictor-specific value
    app_id = models.IntegerField(default=0, unique=True)
    prev_subm = models.IntegerField(default=0)  # Requests submitted in last interval
    prev_rej = models.IntegerField(default=0)  # Requests rejected in last interval
    next_predicted_rr = models.FloatField(default=0)  # Request Rate Limit predicted for the next interval (vertical scaling)
    previous_predicted_rr = models.FloatField(default=0)  # Request Rate Limit predicted for last interval (vertical scaling)
    containers_op_list = models.CharField(max_length=10, default = "NaN")  # A (String) list containing the operating points of the containers running this app

    def __unicode__(self):
        return self.cont_id

    def predict_next_rr(self, app_stats):
        self.prev_subm = app_stats['requests_submitted']
        self.prev_rej = app_stats['requests_rejected']
        alpha = 0.5
        v = 0.5
        # Get an instance of a logger
        print("Predicting for App: " + str(self.app_id))
        print("Totally admitted: " + str(self.prev_subm + self.prev_rej))
        prev_real_rr = round(float(self.prev_subm + self.prev_rej) / SAMPLING_INTERVAL, 2)
        print("Previous Real Request Rate: " + str(prev_real_rr))
        s = alpha * prev_real_rr + (1 - alpha) * (self.s - self.b)
        print("s = " + str(s))
        self.b = v * (s - self.s) + (1 - v) * self.b
        print("b = " + str(self.b))
        self.s = round(s + self.b, 2)
        print("Predicted Request Rate: " + str(self.s) + "\n")
        self.previous_predicted_rr = self.next_predicted_rr
        self.next_predicted_rr = self.s
        self.save()
        return self.next_predicted_rr

    def set_containers_op_list(self, op_list):
        self.containers_op_list = json.dumps(op_list)

    def get_containers_op_list(self):
        return json.loads(self.containers_op_list)
