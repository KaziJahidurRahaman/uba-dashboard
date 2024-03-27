from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('table/reports/lysimeter-samples', views.get_lm_samples, name='report_lysimeter_samples'),
    path('table/reports/lysimeter-weights', views.get_lm_weights, name='report_lysimeter_weights'),
    path('table/reports/weather', views.get_weather, name='report_weather'),
    
    path('upload/upload-sample', views.uploadSample, name='upload-sample'),
    path('upload/upload-sample-process', views.uploadSampleProcess, name='upload-sample-process'),

    path('create/create-record', views.createRecord, name='create-record'),
    path('create/save-person', views.savePerson, name='save-person'),
    path('create/save-instrument', views.saveInstrument, name='save-instrument'),
    path('create/save-object', views.saveObject, name='save-object'),
    

    path('table/reports/persons', views.getPersons, name='get-persons'),
    path('table/reports/instruments', views.getInstruments, name='get-instruments'),
    

]
