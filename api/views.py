import string
import random
import os
import datetime
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.constants import OUTPUT_DIR


class RandomNumberView(views.APIView):
    """
    this view is creating a new object and storing it into a file
    """

    def get(self, request):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        files = os.listdir(OUTPUT_DIR)
        return Response({
            'success': True,
            'message': "Objects fetched successfully",
            'result': [request.build_absolute_uri(reverse('api:fetch', kwargs={'name': file})) for file in files]
        }, status=status.HTTP_200_OK)

    def post(self, request):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = "object - {}".format(datetime.datetime.now())
        file_path = os.path.join(OUTPUT_DIR, filename)

        alphabetic = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        real_number = random.uniform(-100000000, 100000000)
        integers = random.randrange(0, 100000000)
        alphanumerics = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

        with open(file_path, 'w') as f:
            f.write("{}, {}, {}, {}".format(alphabetic, integers, alphanumerics, real_number))
        return Response({
            'success': True,
            'message': "objects created successfully",
            'result': {"name": filename}
        }, status=status.HTTP_200_OK)


@api_view(("GET",))
def object_detail(request, name):

    """
    This view is return an object's details against filename
    """
    file_path = os.path.join(OUTPUT_DIR, name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as fh:
            line = fh.read()
            alphabetic, integers, alphanumerics, real_number = line.split(', ')
    return Response({
        'success': True,
        'message': "objects created successfully",
        'result': {
            "alphabetic": len(alphabetic),
            "integers": len(integers),
            'alphanumerics': len(alphanumerics),
            'real_number': len(real_number)
        }
    }, status=status.HTTP_200_OK)


@api_view(('GET',))
def download(request, name):
    """
    this View is download the file
    """
    file_path = os.path.join(OUTPUT_DIR, name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.txt")
            response['Content-Disposition'] = 'inline; filename=' + name + ".txt"
            return response
    raise Http404


# These are the helper views for template rendering

def home(request):
    return render(request, 'api/home.html', context={})


def detail(request, name):
    context = {
        "link": request.build_absolute_uri(reverse('api:download', kwargs={'name': name})),
        "name": name
    }
    return render(request, 'api/detail.html', context=context)




