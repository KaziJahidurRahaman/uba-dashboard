from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
import mimetypes
import datetime
from django.utils import timezone
import pandas as pd



#Tasks
from .tasks import process_uploaded_file
#Models
from .models import Sample, ObjectWeight, Weather, Instrument, Object, Person, ActivityType, SampleType, Activity



# Create your views here.
def index(request):
    object_c = Object.objects.count()
    samples_c = Sample.objects.count()
    weights_c = ObjectWeight.objects.count()
    instruments_c = Instrument.objects.count()
    
    db_counts = {
        'objects': object_c,
        'samples': samples_c,
        'weights': weights_c,
        'instruments': instruments_c
    }
    
    context = {
        'parent': 'dashboard',
        'segment': 'index',
        'db_counts': db_counts
    }
    
    return render(request, 'pages/index.html', context)




# Create Elements
def createElement(request):
    context = {
        'parent': 'create',
        'segment': 'create-element',
    }
    return render(request, 'pages/forms/create-element.html', context)

@require_POST
def savePerson(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        initials = request.POST.get('initials')
        if not name or not initials:
            return JsonResponse({'error': 'Name and initials are required'}, status=400)

        try:
            if Person.objects.filter(p_initials=initials).exists():
                return JsonResponse({'error': 'Initials already exist'}, status=400)
            person = Person(p_name=name, p_initials=initials)
            person.save()
            return JsonResponse({'message': 'Person saved successfully'}, status=200)
        except ValidationError as e:
            error_messages = [str(msg) for msg in e.messages]
            print(error_messages)
            return JsonResponse({'error': 'There was an error while validating inputs. Contact site admin.'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'There was an error while saving the person. Contact site admin.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@require_POST
def saveInstrument(request):
    if request.method == 'POST':
        serial_no = request.POST.get('serial')
        name = request.POST.get('name')
        comment = request.POST.get('comment')
        if not serial_no or not name:
            return JsonResponse({'error': 'Serial number and name are required'}, status=400)
        if Instrument.objects.filter(instrument_serial_no=serial_no).exists():
            return JsonResponse({'error': 'Serial number already exists, choose a different one.'}, status=400)
        try:
            instrument = Instrument(instrument_serial_no=serial_no, instrument_name=name, instrument_comment=comment)
            instrument.save()
            return JsonResponse({'message': 'Instrument saved successfully'}, status=200)
        except ValidationError as e:
            error_messages = [str(msg) for msg in e.messages]
            print(error_messages)
            return JsonResponse({'error': 'There was an error while validating inputs. Contact site admin.'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'There was an error while saving the instrument. Contact site admin.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@require_POST
def saveObject(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        instrument_id = request.POST.get('instrument')
        collector_initials = request.POST.get('collector')
        collection_date_time = request.POST.get('collection_date_time')
        comment = request.POST.get('comment')
        
        # Parse the collection_date_time string into separate date and time components
        collection_datetime = datetime.datetime.strptime(collection_date_time, '%m/%d/%Y %I:%M %p')
        collection_date = collection_datetime.date()
        collection_time = collection_datetime.time()


        if not code or not instrument_id:
            return JsonResponse({'error': 'At least one of the mandatory values missing.'}, status=400)
        if Object.objects.filter(object_code=code).exists():
            return JsonResponse({'error': 'Object code already exists, choose a different one.'}, status=400)
        try:
            # Create and save the Object object
            obj = Object(
                object_code=code,
                object_instrument_id=instrument_id,
                object_collector_id=collector_initials,
                object_collection_date=collection_date,
                object_collection_time=collection_time,
                object_comment=comment
            )
            obj.save()
            return JsonResponse({'message': 'Object saved successfully'}, status=200)
        except ValidationError as e:
            # Handle validation errors
            error_messages = [str(msg) for msg in e.messages]
            print(error_messages)
            return JsonResponse({'error': 'There was an error while validating inputs. Contact site admin.'}, status=400)
        except Exception as e:
            # Handle other exceptions
            print(str(e))
            return JsonResponse({'error': 'There was an error while saving the instrument. Contact site admin.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@require_POST
def saveActivityType(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        unit = request.POST.get('unit')
        comment = request.POST.get('comment')

        try:
            # Create and save the Object object
            activtity_type = ActivityType(
                activity_name=name,
                activity_unit=unit,
                activity_type_comment=comment
            )
            activtity_type.save()
            return JsonResponse({'message': 'Activity type saved successfully'}, status=200)
        except ValidationError as e:
            # Handle validation errors
            error_messages = [str(msg) for msg in e.messages]
            print(error_messages)
            return JsonResponse({'error': 'There was an error while validating inputs. Contact site admin.'}, status=400)
        except Exception as e:
            # Handle other exceptions
            print(str(e))
            return JsonResponse({'error': 'There was an error while saving the activity type. Contact site admin.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@require_POST
def saveSampleType(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        description = request.POST.get('description')

        try:
            # Create and save the Object object
            sample_type = SampleType(
                sample_type_code=code,
                description=description
            )
            sample_type.save()
            return JsonResponse({'message': 'Sample type saved successfully'}, status=200)
        except ValidationError as e:
            # Handle validation errors
            error_messages = [str(msg) for msg in e.messages]
            print(error_messages)
            return JsonResponse({'error': 'There was an error while validating inputs. Contact site admin.'}, status=400)
        except Exception as e:
            # Handle other exceptions
            print(str(e))
            return JsonResponse({'error': 'There was an error while saving the sample type. Contact site admin.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

#  Create Element ends


# Create Records
def createRecord(request):
    context = {
        'parent': 'create',
        'segment': 'create-record',
    }
    return render(request, 'pages/forms/create-record.html', context)

# Create Records Ends
    



def get_lm_samples(request):
    samples = Sample.objects.select_related('sample_person', 'sample_object', 'sample_type').all()
    context = {
        'parent': 'tables',
        'segment': 'sample',
        'samples': samples
    }
    return render(request, 'pages/tables/sample.html', context)

def get_lm_weights(request):
    lmweights = ObjectWeight.objects.select_related('objectweight_objectid', 'objectweight_person').all()
    context = {
        'parent': 'tables',
        'segment': 'lysimeter-weights',
        'lmweights': lmweights
    }
    return render(request, 'pages/tables/lysimeterweight.html', context)

def get_weather(request):
    weathers = Weather.objects.all()
    context = {
        'parent': 'tables',
        'segment': 'weather',
        'weathers': weathers
    }
    return render(request, 'pages/tables/weather.html', context)

def get_activities(request):
    activities = Activity.objects.all()
    
    context = {
        'parent': 'tables',
        'segment': 'activities',
        'activities': activities
    }
    return render(request, 'pages/tables/activities.html', context)

def getPersons(request):
    persons = Person.objects.all()
    data = serializers.serialize('json', persons)
    return JsonResponse({'persons': data}, safe=False)

def get_persons_report(request):
    persons = Person.objects.all()
    
    context = {
        'parent': 'tables',
        'segment': 'persons',
        'persons': persons
    }
    return render(request, 'pages/tables/persons.html', context)


def getInstruments(request):
    instruments = Instrument.objects.all()
    data = serializers.serialize('json', instruments)
    return JsonResponse({'instruments': data}, safe=False)



def get_instruments_report(request):
    instruments = Instrument.objects.all()
    
    context = {
        'parent': 'tables',
        'segment': 'instruments',
        'instruments': instruments
    }
    return render(request, 'pages/tables/instruments.html', context)



def getSampleTypes(request):
    sampleTypes = SampleType.objects.all()
    data = serializers.serialize('json', sampleTypes)
    return JsonResponse({'sampleTypes': data}, safe=False)



def getObjects(request):
    Objects = Object.objects.all()
    data = serializers.serialize('json', Objects)
    return JsonResponse({'Objects': data}, safe=False)


def get_objects_report(request):
    objects = Object.objects.all()
    
    context = {
        'parent': 'tables',
        'segment': 'objects',
        'objects': objects
    }
    return render(request, 'pages/tables/objects.html', context)

    
def uploadSample(request):
    context = {
        'parent': 'uploads',
        'segment': 'upload-sample',
    }
    return render(request, 'pages/forms/upload_sample.html', context)


def uploadSampleProcess(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']  # 'file' should match the name attribute of your file input

        # Check the MIME type of the uploaded file
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        
        if mime_type not in ['application/vnd.ms-excel', 
                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                             'text/csv']:
            return JsonResponse({'error': 'Invalid file format. Please upload either an Excel (.xls, .xlsx) or CSV (.csv) file.'}, status=400)
        
        else:
            try: # For Excel files
                print('Reading Excel file...')
                xls_file = pd.ExcelFile(uploaded_file)
                sheet = xls_file.sheet_names[0]  # Assuming first sheet
                df = pd.read_excel(xls_file, sheet_name=sheet)
            except Exception as e:
                # For CSV files
                try:
                    df = pd.read_csv(uploaded_file)
                except Exception as e:
                    print('Error reading CSV file:', e)
                    return JsonResponse({'error': 'Error reading the file. Check file format!'}, status=500)
            
                    return JsonResponse({'error': 'Error reading the file. Check file format!'}, status=500)
            file_columns = df.columns.tolist()
            expected_columns = ['SamplingDate',	'SamplingTime',	'SampleType', 'SampledObject', 'Volume(mL)',
                                'pH', 'Conductivity(µS/cm)', 'Nitrite(mg/L)', 'Nitrate(mg/L)', 'Sulfat(mg/L)',	
                                'DOC(mg/L)', 'TOC(mg/L)', 'Bromid(mg/L)', 'Phosphate(mg/L)', 'Fluorid(mg/L)',
                                'Chlorid(mg/L)', '2NPT(mg/L)', 'MPA(mg/L)', 'SampleTaker', 'SampleComment']
            file_columns_set = set(file_columns)
            expected_columns_set = set(expected_columns)

            if not expected_columns_set.issubset(file_columns_set):
                missing_columns = expected_columns_set - file_columns_set
                return JsonResponse({'error': f'File does not contain required columns. Missing columns: {missing_columns}'}, status=400)
            invalid_rows = []
            inserted_rows = 0
            
            for index, row in df.iterrows():
                try:
                    sample_date = row['SamplingDate']  
                    sample_time = row['SamplingTime']
                    sample_volume = row['Volume(mL)']
                    sample_pH = row['pH']
                    sample_ec = row['Conductivity(µS/cm)']
                    sample_nitrite = row['Nitrite(mg/L)']
                    sample_bromid = row['Bromid(mg/L)']
                    sample_nitrate = row['Nitrate(mg/L)']
                    sample_phosphate = row['Phosphate(mg/L)']
                    sample_fluorid = row['Fluorid(mg/L)']
                    sample_chlorid = row['Chlorid(mg/L)']
                    sample_sulfat = row['Sulfat(mg/L)']
                    sample_doc = row['DOC(mg/L)']
                    sample_toc = row['TOC(mg/L)']
                    sample_2NPT = row['2NPT(mg/L)']
                    sample_MPA = row['MPA(mg/L)']
                    sample_comment = row['SampleComment']

                    sample_type = SampleType.objects.get(sample_type_code=row['SampleType'])
                    sample_object = Object.objects.get(object_code=row['SampledObject'])
                    sample_person = Person.objects.get(p_initials=row['SampleTaker'])                
                    
                    temp_sample = Sample(
                        sample_date=sample_date, sample_time=sample_time,
                        sample_type=sample_type, sample_object=sample_object,
                        sample_volume=sample_volume,
                        sample_pH=sample_pH, sample_ec=sample_ec, sample_nitrite=sample_nitrite,
                        sample_bromid=sample_bromid, sample_nitrate=sample_nitrate,
                        sample_phosphate=sample_phosphate, sample_fluorid=sample_fluorid,
                        sample_chlorid=sample_chlorid, sample_sulfat=sample_sulfat,
                        sample_doc=sample_doc, sample_toc=sample_toc,
                        sample_2NPT=sample_2NPT, sample_MPA=sample_MPA,
                        sample_person=sample_person, sample_comment=sample_comment,
                    )
                    temp_sample.save() 
                    inserted_rows += 1 
                except Exception as e:
                    invalid_rows.append({'row': index+1, 'error': str(e)})
            if inserted_rows == 0:
                return JsonResponse({'error': 'No samples uploaded. Check the data report!', 'invalid_rows': invalid_rows}, status=500)
            elif invalid_rows:
                # return the invalid rows to the front end
                return JsonResponse({'error': f'{len(invalid_rows)} row/s not uploaded!', 'invalid_rows': invalid_rows}, status=500)
            else:
                return JsonResponse({'success': 'All rows uploaded successfully!'}, status=200)
    else:
        return JsonResponse({'error': 'No file uploaded or invalid request method!'}, status=400)
        


def uploadWeight(request):
    context = {
        'parent': 'uploads',
        'segment': 'upload-weight',
        }
    return render(request, 'pages/forms/uploadWeight.html', context)
    
def uploadWeightProcess(request):
    # return JsonResponse({'error': 'Invalid file format. Please upload either an Excel (.xls, .xlsx) or CSV (.csv) file.'}, status=400)
    
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']  # 'file' should match the name attribute of your file input

        # Check the MIME type of the uploaded file
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        
        if mime_type not in ['application/vnd.ms-excel', 
                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                             'text/csv']:
            return JsonResponse({'error': 'Invalid file format. Please upload either an Excel (.xls, .xlsx) or CSV (.csv) file.'}, status=400)
        
        else:
            try: # For Excel files
                print('Reading Excel file...')
                xls_file = pd.ExcelFile(uploaded_file)
                sheet = xls_file.sheet_names[0]  # Assuming first sheet
                df = pd.read_excel(xls_file, sheet_name=sheet)
            except Exception as e:
                # For CSV files
                try:
                    df = pd.read_csv(uploaded_file)
                except Exception as e:
                    print('Error reading CSV file:', e)
                    return JsonResponse({'error': 'Error reading the file. Check file format!'}, status=500)
            file_columns = df.columns.tolist()
            expected_columns = ['WeightDate', 'WeightTime', 'Object(Lsimeter-Soil)', 'TotalWeight(kg)',	
                                'DrainageWeight(kg)', 'RecordedBy', 'Comment']
            file_columns_set = set(file_columns)
            expected_columns_set = set(expected_columns)

            if not expected_columns_set.issubset(file_columns_set):
                missing_columns = expected_columns_set - file_columns_set
                return JsonResponse({'error': f'File does not contain required columns. Missing columns: {missing_columns}'}, status=400)
            invalid_rows = []
            inserted_rows = 0
            for index, row in df.iterrows():
                try:
                    objectweight_date=row['WeightDate']  
                    objectweight_time=row['WeightTime']
                    objectweight_total=row['TotalWeight(kg)']
                    objectweight_drainage=row['DrainageWeight(kg)']
                    objectweight_comment=row['Comment'] 

                    objectweight_objectid=Object.objects.get(object_code=row['Object(Lsimeter-Soil)'])
                    objectweight_person=Person.objects.get(p_initials = row['RecordedBy'])                
                    
                    temp_weight = ObjectWeight(
                        objectweight_date = objectweight_date, objectweight_time = objectweight_time,
                        objectweight_objectid = objectweight_objectid, 
                        objectweight_total = objectweight_total,
                        objectweight_drainage = objectweight_drainage,
                        objectweight_person = objectweight_person, objectweight_comment = objectweight_comment
                    )
                    temp_weight.save()
                    inserted_rows += 1 
                except Exception as e:
                    invalid_rows.append({'row': index+1, 'error': str(e)})
            if inserted_rows == 0:
                return JsonResponse({'error': 'No weights  uploaded. Check the data report!', 'invalid_rows': invalid_rows}, status=500)
            elif invalid_rows:
                # return the invalid rows to the front end
                return JsonResponse({'error': f'{len(invalid_rows)} row/s not uploaded!', 'invalid_rows': invalid_rows}, status=500)
            else:
                return JsonResponse({'success': 'All rows uploaded successfully!'}, status=200)
    else:
        return JsonResponse({'error': 'No file uploaded or invalid request method!'}, status=400)
        
def uploadWeather(request):
    context = {
        'parent': 'uploads',
        'segment': 'upload-weather',
        }
    return render(request, 'pages/forms/uploadWeather.html', context)
def uploadWeatherProcess(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']  # 'file' should match the name attribute of your file input

        # Check the MIME type of the uploaded file
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        
        if mime_type not in ['application/vnd.ms-excel', 
                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                             'text/csv']:
            return JsonResponse({'error': 'Invalid file format. Please upload either an Excel (.xls, .xlsx) or CSV (.csv) file.'}, status=400)
        
        else:
            try: # For Excel files
                print('Reading Excel file...')
                xls_file = pd.ExcelFile(uploaded_file)
                sheet = xls_file.sheet_names[0]  # Assuming first sheet
                df = pd.read_excel(xls_file, sheet_name=sheet)
            except Exception as e:
                # For CSV files
                try:
                    df = pd.read_csv(uploaded_file)
                except Exception as e:
                    print('Error reading CSV file:', e)
                    return JsonResponse({'error': 'Error reading the file. Check file format!'}, status=500)
            file_columns = df.columns.tolist()
            expected_columns = ['DateTime', 'Niederschlagsmenge-24h(mm/d)', 'Verdunstung-nach Haude-24h(mm/d)']
            file_columns_set = set(file_columns)
            expected_columns_set = set(expected_columns)

            if not expected_columns_set.issubset(file_columns_set):
                missing_columns = expected_columns_set - file_columns_set
                return JsonResponse({'error': f'File does not contain required columns. Missing columns: {missing_columns}'}, status=400)
            invalid_rows = []
            inserted_rows = 0
            for index, row in df.iterrows():
                try:
                    weather_datetime_obj = datetime.datetime.strptime(row['DateTime'], '%d.%m.%Y %H:%M:%S')
                    # Extract date and time components
                    weather_date = weather_datetime_obj.date()
                    weather_time = weather_datetime_obj.time()
                    weather_precipitation=row['Niederschlagsmenge-24h(mm/d)']
                    weather_evaporation=row['Verdunstung-nach Haude-24h(mm/d)']
                    
                    temp_weather = Weather(
                        weather_date = weather_date, weather_time = weather_time,
                        weather_precipitation = weather_precipitation, weather_evaporation = weather_evaporation,
                        )
                    temp_weather.save()  
                    inserted_rows += 1 
                except Exception as e:
                    invalid_rows.append({'row': index+1, 'error': str(e)})
                    print(e)
            if inserted_rows == 0:
                return JsonResponse({'error':  'No weather data uploaded. Check the data report!', 'invalid_rows': invalid_rows}, status=500)
            elif invalid_rows:
                # return the invalid rows to the front end
                return JsonResponse({'error': 'Some rows were not uploaded!', 'invalid_rows': invalid_rows}, status=500)
            else:
                return JsonResponse({'success': 'All rows uploaded successfully!'}, status=200)
    else:
        return JsonResponse({'error': 'No file uploaded or invalid request method!'}, status=400)

def uploadActivity(request):
    context = {
        'parent': 'uploads',
        'segment': 'upload-activity',
        }
    return render(request, 'pages/forms/uploadActivity.html', context)
def uploadActivityProcess(request):

    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']  # 'file' should match the name attribute of your file input

        # Check the MIME type of the uploaded file
        mime_type, _ = mimetypes.guess_type(uploaded_file.name)
        
        if mime_type not in ['application/vnd.ms-excel', 
                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                             'text/csv']:
            return JsonResponse({'error': 'Invalid file format. Please upload either an Excel (.xls, .xlsx) or CSV (.csv) file.'}, status=400)
        
        else:
            try: # For Excel files
                print('Reading Excel file...')
                xls_file = pd.ExcelFile(uploaded_file)
                sheet = xls_file.sheet_names[0]  # Assuming first sheet
                df = pd.read_excel(xls_file, sheet_name=sheet)
            except Exception as e:
                # For CSV files
                try:
                    df = pd.read_csv(uploaded_file)
                except Exception as e:
                    print('Error reading CSV file:', e)
                    return JsonResponse({'error': 'Error reading the file. Check file format!'}, status=500)
            file_columns = df.columns.tolist()
            expected_columns = ['ActivityDate', 'ActivityTime','Object(Lsimeter-Soil)', 'ActivityType', 'ActivityComment', 'ConductedBy']
            file_columns_set = set(file_columns)
            expected_columns_set = set(expected_columns)

            if not expected_columns_set.issubset(file_columns_set):
                missing_columns = expected_columns_set - file_columns_set
                return JsonResponse({'error': f'File does not contain required columns. Missing columns: {missing_columns}'}, status=400)
            invalid_rows = []
            inserted_rows = 0
            for index, row in df.iterrows():
                try:
                    activity_date = row['ActivityDate']
                    activity_time = row['ActivityTime']
                    activity_object = Object.objects.get(object_code=row['Object(Lsimeter-Soil)'])
                    
                    activity_type=ActivityType.objects.get(activity_name=row['ActivityType'])
                    activity_person=Person.objects.get(p_initials = row['ConductedBy']) 
                    activity_comment = row['ActivityComment']
                    temp_activity = Activity(
                        activity_date = activity_date, activity_time = activity_time, activity_object = activity_object, 
                        activity_type = activity_type, activity_person = activity_person, activity_comment = activity_comment
                        )
                    temp_activity.save()  
                    inserted_rows += 1 
                except Exception as e:
                    invalid_rows.append({'row': index+1, 'error': str(e)})
                    print(e)
            if inserted_rows == 0:
                return JsonResponse({'error': 'No acitvity uploaded. Check the data report!', 'invalid_rows': invalid_rows}, status=500)
            elif invalid_rows:
                # return the invalid rows to the front end
                return JsonResponse({'error': f'{len(invalid_rows)} row/s not uploaded!', 'invalid_rows': invalid_rows}, status=500)
            else:
                return JsonResponse({'success': 'All rows uploaded successfully!'}, status=200)
    else:
        return JsonResponse({'error': 'No file uploaded or invalid request method!'}, status=400)