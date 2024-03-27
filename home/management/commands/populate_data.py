# home/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Instrument, Object, Person, SampleType, Sample
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.populate_instruments()
        self.populate_persons()
        self.populate_objects()
        self.populate_sample_types()
        self.populate_samples()

    def populate_instruments(self):
        for _ in range(5):
            Instrument.objects.create(
                instrument_serial_no=fake.uuid4(),
                instrument_name=fake.word(),
                instrument_comment=fake.sentence(),
                
            )

    def populate_persons(self):
        for _ in range(5):
            Person.objects.create(
                p_name=fake.name(),
                p_eid=fake.random_number(6),
            )

    def populate_objects(self):
        for _ in range(10):
            Object.objects.create(
                object_instrument=random.choice(Instrument.objects.all()),
                object_source_latlong=random.choice(['Value A', 'Value B']),
                object_current_latlong=random.choice(['Value A', 'Value B']),
                object_collection_date=fake.date(),
                object_collection_time=fake.time(),
                object_collector=random.choice(Person.objects.all()),
                object_comment=fake.sentence(),
            )

    def populate_sample_types(self):
        for _ in range(3):
            SampleType.objects.create(
                parameter_name=fake.word(),
                param_unit=fake.word(),
                description=fake.sentence(),
            )

    def populate_samples(self):
        for _ in range(20):
            Sample.objects.create(
                sample_date=fake.date(),
                sample_time=fake.time(),
                sample_type=random.choice(SampleType.objects.all()),
                sample_object=random.choice(Object.objects.all()),
                sample_value=fake.random_number(2),
                sample_person=random.choice(Person.objects.all()),
                sample_db_timestamp=datetime.now() - timedelta(days=random.randint(1, 30)),
            )
