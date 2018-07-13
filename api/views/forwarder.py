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
    if slug == "0":
        app = App.objects.get(app_id=slug)
        containers_op_list = app.get_containers_op_list()
        print str(containers_op_list)
        # Match operating points to request processing capabilities
        request_procc_cap = map(lambda op: settings.GLOBAL_SETTINGS['U_REQ_MAX'][int(slug)][op], containers_op_list)
        print str(request_procc_cap)
        # Create total request capabilities
        total_requests_capability = sum(request_procc_cap)
        print total_requests_capability
        # Create possibilities by dividing each request capability with total requests capabilities
        possibilities = map(lambda pc: pc/total_requests_capability, request_procc_cap)
        print possibilities
        # Create a list containing the cumulative sum of the possibilities
        cumsum_possibilities = reduce(lambda c, x: c + [c[-1] + x], possibilities, [0])[1:]
        print cumsum_possibilities
        # Seed a random uniform number
        rand = random.uniform(0, 1)
        print rand
        # Offload request to container dictated by rand
        container_id = next(i for i, v in enumerate(cumsum_possibilities) if v > rand)
        print container_id
        # app0 is running on :8800 & app1 on 8801
        resp = offload(slug, container_id, request)
        return Response(resp)
        # return Response(status=status.HTTP_204_NO_CONTENT)
    elif slug == "1":
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


def offload(app_id, container_id, request):
    size = request.data['size']
    print size
    pts = request.data['start_time']
    print pts
    img = request.data['file']
    print img.name
    json = {"size": size, "start_time": pts}
    files = {"file": img}
    # post_url = "http://0.0.0.0:880" + str(container_id) + "/ca_tf/imageUpload/" + file.name
    # TODO change from localhost & correct port
    post_url = "http://0.0.0.0:8000/ca_tf/imageUpload/" + img.name
    try:
        return requests.post(post_url, files=files, data=json, timeout=15)
    except requests.Timeout:
        print('Host unavailable.')
        return Response(status=status.HTTP_404_NOT_FOUND)
