from rest_framework import viewsets,status 
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import GeneralInfo, Property, Address, EconomicInfo, AmenityInfo, ChargeInfo, ExtraFee ,UtilityInformation,DocumentInfo,Documents,CustomUser
# from rest_framework.decorators import permission_classes
from .serializers import GeneralInfoSerializer, PropertySerializer, AddressSerializer, EconomicInfoSerializer, ExtraFeeSerializer,AmenityInfoSerializer,ChargeInfoSerializer,UtilityInfoSerializer,DocumentInfoSerializer,DocumentsSerializer,UserAuthenticationSerializer
# from .decorators import check_credentials

from functools import wraps
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status

# @check_credentials
class UserExistsView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user_exists = CustomUser.objects.filter(email=email,password=password).exists()
        if user_exists:
            return Response({'User Verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid User '}, status=status.HTTP_404_NOT_FOUND)
  
class UserViewSet(viewsets.ModelViewSet):
        queryset = CustomUser.objects.all()
        serializer_class = UserAuthenticationSerializer

class MyPageNumberPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  

class GeneralInfoViewSet(viewsets.ModelViewSet):
    queryset = GeneralInfo.objects.all()
    serializer_class = GeneralInfoSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    pagination_class = MyPageNumberPagination
    # permission_classes = [IsAuthenticated]
    # @check_credentials
    # def create(self, request, *args, **kwargs):
    #     user = request.user
    #     if user:
    #         # agent_id = user.id
    #         # request.data['agent'] = agent_id  # Add agent_id to request data
    #         # serializer = self.get_serializer(data=request.data)
    #         # serializer.is_valid(raise_exception=True)
    #         # self.perform_create(serializer)
    #         return Response(user, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({'error': 'Only agents can add properties.'}, status=status.HTTP_403_FORBIDDEN)
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class EconomicInfoViewSet(viewsets.ModelViewSet):
    queryset = EconomicInfo.objects.all()
    serializer_class = EconomicInfoSerializer


class AmenityInfoViewSet(viewsets.ModelViewSet):
    queryset = AmenityInfo.objects.all()
    serializer_class = AmenityInfoSerializer

class ChargeInfoViewSet(viewsets.ModelViewSet):
    queryset = ChargeInfo.objects.all()
    serializer_class = ChargeInfoSerializer

class ExtraFeeViewSet(viewsets.ModelViewSet):
    queryset = ExtraFee.objects.all()
    serializer_class = ExtraFeeSerializer

class UtilityInfoViewSet(viewsets.ModelViewSet):
    queryset = UtilityInformation.objects.all()
    serializer_class = UtilityInfoSerializer

class DocumentInfoViewSet(viewsets.ModelViewSet):
    queryset = DocumentInfo.objects.all()
    serializer_class = DocumentInfoSerializer

class DocumentsViewSet(viewsets.ModelViewSet):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer