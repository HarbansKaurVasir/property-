from rest_framework import serializers
from .models import Property, GeneralInfo, Address, EconomicInfo, AmenityInfo, ChargeInfo, ExtraFee, UtilityInformation,DocumentInfo,Documents,CustomUser
from rest_framework.exceptions import ValidationError
from .decorators import check_credentials


class UserAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password','first_name', 'last_name', 'phone', 'user_type']
    
    def validate_user_type(self, user_type):
        if user_type not in ['AGENT', 'RENTER']:
            raise ValidationError('Invalid user type')
        return user_type
class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ['name','category']

class DocumentInfoSerializer(serializers.ModelSerializer):
    documents = DocumentsSerializer(many=True)
    class Meta:
        model = DocumentInfo
        fields = ['documents']

class UtilityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityInformation
        fields = [ 'gas', 'sewage', 'electricity', 'internet', 'water', 'garbage', 'cable', 'satellite_tv', 'other_utilities']

class ExtraFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraFee
        fields = [ 'name', 'amount', 'fee_type']

class ChargeInfoSerializer(serializers.ModelSerializer):
    extra_fee = ExtraFeeSerializer(many=True)
    class Meta:
        model = ChargeInfo
        fields = ['first_month_rent', 'security_deposit', 'broker_fee', 'application_fee',
                  'extra_fee_name', 'extra_fee_cost', 'extra_fee']
          
class AmenityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityInfo
        fields = ['type','included']

class EconomicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicInfo
        fields = ['cost', 'updated_cost']
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [ 'address', 'place_id', 'address_place_id', 'unit_code', 'floor']

    def validate_address(self, value):
        if self.context['request'].method == 'POST':
            if Address.objects.filter(address=value).exists():
                raise serializers.ValidationError("Address must be unique.")
        return value
    
class GeneralInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = GeneralInfo
        fields = [ 'address', 'unit', 'floor', 'bedrooms', 'bathrooms', 'agent_id',
                  'apartment_number', 'property_name', 'date_available', 'description', 'is_easy_apply']

class PropertySerializer(serializers.ModelSerializer):
    general_info = GeneralInfoSerializer()
    economic_info = EconomicInfoSerializer()
    amenities = AmenityInfoSerializer(many=True)
    charge_info = ChargeInfoSerializer()
    utility_info = UtilityInfoSerializer()
    document_info = DocumentInfoSerializer()
   
    class Meta:
        model = Property
        fields = ['id','name', 'general_info', 'economic_info','amenities','charge_info','utility_info','document_info']
      
    def create(self, validated_data):
        general_info_data = validated_data.pop('general_info')
        address_data = general_info_data.pop('address')
        
        economic_info_data = validated_data.pop('economic_info')
    
        amenities_data = validated_data.pop('amenities',[])
        
        charge_info_data = validated_data.pop('charge_info')
        extra_fee_data = charge_info_data.pop('extra_fee',[])
    
        utility_info_data = validated_data.pop('utility_info',{})
        
        document_info_data = validated_data.pop('document_info')
        documents = document_info_data.pop('documents',[])

        # making new object for models
        address_instance = Address.objects.create(**address_data)
        general_info_instance = GeneralInfo.objects.create(address=address_instance, **general_info_data)

        economic_info_instance = EconomicInfo.objects.create(**economic_info_data)
        
        charge_info_instance = ChargeInfo.objects.create(**charge_info_data)
        for fee_data in extra_fee_data:
            extra_fee_instance = ExtraFee.objects.create(**fee_data)
            charge_info_instance.extra_fee.add(extra_fee_instance)

        utility_info_instance = UtilityInformation.objects.create(**utility_info_data)

        document_info_instance = DocumentInfo.objects.create(**document_info_data)
        for documents_data in documents:
            documents_instance =Documents.objects.create(**documents_data)
            document_info_instance.documents.add(documents_instance)

        property_instance = Property.objects.create(
            general_info = general_info_instance,
            economic_info = economic_info_instance,
            charge_info = charge_info_instance,
            utility_info = utility_info_instance,
            document_info = document_info_instance,
            **validated_data)

        for amenity_data in amenities_data:
            amenity_instance, _ = AmenityInfo.objects.get_or_create(**amenity_data)
            property_instance.amenities.add(amenity_instance)

        return property_instance
          
    def validate_name(self , value):
        if not value.replace(' ', '').isalpha():
            raise ValidationError("Name must contain only alphabets and spaces")
        return value

    def update(self, instance, validated_data):
        
        general_info_data = validated_data.pop('general_info', {})
        if general_info_data:
            address_data = general_info_data.pop('address', {})
            address_instance, _ = Address.objects.get_or_create(**address_data)
            instance.general_info.address = address_instance
            instance.general_info.unit = general_info_data.get('unit', instance.general_info.unit)
            instance.general_info.floor = general_info_data.get('floor', instance.general_info.floor)
            instance.general_info.bedrooms = general_info_data.get('bedrooms', instance.general_info.bedrooms)
            instance.general_info.bathrooms = general_info_data.get('bathrooms', instance.general_info.bathrooms)
            instance.general_info.agent_id = general_info_data.get('agent_id', instance.general_info.agent_id)
            instance.general_info.apartment_number = general_info_data.get('apartment_number', instance.general_info.apartment_number)
            instance.general_info.property_name = general_info_data.get('property_name', instance.general_info.property_name)
            instance.general_info.date_available = general_info_data.get('date_available', instance.general_info.date_available)
            instance.general_info.description = general_info_data.get('description', instance.general_info.description)
            instance.general_info.is_easy_apply = general_info_data.get('is_easy_apply', instance.general_info.is_easy_apply)
            instance.general_info.save()

        economic_info_data = validated_data.pop('economic_info', {})
        if economic_info_data is not None:
            if instance.economic_info:
                instance.economic_info.cost = economic_info_data.get('cost', instance.economic_info.cost)
                instance.economic_info.updated_cost = economic_info_data.get('updated_cost', instance.economic_info.updated_cost)
                instance.economic_info.save()
            else:
                economic_info_instance = EconomicInfo.objects.create(
                    cost=economic_info_data.get('cost', 0), 
                    updated_cost=economic_info_data.get('updated_cost', 0)  
                )
                instance.economic_info = economic_info_instance
                instance.save()

        amenities_data = validated_data.pop('amenities', [])
        if amenities_data:
            instance.amenities.clear()  
            for amenity_data in amenities_data:
                amenity_instance, _ = AmenityInfo.objects.get_or_create(**amenity_data)
                instance.amenities.add(amenity_instance)

        charge_info_data = validated_data.pop('charge_info', {})
        if charge_info_data is not None:
            if instance.charge_info:
                instance.charge_info.first_month_rent = charge_info_data.get('first_month_rent', instance.charge_info.first_month_rent)
                instance.charge_info.security_deposit = charge_info_data.get('security_deposit', instance.charge_info.security_deposit)
                instance.charge_info.broker_fee = charge_info_data.get('broker_fee', instance.charge_info.broker_fee)
                instance.charge_info.application_fee = charge_info_data.get('application_fee', instance.charge_info.application_fee)
                instance.charge_info.extra_fee_name = charge_info_data.get('extra_fee_name', instance.charge_info.extra_fee_name)
                instance.charge_info.extra_fee_cost = charge_info_data.get('extra_fee_cost', instance.charge_info.extra_fee_cost)
                instance.charge_info.save() 

                extra_fee_data = charge_info_data.pop('extra_fee', [])
                if extra_fee_data:
                    instance.charge_info.extra_fee.clear() 
                    for extra_fee_data_item in extra_fee_data:                      
                        extra_fee_instances = ExtraFee.objects.filter(**extra_fee_data_item)
                        if extra_fee_instances.exists():
                            extra_fee_instance = extra_fee_instances.first()
                        else:
                            extra_fee_instance = ExtraFee.objects.create(**extra_fee_data_item)
                        instance.charge_info.extra_fee.add(extra_fee_instance)
            else:
                charge_info_instance = ChargeInfo.objects.create(
                    first_month_rent=charge_info_data.get('first_month_rent', 0), 
                    security_deposit=charge_info_data.get('security_deposit', 0), 
                    broker_fee=charge_info_data.get('broker_fee', 0),  
                    application_fee=charge_info_data.get('application_fee', 0),  
                    extra_fee_name=charge_info_data.get('extra_fee_name', ''),
                    extra_fee_cost=charge_info_data.get('extra_fee_cost', 0), 
                )
                extra_fee_data = charge_info_data.pop('extra_fee', [])
                for extra_fee_data_item in extra_fee_data:
                    extra_fee_instances = ExtraFee.objects.filter(**extra_fee_data_item)
                    if extra_fee_instances.exists():
                        extra_fee_instance = extra_fee_instances.first()
                    else:
                        extra_fee_instance = ExtraFee.objects.create(**extra_fee_data_item)
                    charge_info_instance.extra_fee.add(extra_fee_instance)
                instance.charge_info = charge_info_instance
                instance.save()  

        utility_info_data = validated_data.pop('utility_info', {})
        if utility_info_data:
            if instance.utility_info:
                instance.utility_info.gas = utility_info_data.get('gas', instance.utility_info.gas)
                instance.utility_info.sewage = utility_info_data.get('sewage', instance.utility_info.sewage)
                instance.utility_info.electricity = utility_info_data.get('electricity', instance.utility_info.electricity)
                instance.utility_info.internet = utility_info_data.get('internet', instance.utility_info.internet)
                instance.utility_info.water = utility_info_data.get('water', instance.utility_info.water)
                instance.utility_info.garbage = utility_info_data.get('garbage', instance.utility_info.garbage)
                instance.utility_info.cable = utility_info_data.get('cable', instance.utility_info.cable)
                instance.utility_info.satellite_tv = utility_info_data.get('satellite_tv', instance.utility_info.satellite_tv)
                instance.utility_info.other_utilities = utility_info_data.get('other_utilities', instance.utility_info.other_utilities)
                instance.utility_info.save()
            else:
                utility_info_instance = UtilityInformation.objects.create(
                    gas=utility_info_data.get('gas', False), 
                    sewage=utility_info_data.get('sewage', False),
                    electricity=utility_info_data.get('electricity', False),
                    internet=utility_info_data.get('internet', False),
                    water=utility_info_data.get('water', False),
                    garbage=utility_info_data.get('garbage', False),
                    cable=utility_info_data.get('cable', False),
                    satellite_tv=utility_info_data.get('satellite_tv', False),
                    other_utilities=utility_info_data.get('other_utilities', ''),
                )
                instance.utility_info = utility_info_instance
                instance.save()

        document_info_data = validated_data.pop('document_info', {})
        if document_info_data is not None:
            if instance.document_info:
                documents_data = document_info_data.pop('documents', [])
                if documents_data:
                   instance.document_info.documents.clear()
                for document_data in documents_data:
                    document_instances = Documents.objects.filter(**document_data)
                    if document_instances.exists():
                        document = document_instances.first()
                    else:
                        document = Documents.objects.create(**document_data)
                    instance.document_info.documents.add(document)
            else:
                document_info_instance = DocumentInfo.objects.create()
                documents_data = document_info_data.pop('documents', [])
                for document_data in documents_data:
                    document_instances = Documents.objects.filter(**document_data)
                    if document_instances.exists():
                        document = document_instances.first()
                    else:
                        document = Documents.objects.create(**document_data)
                    document_info_instance.documents.add(document)
                instance.document_info = document_info_instance
                instance.save()
                
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance