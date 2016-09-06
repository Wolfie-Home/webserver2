# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Device(models.Model):
    uid = models.AutoField(db_column='Id', primary_key=True)  
    name = models.CharField(db_column='Name', max_length=20)  
    description = models.CharField(db_column='Description', max_length=50)  
    createdTime = models.DateTimeField(db_column='CreatedTime')  
    modifiedTime = models.DateTimeField(db_column='ModifiedTime')  

    owner = models.ForeignKey('User', models.DO_NOTHING, db_column='OwnerRef')  
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='LocationRef', blank=True, null=True)  
    parent = models.ForeignKey('self', models.DO_NOTHING, db_column='Parent', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'Device'
        unique_together = (('owner', 'name'),)

class Datafield(models.Model):
    uid = models.AutoField(db_column='Id', primary_key=True)  
    dataFieldName = models.CharField(db_column='DatafieldName', max_length=16)  
    controllable = models.IntegerField(db_column='Controllable')  
    description = models.CharField(db_column='Description', max_length=50)  
    createdTime = models.DateTimeField(db_column='CreatedTime')  
    modifiedTime = models.DateTimeField(db_column='ModifiedTime')

    device = models.ForeignKey('Device', models.DO_NOTHING, db_column='DeviceRef')  
    dataType = models.ForeignKey('DataType', models.DO_NOTHING, db_column='DataTypeRef')  

    class Meta:
        managed = False
        db_table = 'DataField'
        unique_together = (('device', 'dataFieldName'),)


class Datarecord(models.Model):
    uid = models.BigAutoField(db_column='Idx', primary_key=True)  
    createdtime = models.DateTimeField(db_column='CreatedTime')
    
    device = models.ForeignKey('Device', models.DO_NOTHING, db_column='DeviceRef')  
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='LocationRef', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'DataRecord'


class Datatype(models.Model):
    uid = models.AutoField(db_column='Id', primary_key=True)  
    typeName = models.CharField(db_column='TypeName', unique=True, max_length=20)  
    description = models.CharField(db_column='Description', max_length=128)  
    createdTime = models.DateTimeField(db_column='CreatedTime')  
    modifiedTime = models.DateTimeField(db_column='ModifiedTime')  

    class Meta:
        managed = False
        db_table = 'DataType'


class Location(models.Model):
    uid = models.AutoField(db_column='Id', primary_key=True)  
    name = models.CharField(db_column='Name', max_length=20)  
    description = models.CharField(db_column='Description', max_length=50)  
    createdTime = models.DateTimeField(db_column='CreatedTime')  
    modifiedTime = models.DateTimeField(db_column='ModifiedTime')  

    user = models.ForeignKey('User', models.DO_NOTHING, db_column='UserRef')
    parent = models.ForeignKey('self', models.DO_NOTHING, db_column='Parent', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'Location'
        unique_together = (('user', 'name'),)


class RecordFieldValue(models.Model):
    idx = models.BigAutoField(db_column='Idx', primary_key=True)
    value = models.CharField(db_column='Value', max_length=30)

    record = models.ForeignKey('DataRecord', models.DO_NOTHING, db_column='RecordRef')
    dataField = models.ForeignKey(Datafield, models.DO_NOTHING, db_column='DataFieldRef')
    
    class Meta:
        managed = False
        db_table = 'RecordFieldValue'


class User(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  
    username = models.CharField(db_column='UserName', unique=True, max_length=30)  
    password = models.CharField(db_column='Password', max_length=128)  
    email = models.CharField(db_column='Email', max_length=40)  
    passSalt = models.CharField(db_column='PassSalt', max_length=8)  
    createdTime = models.DateTimeField(db_column='CreatedTime')  
    modifiedTime = models.DateTimeField(db_column='ModifiedTime')  

    class Meta:
        managed = False
        db_table = 'User'
