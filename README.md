# Social Media API

The Social Media API is a RESTful web service for managing social media-related information. This API allows users to manage posts, comments, likes, followers, and user profiles. The API provides endpoints for various operations such as creating, reading, updating, and deleting resources. It also includes JWT authentication to secure the endpoints.

## Features

- User profile management
- Post management
- Comment management
- Like management
- Follower management
- JWT authentication


### Installation


Before getting started with the Social Media API, ensure that you have Python installed on your system. If Python is not installed, you can download and install it from the official Python website.

Once Python is installed, you can proceed with the following steps to set up the Social Media API:


```
git clone https://github.com/mish-sk/social-media-api.git
cd social-media-api
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

### Set up the database:
    
- Create the migrations:
   ```sh
   python manage.py makemigrations
   ```
    
- Run the migrations:
   ```sh
   python manage.py migrate
   ```
### Create a superuser:

 ```sh
 python manage.py createsuperuser
 ```

### Start the development server:
 ```sh
 python manage.py runserver
 ```


## License

This project is licensed under the MIT License.

---
