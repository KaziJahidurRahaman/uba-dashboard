from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('table/reports/lysimeter-samples', views.get_lm_samples, name='report_lysimeter_samples'),
    path('table/reports/lysimeter-weights', views.get_lm_weights, name='report_lysimeter_weights'),
    path('table/reports/weather', views.get_weather, name='report_weather'),
    path('table/reports/activities', views.get_activities, name='report_activities'),
    path('table/reports/objects', views.get_objects_report, name='report_objects'),
    path('table/reports/instruments', views.get_instruments_report, name='report_instruments'),
    path('table/reports/persons', views.get_persons_report, name='report_persons'),
    
    path('upload/upload-sample', views.uploadSample, name='upload-sample'),
    path('upload/upload-sample-process', views.uploadSampleProcess, name='upload-sample-process'),
    
    
    path('upload/upload-weight', views.uploadWeight, name='upload-weight'),
    path('upload/upload-weight-process', views.uploadWeightProcess, name='upload-weight-process'),
    
    path('upload/upload-weather', views.uploadWeather, name='upload-weather'),
    path('upload/upload-weather-process', views.uploadWeatherProcess, name='upload-weather-process'),
    
    path('upload/upload-activity', views.uploadActivity, name='upload-activity'),
    path('upload/upload-activity-process', views.uploadActivityProcess, name='upload-activity-process'),
    
    path('create/create-element', views.createElement, name='create-element'),
    path('create/save-person', views.savePerson, name='save-person'),
    path('create/save-instrument', views.saveInstrument, name='save-instrument'),
    path('create/save-object', views.saveObject, name='save-object'),
    path('create/save-activitytype', views.saveActivityType, name='save-activitytype'),
    path('create/save-sampletype', views.saveSampleType, name='save-sampletype'),
    
    path('create/create-record', views.createRecord, name='create-record'),

    

    path('table/get/persons', views.getPersons, name='get-persons'),
    path('table/get/sampleTypes', views.getSampleTypes, name='get-sample-types'),
    path('table/get/instruments', views.getInstruments, name='get-instruments'),
    path('table/get/objects', views.getObjects, name='get-objects'),
    

]
