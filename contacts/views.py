from django.http import HttpResponse
# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics,permissions
from contacts.models import Contact
from .serializers import ContactSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User


# Create your views here.


# contacts/views.py
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)



def contact_view(request):
    return HttpResponse('welcome')


# @api_view(['GET','POST'])
# def contact_list(request):
#     if request.method == 'GET':
#         contacts = Contact.objects.all()
#         serializer = ContactSerializer(contacts,many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ContactSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET','PUT','Delete'])
# def contact_detail(request,pk):

#     try:
#         contact = Contact.objects.get(pk=pk)
#     except Contact.DoesNotExist:
#         return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = ContactSerializer(contact)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     elif request.method == 'PUT':
#         serializer = ContactSerializer(contact,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'Delete':
#         contact.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        


# class ContactListView(generics.ListCreateAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Contact.objects.all()
#     serializer_class = ContactSerializer
#     permission_classes = [permissions.IsAuthenticated]





from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Contact
from .serializers import ContactSerializer
from .permissions import IsOwner  # import custom permission

# List & create contacts
class ContactListView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return contacts owned by the logged-in user
        return Contact.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Set the owner to the logged-in user
        serializer.save(owner=self.request.user)

# Retrieve, update, delete a single contact
class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwner]  # enforce object-level authorization

    def get_queryset(self):
        # Only allow access to contacts owned by the logged-in user
        return Contact.objects.filter(owner=self.request.user)



