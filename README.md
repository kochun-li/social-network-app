# Social Network Web Application

## Description
This project is a nano-blogging social network built using Django, designed for users to create posts, comment, follow/unfollow others, and interact in real-time. The project evolves adding features such as user authentication, profile management, AJAX-based updates, and cloud deployment.

## Features
- **User Authentication:** Register, login, and logout using Django's authentication system.
- **Posting & Commenting:** Users can create posts, comment on posts, and interact with others.
- **User Profiles:** Each user has a profile with a bio and profile picture.
- **Following System:** Users can follow/unfollow others, and view a personalized follower stream.
- **AJAX-based Updates:** Posts and comments update in real-time without refreshing the page.
- **Cloud Deployment:** Hosted on a cloud platform (AWS EC2).

## Installation
### Prerequisites
- Python 3.13
- Django 5.1
- MySQL (for deployment; SQLite for local development)
- AWS EC2

### Steps
1. **Clone the repository**
   ```sh
   git clone https://github.com/kochun-li/social-network-app.git
   cd socialnetwork

2. **Set up a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt

4. **Apply migrations and run the server**
    ```sh
    python manage.py migrate
    python manage.py runserver


## Technologies Used
- Backend: Django, Django Forms, Django ORM
- Database: SQLite (local), MySQL (deployment)
- Frontend: HTML, CSS, JavaScript, AJAX
- Cloud Hosting: AWS EC2
- Storage: AWS S3 (for profile pictures)
