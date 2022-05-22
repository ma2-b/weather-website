from ast import Delete
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
import requests
from .models import city
from .forms import CityForm
from django.views.generic import DeleteView

# Create your views here.

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=dfb118c161e5402ff2370dff36caa539'
    cities = city.objects.all().order_by('-id')
    weather_data = []
    form = CityForm()
    
    error_msg = ''
    message = ''
        
    if request.method == "POST":
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city = city.objects.filter(name=new_city).count()
            
            if existing_city == 0:
                r = requests.get(url.format(new_city)).json() 
                if r['cod'] == 200:
                    form.save()
                else:
                    error_msg = 'City does not exist'
            else:
                error_msg = 'City already exists in the database'
    
    if error_msg:
        message = error_msg 
    
    for citye in cities:
        r = requests.get(url.format(citye)).json()
        city_weather = {
        'city' : citye.name,
        'temperature' : r['main']['temp'],
        'description' : r['weather'][0]['description'],
        'icon' : r['weather'][0]['icon'], 
        'wind_speed' : r['wind']['speed'],
        }
    
        weather_data.append(city_weather)
        
    context = {'weather_data':weather_data, 
               'form':form,
               'message':message,}
    return render(request,'index.html',context)

def delete_city(request, city_name):
    city.objects.get(name=city_name).delete()
    
    return redirect('weather:index')