import jwt
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Contact, ProfileUser, UserContactRelation
from .serializers import ContactSerializer


class SignUp(APIView):

	def post(self, request):
		username = request.data.get('username', None)
		password = request.data.get('password', None)
		phone = request.data.get('phone', None)
		email = request.data.get('email', None)

		user = User(
			username = username,
			password = password,
			email = email
		)

		user.set_password(password)
		user.save()

		user_profile = ProfileUser(
			user=user,
			phone=phone
		)
		user_profile.save()

		if user:
			payload = {
				'id': user.id,
				'username': user.username,
			}

			jwt_token = {'token': jwt.encode(payload, "TRUECALLER_KINDA_APP")}

			return Response(
				jwt_token,
				status=200,
				content_type="application/json"
			)
		else:
			return Response(
				json.dumps({'Error': "Error in signup"}),
				status=400,
				content_type="application/json"
			)


class SignIn(APIView):

	def post(self, request):
		if not request.data:
			return Response({'Error': "Username/Password field empty, No data received"}, status=400)

		username = request.data.get('username', None)
		password = request.data.get('password', None)

		if(authenticate(username=username, password=password)):
			user = User.objects.get(username= username)
		else:
			return Response({'Error': "Provided Username/Password is/are incorrect"}, status=400)

		if user:
			payload = {
				'id': user.id,
				'username': user.username,
			}

			jwt_token = {'token': jwt.encode(payload, "TRUECALLER_KINDA_APP")}

			return Response(
				jwt_token,
				status=200,
				content_type="application/json"
			)
		else:
			return Response(
				json.dumps({'Error': "Credentials are Invalid"}),
				status=400,
				content_type="application/json"
			)

class AuthenticateToken(BaseAuthentication):

	def authenticate(self, request):
		auth = get_authorization_header(request).split()

		if not auth or auth[0].lower() != b'bearer':
			return ('',{'Error': "Invalid Token"})

		if len(auth) == 1:
			message = "Token Header Invalid, No Credentials Provided"
			raise AuthenticationFailed(message)

		elif len(auth) > 2:
			message = "Token Header Invalid"
			raise AuthenticationFailed(message)

		try:
			token = auth[1]
			if token == 'null':
				message = "Null Token"
				raise AuthenticationFailed(message)

		except UnicodeError:
			message = "Token Header Invalid. Token Should Not Contain Invalid Strings Or Characters"
			raise AuthenticationFailed(message)

		return self.credentials_authentication(token)

	def credentials_authentication(self, token):
		try:
			payload = jwt.decode(token, "TRUECALLER_KINDA_APP")
			username = payload['username']
			userid = payload['id']
			user = User.objects.get(
				username = username,
				id = userid,
				is_active=True
			)

		except:
			return ('', {'Error': "Invalid Token"})

		return (user, '')

class Contacts(APIView):

	def get(self, request):
		contacts = Contact.objects.all()
		serializer = ContactSerializer(contacts, many=True)
		return Response(serializer.data)

	def post(self, request):
		auth = AuthenticateToken()
		user, error = auth.authenticate(request)
		if error:
			return Response(
				error,
				status=400,
				content_type="application/json"
			)
		else:
			name = request.data.get('name', None)
			phone = request.data.get('phone', None)
			email = request.data.get('email', None)

			contact = Contact(
				name=name,
				phone=phone,
				email=email
			)
			contact.save()

			relation = UserContactRelation(
				user=user,
				contact=contact
			)
			relation.save()

			response = {
				'message': "Contact Saved",
				'data': request.data
			}

			return Response(
				response,
				status=200,
				content_type="application/json"
			)

class MarkSpam(APIView):
	def post(self, request):
		try:
			auth = AuthenticateToken()
			user, error = auth.authenticate(request)

			if error:
				return Response(
					error,
					status=400,
					content_type="application/json"
				)
			else:
				phone = request.data.get('phone',None)
				list1 = Contact.objects.filter(phone=phone).update(spam=True)
				list2 = ProfileUser.objects.filter(phone=phone).update(spam=True)

				if (list1 + list2):
					return HttpResponse(
						json.dumps({'Message': "Marked as Spam"}),
						status=200,
						content_type="application/json"
					)

				else:
					new = Contact()
					new.name = str(phone)
					new.phone = phone
					new.email = 'dummy@dummy.com'
					new.spam = True
					new.save()
					return HttpResponse(
						json.dumps({'Message': "Marked as Spam, Contact Created"}),
						status=200,
						content_type="application/json"
					)
		except:
			return HttpResponse(
				json.dumps({'Error': "Server Error"}),
				status=500,
				content_type="application/json"
			)


class NameSearch(APIView):
	def get(self, request):

		try:
			auth = AuthenticateToken()
			user, error = auth.authenticate(request)
			if error:
				return Response(
					error,
					status=400,
					content_type="application/json"
				)
			else:
				name = request.GET.get('name', None)

				contact_a = Contact.objects.all().filter(name=name)
				contact_b = Contact.objects.all().filter(name__contains=name).exclude(name=name)

				response = []

				for contact in contact_a:
					response.append({
						'name': contact.name,
						'phone': contact.phone,
						'spam': contact.spam
					})

				for contact in contact_b:
					response.append({
						'name': contact.name,
						'phone': contact.phone,
						'spam': contact.spam
					})

				return Response(
					response,
					status=200,
					content_type="application/json"
				)
		except:
			return HttpResponse(
				json.dumps({'Error': "Server Error"}),
				status=500,
				content_type="application/json"
			)

class PhoneSearch(APIView):
	def get(self, request):

		try:
			auth = AuthenticateToken()
			user, error = auth.authenticate(request)

			if error:
				return Response(
					error,
					status=400,
					content_type="application/json"
				)
			else:
				phone = request.GET.get('phone', None)
				profile = ProfileUser.objects.get(phone=phone)

				if profile:
					user = User.objects.get(
						id = profile.id,
						is_active=True
					)
				response = {
					'name': user.username,
					'email': user.email,
					'phone': profile.phone,
					'spam': profile.spam
				}

				return Response(
					response,
					status=200,
					content_type="application/json"
				)
		except ProfileUser.DoesNotExist:
			contacts = Contact.objects.all().filter(phone=phone)
			response = []
			for contact in contacts:
				response.append({
					'name': contact.name,
					'email': contact.email,
					'phone': contact.phone,
					'spam': contact.spam
				})
			return Response(
				response,
				status=200,
				content_type="application/json"
			)
		except:
			return HttpResponse(
				json.dumps({'Error': "Contact Not Found"}),
				status=400,
				content_type="application/json"
			)
