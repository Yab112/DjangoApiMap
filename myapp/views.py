from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import os
from dotenv import load_dotenv
from requests import Response  # Import the Response object

# Load environment variables
load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
@csrf_exempt  # Temporarily disable CSRF for testing (we'll fix this later)
def get_route(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            coordinates = data.get("coordinates")  # Expecting [[lng, lat], [lng, lat], ...]

            if not coordinates or len(coordinates) < 2:
                return JsonResponse({"error": "Invalid coordinates"}, status=400)

            # OpenRouteService API call
            url = "https://api.openrouteservice.org/v2/directions/driving-car"
            headers = {"Authorization": ORS_API_KEY,  'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Content-Type': 'application/json; charset=utf-8'}
            params = {"coordinates": coordinates, "format": "json"}

            response: Response = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/json', json=params, headers=headers)

            

            return JsonResponse(response.json())

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)