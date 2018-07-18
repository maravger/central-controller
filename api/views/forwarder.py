from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import App
from django.conf import settings
import random
import requests


@api_view(['POST'])
@permission_classes((AllowAny, ))
def post(request, slug=None):
    # TODO: test for asynchronous requests
    # slug == app_id
    if slug == "0" or slug == "1":
        app = App.objects.get(app_id=slug)
        containers_op_list = app.get_containers_op_list()
        print ("Operating Points of Containers currently running App " + slug + " : "  + str(containers_op_list))
        # Match operating points to request processing capabilities
        request_procc_cap = map(lambda op: settings.GLOBAL_SETTINGS['U_REQ_MAX'][int(slug)][op], containers_op_list)
        print ("Respective request processing capabilities: " + str(request_procc_cap))
        # Create total request capabilities
        total_requests_capability = sum(request_procc_cap)
        print ("Total request processing capabilities: " + str(total_requests_capability))
        # Create possibilities by dividing each request capability with total requests capabilities
        possibilities = map(lambda pc: pc/total_requests_capability, request_procc_cap)
        print ("Respective possibilities of the request being offloaded to container: " + str(possibilities))
        # Create a list containing the cumulative sum of the possibilities
        cumsum_possibilities = reduce(lambda c, x: c + [c[-1] + x], possibilities, [0])[1:]
        print ("Respective cumulative sum of possibilities: " + str(cumsum_possibilities))
        # Seed a random uniform number
        rand = random.uniform(0, 1)
        print ("Random number to select container: " + str(rand))
        # Offload request to container dictated by rand
        host_id = next(i for i, v in enumerate(cumsum_possibilities) if v > rand)
        print ("Actual selected Host ID: " + str(host_id))
        # app0 is running on :8001 & app1 on 8002
        resp = offload(slug, host_id, request)
        return Response({'Response' : resp})
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


def offload(app_id, host_id, request):
    size = request.data['size']
    print ("Size: " + str(size) + "B")
    pts = request.data['start_time']
    print ("Timestamp: " + str(pts))
    img = request.data['file']
    print ("Image name: " + img.name)
    print ("------------------------------------------------------------\n")
    json = {"size": size, "start_time": pts}
    files = {"file": img}
    post_url = "http://" + settings.GLOBAL_SETTINGS['HOST_IPS'][host_id]  + ":" + str(8001+int(app_id)) + "/ca_tf/imageUpload/" + img.name
    try:
        return requests.post(post_url, files=files, data=json, timeout=15)
    except (requests.Timeout, requests.ConnectionError):
        print('Host at ' + settings.GLOBAL_SETTINGS['HOST_IPS'][host_id]  + ' unavailable.')
        #return Response({'Response': status=status.HTTP_404_NOT_FOUND})
        return 'Host unavailable.'
