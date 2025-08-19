
from django.urls import path
from contacts import views


urlpatterns = [
    path('',views.contact_view,name='contact-view'),
    # path('contact-list/',views.contact_list,name='contact-list'),
    # path('contact-detail/<int:pk>/',views.contact_detail,name='contact-detail'),
    path('contact-list/',views.ContactListView.as_view(),name='contact-list'),
    path('contact-detail/<int:pk>/',views.ContactDetailView.as_view(),name='contact-detail'),

]
