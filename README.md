# CALLER ID
	Built Using Django Rest Framework
Instructions to Test API

### Install Dependencies
`pip install -r requirements.txt`

### Start the Server
`python3 manage.py runserver`

##Testing
> Preferred is Postman to Test the API. I consider you have it preinstalled.

###Sign Up
``` 
Route: 'http://localhost:8000/signup/'
Request Method: POST	
```
Body:
```json
{
	'username': 'john',
	'password': 'john',
	'email': 'john@doe.com',
	'phone': '9876567890'
}
```
You will get a **JWT AUTH** Token in the Preview, Note it down.
Example: `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwidXNlcm5hbWUiOiJyaXNoYWJoIn0.1nQGWWpjkMF3l0G2ACQoNRCmtMg9Eb5paBuLJda5PbY`

### Sign In
```
Route: 'http://localhost:8000/signin/'
Request Method: POST
``` 
Body:
```json
{
	'username': 'john',
	'password': 'john'
}
```

### Check all Contacts
```
Route: 'http://localhost:8000/contacts'
Request Method: GET
```

### Mark Contact as Spam
```
Route: 'http://localhost:8000/mark_spam/'
Request Method: POST
```
Body:
```json
{ 
	'phone': '7878787878'
}
```
>If the contact Does not Exist, It will be instantly created and marked as spam.

### Search By Name
```
Route: 'http://localhost:8000/search_by_name?name=Arpit'
Request Method: GET
```

### Search By Phone
```
Route: 'http://localhost:8000/search_by_phone?phone=9876543210'
Request Method: GET
```