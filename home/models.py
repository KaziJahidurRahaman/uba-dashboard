from django.db import models

class Person(models.Model):
    p_id = models.AutoField(primary_key=True, null=False, db_column='PID', verbose_name='unique db id of the person')
    p_initials = models.CharField(unique=True, db_column='PInitials', max_length=15, verbose_name='unique initials of the person')
    p_name = models.CharField(db_column='P_Name', max_length=255, null=True)
    p_eid = models.IntegerField(db_column='P_EID', default=0)

    class Meta:
        db_table = 'tbl_persons'
        verbose_name_plural = 'Persons'


class Instrument(models.Model):
    instrument_id = models.AutoField(primary_key=True)
    instrument_serial_no = models.CharField(max_length=50, null=True)
    instrument_name = models.CharField(max_length=50, null=True)
    instrument_comment = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'tbl_instruments'
        verbose_name_plural = 'Instruments'

class Object(models.Model):
    object_id = models.AutoField(primary_key=True, db_column='ObjectID',verbose_name='unique db id of the sample')
    object_code = models.CharField(max_length=12, unique=True, null=False, db_column = 'ObjectCode', default=None, verbose_name='name/code of the object')
    object_instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column = 'ObjectInstrument', null=True, default=None, verbose_name='db id of the instrument used for sampling')
    object_collector = models.ForeignKey(Person,  to_field='p_id', on_delete=models.CASCADE, null=True, default=None, db_column = 'ObjectCollector', verbose_name='initials of the person who collected the sample')
    object_collection_date = models.DateField(null=True,db_column = 'ObjectColDate', default=None, verbose_name='the day sample was collected')
    object_collection_time = models.TimeField(null=True, default=None,db_column = 'ObjectColTime', verbose_name='time of the day sample was collected')
    object_comment = models.CharField(max_length=100, null=True, default=None,db_column = 'ObjectComment', verbose_name='additional info')

    class Meta:
        db_table = 'tbl_objects'
        verbose_name_plural = 'Objects'

class SampleType(models.Model):
    sample_type_id =  models.AutoField(primary_key=True)
    sample_type_code = models.CharField(max_length=7)
    # sample_type_units = models.JSONField()
    description = models.TextField(null=True)

    class Meta:
        db_table = 'tbl_sample_types'
        verbose_name_plural = 'SampleTypes'

class Sample(models.Model):
    sample_id = models.BigAutoField(primary_key=True, db_column='SampleID')
    sample_date = models.DateField(null=True, default=None, db_column='SampleDate')
    sample_time = models.TimeField(null=True, default=None, db_column='SampleTime')
    sample_type = models.ForeignKey(SampleType, on_delete=models.DO_NOTHING, db_column='SampleType')
    sample_object = models.ForeignKey(Object, on_delete=models.DO_NOTHING, db_column='SampleObject')
    sample_volume = models.FloatField(null=True, default=None, db_column='Volume_mL')
    sample_pH = models.FloatField(null=True, default=None, db_column='pH')
    sample_ec = models.FloatField(null=True, default=None, db_column='EConductivity')
    sample_nitrite = models.FloatField(null=True, default=None, db_column='Nitrite')
    sample_bromid = models.FloatField(null=True, default=None, db_column='Bromid')
    sample_nitrate = models.FloatField(null=True, default=None, db_column='Nitrate')
    sample_phosphate = models.FloatField(null=True, default=None, db_column='Phosphate')
    sample_fluorid = models.FloatField(null=True, default=None, db_column='Flourid')
    sample_chlorid = models.FloatField(null=True, default=None, db_column='Clorid')
    sample_sulfat = models.FloatField(null=True, default=None, db_column='Sulfat')
    sample_doc = models.FloatField(null=True, default=None, db_column='DOC')
    sample_toc = models.FloatField(null=True, default=None, db_column='TOC')
    sample_2NPT = models.FloatField(null=True, default=None, db_column='2NPT')
    sample_MPA = models.FloatField(null=True, default=None, db_column = 'MPA')
    sample_person = models.ForeignKey(Person, to_field='p_initials', on_delete=models.DO_NOTHING, db_column='SamplingPerson')
    sample_comment = models.TextField(null=True, default=None, db_column='Comment')
    sample_created_at = models.DateTimeField(null=True, auto_now_add = True,  db_column='created_at')
    
    class Meta:
        db_table = 'tbl_samples'
        verbose_name_plural = 'Samples'



class ObjectWeight(models.Model):
    objectweight_id = models.BigAutoField(primary_key=True)
    objectweight_date = models.DateField(null=True, default=None)
    objectweight_time = models.TimeField(null=True, default=None)
    objectweight_objectid = models.ForeignKey(Object, on_delete=models.DO_NOTHING, db_column='objectweight_objectid')
    objectweight_total = models.FloatField(null=True, default=None)
    objectweight_drainage = models.FloatField(null=True, default=None)
    objectweight_person = models.ForeignKey(Person,to_field='p_initials', on_delete=models.DO_NOTHING, db_column='objectweight_person_id')
    objectweight_comment = models.TextField(null=True, default=None)
    objectweight_db_timestamp = models.DateTimeField(null=True, default=None)
    
    class Meta:
        db_table = 'tbl_objectWeights'
        verbose_name_plural = 'ObjectWeights'

class Weather(models.Model):
    weather_id = models.BigAutoField(primary_key=True)
    weather_date = models.DateField(null=True, default=None)
    weather_time = models.TimeField(null=True, default=None)
    weather_precipitation = models.FloatField(null = True, default = None)
    weather_evaporation = models.FloatField(null = True, default = None)
    objectweight_db_timestamp = models.DateTimeField(null=True, default=None)
    
    class Meta:
        db_table = 'tbl_weathers'
        verbose_name_plural = 'Weathers'

class Activity(models.Model):
    activity_id = models.BigAutoField(primary_key=True)
    activity_date = models.DateField(null=True, default=None)
    activity_time = models.TimeField(null=True, default=None)
    activity_object  = models.ForeignKey(Object, on_delete=models.DO_NOTHING, db_column='activity_objectid')
    activity_type = models.CharField(null = True, default = None, max_length = 1,  verbose_name='C = Crop, Watering = W, Others = O')
    activity_comment = models.TextField(null=True, default=None)
    activity_person = models.ForeignKey(Person, to_field='p_initials', on_delete=models.DO_NOTHING, db_column='activity_person_id')
    activity_db_timestamp = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'tbl_activities'
        verbose_name_plural = 'Activities'
