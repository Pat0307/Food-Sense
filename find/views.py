from django.shortcuts import render, redirect
import requests
import json
from .markdownRender import *
from gemini.functions import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from users.models import Profile, Favorite
# Create your views here.

def index(request):
    return render(request, 'find/index.html')

@login_required()
def find(request):
    if request.method == "POST":
        try:
            profile = Profile.objects.get(user=request.user)

            latitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")
            url = "https://places.googleapis.com/v1/places:searchNearby"
            myHeader = {
                'Content-Type': 'application/json',
                'x-Goog-Api-Key': 'AIzaSyBxe3eAkFoka4n2RkpXJysB9NmRJld0iQ8',
                'X-Goog-FieldMask': 'places.displayName,places.id,places.types,places.formattedAddress'
            }
            myBody = {
                'includedTypes': ['restaurant'],
                'maxResultCount': 10,
                'locationRestriction': {
                    'circle': {
                        'center': {
                            'latitude': latitude,
                            'longitude': longitude,
                        },
                        'radius': 10000.0
                    }
                },
                'rankPreference': 'DISTANCE'
            }
            result = requests.post(url, json=myBody, headers=myHeader).json()
            # print(type(result)) // DICTIONARY
            # print(result)
            places = []
            for restaurant in result['places']:
                new_data = {
                    'displayName': restaurant['displayName']['text'],
                    'address': restaurant['formattedAddress'],
                    'types': restaurant['types'],
                }
                places.append(new_data)

                # print(f"Name: {restaurant['displayName']['text']}")
                # print(f"Address: {restaurant['formattedAddress']}")
                # print(f"Types: {restaurant['types']}")
                # print("-" * 20)

            context = {
                "latitude": latitude,
                "longitude": longitude,
                "places": places,
            }
            return render(request, "find/find.html", context)
        except Profile.DoesNotExist:
            return redirect('users:createProfile')
        # nearby_restaurants = gmaps.places_nearby(
        #     location=(latitude, longitude),
        #     radius = 5000,
        #     type = 'restaurant',
        #     rankby = 'distance',
        # )
        # print(nearby_restaurants)
        # nearby_restaurants = gmaps.places.textsearch(
        #     query='restaurants',  # Search for restaurants (can be more specific)
        #     location=(latitude, longitude),  # Your location
        #     radius=5000,  # Search within a 5 km radius
        #     rankby='distance',  # Sort by distance
        # )
        # for restaurant in nearby_restaurants['results']:
        #     print(f"Name: {restaurant['name']}")
        #     print(f"Address: {restaurant['vicinity']}")
        #     print(f"Types: {restaurant['types']}")
        #     print("-" * 20)
    else:
        return redirect('index')


def generate_rec(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        data = json.loads(request.body.decode('utf-8'))
        response = generate_recommendation(data)
        return JsonResponse({'response': md_to_html(response)}, safe=False)
    else:
        return JsonResponse({'message': 'Invalid request Method'}, status=400)


def recipe(request):
    return render(request, "find/recipe.html")


def generateRecipe(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        data = json.loads(request.body)
        item = data['item']
        response = json.loads(generate_recipe(item))
        return JsonResponse({"response": response}, safe=False)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)

@login_required()
def findIngredient(request):
    return render(request, "find/ingredients.html")

@login_required()
def ingredientRecipe(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        data = json.loads(request.body)
        ingredients = data['ingredients']
        response = json.loads(generate_ingredient_recipe(ingredients))
        return JsonResponse({"response": response}, safe=False)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=400)

@login_required
def save_favorite(request):
   if request.method == 'POST':
       try:
           data = json.loads(request.body.decode('utf-8'))
           print(data)
           entry = Favorite()
           entry.user = request.user
           entry.name = data.get('item')
           entry.ingredients = data.get('ingredients')
           entry.steps = data.get('steps')
           entry.save()
           return JsonResponse({'message': 'Recipe saved to favorites!'})


       except Profile.DoesNotExist:
           return JsonResponse({'message': 'Profile not found.'}, status=404)


   return JsonResponse({'message': 'Invalid request method.'}, status=405)

