# Social Media API

The Airport RESTful API for a social media platform. The API allows users to create profiles, follow other users, create and view posts, manage likes and comments, and perform basic social media actions.

## Table of Contents

- [Installation](#installation)
- [Run with docker](#run-with-docker)
- [Getting access](#getting-access)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [General Features](#general-features)
- [DB Structure](#db-structure)
- [An example of using the API](#an-example-of-using-the-api)

## Installation

Install PostgreSQL and create db

```bash
git clone https://github.com/AlexTsikhun/social-media-api
cd social-media-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# for postgres set env variables
python3 manage.py makemigations
python3 manage.py migate
python3 manage.py runserver

```

## Run with docker
Docker should be installed locally (no need to install Postgres)

```bash
docker compose build
docker compose up
```

## Getting access

- Create user via `api/v1/user/register/`
- Get access token `api/v1/user/token/`
- API Root `api/v1/social_media/`

## Technologies Used

- Django, DRF
- Celery, Redis
- PostgreSQL (for production), Sqlite3 (for test)
- Docker, docker compose
- Unittest

## Features:
- schedule Post creation using Celery
- Using Django Signals when creating a user, a profile is created automatically 
- JWT authenticated
- Admin panel `/admin/`
- Documentation is located at `api/doc/swagger-ui/` or `api/doc/redoc/`
- Managing Profile and Posts
- Used fat models for create Posts, Likes and add Comments
- Filtering followers, following
- Throttling, Pagination for Posts, Adding profile and post images  
- Validation for Flight.....

### General Features

User Registration and Authentication:

- Users can register with their email and password to create an account.

- Users can log in with their credentials and receive a token for authentication.

- Users can log out and invalidate their token.

User Profile:

- Users can create and update their profile, including profile picture, bio, and other details.

- Users can retrieve their own profile and view profiles of other users.

- Users can search for users by username or other criteria.

Follow/Unfollow:

- Users can follow and unfollow other users. (Delete in followers/following pages - like unfollow)

- Users can view the list of users they are following and the list of users following them.

Post Creation and Retrieval:

- Users can create new posts with text content and optional media attachments (e.g., images).

- Users can get their own posts and posts of users they are following.

- Users can get posts by hashtags or other criteria.

Likes and Comments:

- Users can like and unlike posts. Users can view the list of posts they have liked. Users can add comments to posts and view comments on posts.

Schedule Post creation using Celery:

- Added possibility to schedule Post creation (you can select the time to create the Post before creating of it).

API Permissions:

- Only authenticated users can perform actions such as creating posts, liking posts, and following/unfollowing users.

- Users can only be able to update and delete their own posts and comments.

- Users should only be able to update and delete their own profile.

API Documentation:

- The API is well-documented with clear instructions on how to use each endpoint.

- The documentation is included sample API requests and responses for different endpoints.

Technical Requirements:

- Used Django and Django REST framework to build the API.

- Used token-based authentication for user authentication.

- Used appropriate serializers for data validation and representation.

- Used appropriate views and viewsets for handling CRUD operations on models.

- Used appropriate URL routing for different API endpoints.

- Used appropriate permissions and authentication classes to implement API permissions.

- Followed best practices for RESTful API design and documentation.

#### DB Structure:

.....

### An example of using the API

A list of some of the main endpoints

....

<details style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px">
<summary style="font-size: 1.17em; font-weight: bold; ">toDo</summary>

- and posts of followed

- delete all user fields in my profile

- followers - follow creators; followees - who are followed by creators 
 
- чи тре пермішина якщо нема екшинів 

- following list filtered show id for all user, or I need personal (and comment)?

- thro

- profile/user-posts/ - no permission, show. deny acces in this endpoi ??

- followings??? not folllowing
- pic how set celery task
- 
after admin creation better to set username with admin panel (profile shows by username)

</details>

<details style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px">
<summary style="font-size: 1.17em; font-weight: bold; ">Future work</summary>

- can be `profiles` - with list of all profiles, `prof/<str>` ???
- if I redirect to profile, but profile is mine - open my-profile
- news - like posts but with filtering
</details>

