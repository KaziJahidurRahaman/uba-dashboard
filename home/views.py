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



#Tasks
from .tasks import process_uploaded_file
#Models
from .models import Sample, ObjectWeight, Weather, Instrument, Object, Person



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

def createRecord(request):
    context = {
        'parent': 'create',
        'segment': 'create-record',
    }
    return render(request, 'pages/forms/create-record.html', context)

def get_lm_samples(request):
    samples = Sample.objects.select_related('sample_person', 'sample_object', 'sample_type').all()
    print(samples.first().__dict__)
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

def getPersons(request):
    persons = Person.objects.all()
    data = serializers.serialize('json', persons)
    return JsonResponse({'persons': data}, safe=False)

def getInstruments(request):
    instruments = Instrument.objects.all()
    data = serializers.serialize('json', instruments)
    return JsonResponse({'instruments': data}, safe=False)

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
    
def uploadSample(request):
    context = {
        'parent': 'uploads',
        'segment': 'upload-sample',
    }
    return render(request, 'pages/forms/upload_sample.html', context)


@csrf_exempt  # Use the decorator if CSRF protection is causing issues
def uploadSampleProcess(request):
    import pandas as pd

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
            file_columns = df.columns
            db_columns = [f.name for f in Sample._meta.get_fields()]
            db_columns.remove('sample_id')
            db_columns.remove('sample_created_at')
            
            if len(file_columns) != len(db_columns):
                return JsonResponse({'error': f'Number of columns do not match with the database. {len(file_columns)} columns in file, {len(db_columns)} expected'}, status=400)
            for inedx, row in df.iterrows():
                print(row)
            return JsonResponse({'message': 'Error reading the file. Check file format!'}, status=200)
        


        # file_columns = df.columns
        #     db_columns = [f.name for f in Sample._meta.get_fields()].remove('')
        #     # print(file_columns)
        #     print(db_columns)
        #     if len(df.columns) != len(Sample._meta.get_fields()):
        #         return JsonResponse({'error': 'Number of columns in the file does not match the number of columns in the database.'}, status=400)
            
        #     # print(db_columns)
        #     # if not all(col in db_columns for col in file_columns):
        #     #     return JsonResponse({'error': 'Column names in the file do not match the column names in the database.'}, status=400) 
        #     # file_columns = df.columns
        #     # db_columns = [f.name for f in Sample._meta.get_fields()]

        #     # print(file_columns)
        
        # ## check if the column names are same as my db column names