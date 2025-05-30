# Django Blog Platform
go to the 127.0.0.1/blog  to run the wbsite perfectly
A fully functional blog website built using Django. Includes features like:

- User Registration and Login
- Profile Picture Upload
- Create, Read, and Delete Blog Posts
- Commenting System
- Responsive UI with custom styling

## Technologies Used
- Python 3
- Django 5
- HTML, CSS
- SQLite3 (default database)
- Bootstrap or custom CSS (optional)

## How to Run Locally

```bash
git clone https://github.com/sutarvaibhav649/blog-website.git
cd newproject
python -m venv env
source env/bin/activate  # on Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

