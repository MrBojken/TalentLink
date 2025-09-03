TalentLink
==========

  
TalentLink is a modern freelance job board platform where clients can 
post jobs and freelancers can submit proposals. 
The platform is designed to connect skilled professionals with clients seeking their 
services, providing a clean interface for job searching, proposal management, and user profiles.

### Features 🚀

*   **Role-Based User Profiles:** Two distinct user roles: **Client** and **Freelancer**.
    
*   **Job Management:** Clients can create, edit, and delete job listings.
    
*   **Proposal System:** Freelancers can submit proposals for jobs, including a cover letter, 
  * proposed rate, and a file attachment (e.g., a resume).
    
*   **Job Completion & Reviews:** Clients can mark a job as complete and 
  * leave a review and a 5-star rating for the freelancer.
    
*   **Freelancer Ratings:** The average rating and all received reviews are displayed on the freelancer's public profile.
    
*   **Robust Authentication:**
    
    *   Standard email/password sign-up and log-in.
        
    *   Integrated Google OAuth2 social authentication with a custom flow for role selection.
        
*   **Profile Management:** Users can view and edit their profiles, including personal details and a profile picture.
    
*   **Robust Backend:** The system is built with Django and includes 
  * custom template filters and a robust database schema.
    

### Technologies Used 💻

*   **Backend:**
    
    *   Python 3.12
        
    *   Django 5.2.5
        
*   **Database:**
    
    *   SQLite3 (default, for development)
        
*   **Frontend:**
    
    *   HTML5
        
    *   Bootstrap 5.3
        
*   **Key Libraries:**
    
    *   **django-allauth:** For authentication and social logins.
        
    *   **django-crispy-forms:** For clean and structured form rendering.
        
    *   **Pillow:** For image processing.
        

### Getting Started 📥

Follow these steps to get a local copy of the project up and running.

#### Prerequisites

*   Python 3.12 or newer
    
*   Git
    
*   A code editor (e.g., VS Code, PyCharm)
    

#### Installation

1.  git clone https://github.com/MrBojken/TalentLink.git
    
2.  cd TalentLink
    
3.  python -m venv venv
    
4.  **Activate the virtual environment:**
    
    *   venv\\Scripts\\activate (Windows)
        
    *   source venv/bin/activate (macOS/Linux)
        
5.  pip install -r requirements.txt
    
6.  python manage.py makemigrations
    
7.  python manage.py migrate
    
8.  python manage.py createsuperuser
    
9.  python manage.py runserver
    

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Configuration ⚙️

#### Google Social Authentication

To enable Google sign-in, you must configure a Google API project and add your credentials to the project's settings.

1.  Create an OAuth 2.0 Client ID in the Google Cloud Console.
    
2.  Add http://127.0.0.1:8000 to the **Authorized JavaScript origins**.
    
3.  Add http://127.0.0.1:8000/accounts/google/login/callback/ to the **Authorized redirect URIs**.
    
4.  Copy your **Client ID** and **Client Secret**.
    
5.  In the Django Admin (/admin), navigate to **Social Applications** and add a new entry for Google with your credentials.

### Business Inquiries 🤝
 For collaboration or business inquiries, please contact me directly at [bojkentocila57@gmail.com].