# your_app/tasks.py
from celery import shared_task
from django.core.files.storage import default_storage

@shared_task
def process_uploaded_file(file_url):
    print('Task Triggered')
    # Retrieve the file from the storage
    # file_content = default_storage.open(file_url).read()

    # # Process the file content (replace this with your actual processing logic)
    # lines = file_content.splitlines()
    # # Perform further processing on 'lines' or do whatever is needed

    # # For demonstration purposes, print the first 5 lines
    # print("First 5 lines of the file:")
    # for line in lines[:5]:
    #     print(line.decode('utf-8'))
