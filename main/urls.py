from django.urls import path
from main import views

urlpatterns = [
	path('signup/', views.SignUp.as_view()),
	path('signin/', views.SignIn.as_view()),
	path('mark_spam/', views.MarkSpam.as_view()),
	path('search_by_name/', views.NameSearch.as_view()),
	path('search_by_phone/', views.PhoneSearch.as_view()),
	path('contacts/', views.Contacts.as_view()),
]