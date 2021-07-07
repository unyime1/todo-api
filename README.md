# Todo Api
This is a lightweight todo API built with Python, Django and Djangorestframework. 

## API Endpoints
```python
### BaseUrl
http://127.0.0.1:8000/
### Endpoints
user/register/ #user registration (post request)
user/login/ #user login (post request)

todo/<str:user_pk>/create/ #create a todo (post request)
todo/<str:user_pk>/ #get user's todo list (get request)
todo/<str:user_pk>/<str:todo_pk>/ #get a todo (get request)
todo/<str:user_pk>/<str:todo_pk>/update #update a todo (put request)
todo/<str:user_pk>/<str:todo_pk>/delete #delete a todo (delete request)

### Alternative Endpoints
todo/ #create todo(post request), get todo(get request)
todo-detail/<str:pk>/ #get todo detail(#get request), update a todo(put request), delete a todo(delete request) 

#Note that: 
# <str:user_pk> represents a user's email address
# <str:todo_pk> represents a todo's unique code
#<str:pk> represents a todo's unique code

``` 

## Installation
Clone this repo and run the following commands

```bash
pip install -r requirements.txt
python manage.py runserver
```

## Run with docker
Build and run this container with
```bash
docker build --tag python-todo-api .
docker run --publish 8000:8000 python-todo-api
```


## Run Tests
Run tests with
```bash
python manage.py test
```

## API Documentation
To view this API's documentation, follow the following steps:
1. Head over to [Swagger Editor](https://editor.swagger.io/), and click on the ```file``` option at the top right.
2. Click on ```Import File```, and upload the [this yaml file](https://github.com/unyime1/todo-api/blob/master/openapi.yaml) to get started. You can also view the [html version](https://github.com/unyime1/todo-api/blob/master/docs.html) locally on your browser.
