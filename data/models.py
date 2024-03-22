from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class EconomicInfo(TimeStampedModel):
    cost = models.PositiveIntegerField(default=10)
    updated_cost = models.IntegerField(default=0)

    def __str__(self):
        return self.cost

class Address(TimeStampedModel):
    address = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255, default='')
    address_place_id = models.CharField(max_length=255)  # Remove db_index=True
    unit_code = models.CharField(max_length=10, default='')
    floor = models.IntegerField(default=0)

    def __str__(self):
        return self.address

class GeneralInfo(TimeStampedModel):
    address = models.OneToOneField(Address, on_delete=models.CASCADE,related_name='general_info',null=True)
    unit = models.CharField(max_length=255)  
    floor = models.IntegerField(default=0)
    bedrooms = models.CharField(max_length=255) 
    bathrooms = models.CharField(max_length=255) 
    agent_id = models.CharField(max_length=36, default='') 
    apartment_number = models.IntegerField(default=0)  
    property_name = models.CharField(max_length=255, default='')  
    date_available = models.DateField(default='2024-04-15')  
    description = models.TextField(default='') 
    is_easy_apply = models.BooleanField(default=False) 
    def __str__(self):
        return self.property_name
    
class AmenityInfo(TimeStampedModel):
    type = models.CharField(max_length=100)
    included = models.BooleanField(default=False)

    def __str__(self):
        return self.type    

class ExtraFee(TimeStampedModel):
    name = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    FEE_TYPES = (
        ('ONE_TIME', 'One Time'),
        ('RECURRING', 'Recurring'),
    )
    fee_type = models.CharField(max_length=20, choices=FEE_TYPES)

    def __str__(self):
        return self.name
    
class ChargeInfo(TimeStampedModel):
    first_month_rent = models.IntegerField(default=0)
    security_deposit = models.IntegerField(default=0)
    broker_fee = models.IntegerField(default=0)
    application_fee = models.IntegerField(default=0)
    extra_fee_name = models.CharField(max_length=255, null=True, blank=True)
    extra_fee_cost = models.IntegerField(default=0)
    extra_fee = models.ManyToManyField(ExtraFee, related_name='charges', blank=True)

    def __str__(self):
        return f"Charge Information for Property: {self.property}"
    
class UtilityInformation(TimeStampedModel):
    gas = models.BooleanField(default=False)
    sewage = models.BooleanField(default=False)
    electricity = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    garbage = models.BooleanField(default=False)
    cable = models.BooleanField(default=False)
    satellite_tv = models.BooleanField(default=False)
    other_utilities = models.CharField(max_length=255, blank=True, null=True)


class Documents(TimeStampedModel):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

class DocumentInfo(TimeStampedModel):
    documents = models.ManyToManyField(Documents, related_name='documents', blank=True)

class CustomUser(TimeStampedModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True)
    user_type = models.CharField(max_length=20, blank=True, choices=[('AGENT', 'Agent'), ('RENTER', 'Renter')])
    # USERNAME_FIELD = 'email'
    def __str__(self):
        return self.email
    
class Property(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True) 
    general_info = models.OneToOneField(GeneralInfo, on_delete=models.CASCADE,related_name='property')
    economic_info = models.OneToOneField(EconomicInfo, on_delete=models.CASCADE, related_name='property', null=True, blank=True)
    amenities = models.ManyToManyField(AmenityInfo, related_name='properties', blank=True)
    charge_info = models.OneToOneField(ChargeInfo, on_delete=models.CASCADE,related_name='property',null=True)
    utility_info = models.OneToOneField(UtilityInformation, on_delete=models.CASCADE,related_name='property',null=True)
    document_info = models.OneToOneField(DocumentInfo, on_delete=models.CASCADE,related_name='property',null=True)

    def __str__(self):
        return self.name
    