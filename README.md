# PDF Vault Project Description
I used **Django Rest Framework** to create the API. Also, I used the default **DBMS** of Django which is **SQLite**.

---
## Installation
- Python should be installed in your device
- Install `pipenv` package using cmd command `pip install pipenv`
- Move to the project directory and type in cmd `pipenv shell`
- Install all the pacakges of the project using `pipenv install`
- Run the server using command `python manage.py runserver` 
- You will see the  name localhost link in the cmd, copy and opoen in browser

---
## Testing using Django Rest Framework
- create a user using `create-user/` endpoint
- login using the form link at the top right of the website
- start testing the api using the provided UI

---
## Testing in Postman

- `'create-user/'` :
    - Method:
        - POST
    - Postman Test:
        - add `username` and `password` to form data and send
    - Example URL:
        - [http://localhost:8000/create-user/](http://localhost:8000/create-user/)
- `'upload-pdf/'` :
    - Method:
        - POST
    - Postman Test
        - add `basic auth` data of the created user
        - add the pdf file as form data and send field name is: `file`
    - Example URL:
        - [http://localhost:8000/upload-pdf/](http://localhost:8000/upload-pdf/)
- `'pdfs-list/'` :
    - Method:
        - GET
    - Postman Test:
        - add `basic auth` data of the created user and send
    - Example URL:
        - [http://localhost:8000/pdfs-list/](http://localhost:8000/pdfs-list/)
- `'word-search/<str:word>'` :
    - Method:
        - GET
    - Postman Test:
        - add `basic auth` data of the created user
        - replace the `<str:word>` with a word of your choice and send
    - Example URL:
        - [http://localhost:8000/word-search/coin](http://localhost:8000/word-search/coin)
- `'retreive-pdf/<int:id>'` :
    - Method:
        - GET
    - Postman Test:
        - add `basic auth` data of the created user
        - replace the  `<int:id>` with an id of a pdf of your choice and send
    - Example URL:
        - [http://localhost:8000/retreive-pdf/12](http://localhost:8000/retreive-pdf/12)
- `'retreive-sentences/<int:id>'` :
    - Method:
        - GET
    - Postman Test:
        - add `basic auth` data of the created user
        - replace the  `<int:id>` with an id of a pdf of your choice and send
    - Example URL:
        - [http://localhost:8000/retreive-sentences/12](http://localhost:8000/retreive-sentences/12)
- `'word-occurrence/<int:id>/<str:word>'` :
    - Method:
        - GET
    - Postman Test:
        - add `basic auth` data of the created user
        - replace the  `<int:id>` with an id of a pdf of your choice
        - replace the  `<str:word>` with a word of your choice
    - Example URL:
        - [http://localhost:8000/word-occurrence/5/code](http://localhost:8000/word-occurrence/550/code)
- `'top-5-words/<int:id>'` :
    - Method:
        - GET
    - Postman Test:
        - add `basic auth` data of the created user
        - replace the  `<int:id>` with an id of a pdf of your choice
    - Example URL:
        - [http://localhost:8000/top-5-words/17](http://localhost:8000/top-5-words/167)
- `'get-page-image/<int:id>/<int:pageNo>'` :
    - Method:
        - GET
    - Postman Test:
        - add `basic auth` data of the created user
        - replace the  `<int:id>` with an id of a pdf of your choice
        - replace the `<int:pageNo>` with a page number of your choice
    - Example URL:
        - [http://localhost:8000/get-page-image/12/2](http://localhost:8000/get-page-image/12/0)
- `'delete-pdf/<int:id>'` :
    - Method:
        - DELETE
    - Postman Test:
        - add `basic auth` data of the created user
        - replace the  `<int:id>` with an id of a pdf of your choice
    - Example URL:
        - [http://localhost:8000/delete-pdf/12](http://localhost:8000/delete-pdf/12)


