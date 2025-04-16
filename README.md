# Website Builder

A web application built with Flask that allows users to create and manage tourist attractions and reviews.

## Features

- User authentication
- Tourist attraction management
- Review system
- Responsive design

## Installation

1. Clone the repository
```bash
git clone https://github.com/Mohammed-hani69/egypt-tourism-platform.git
cd egypt-tourism-platform
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. Initialize the database
```bash
flask db upgrade
```

6. Run the application
```bash
flask run
```

## Deployment

### GitHub Deployment

1. Initialize Git repository (if not already done)
```bash
git init
```

2. Add your files to Git
```bash
git add .
git commit -m "version 1.0.4"
```

3. Create a new repository on GitHub
   - Go to github.com
   - Click "New repository"
   - Name your repository
   - Do not initialize with README.md

4. Connect and push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

5. For subsequent updates
```bash
git add .
git commit -m "Your commit message"
git push
```

### Heroku Deployment

1. Install Heroku CLI and login
```bash
heroku login
```

2. Create a new Heroku app
```bash
heroku create your-app-name
```

3. Add PostgreSQL addon
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. Configure environment variables
```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DATABASE_URL=your_database_url
```

5. Deploy the application
```bash
git push heroku main
```

6. Initialize the database
```bash
heroku run flask db upgrade
```

### Production Considerations

- Use a production-grade server like Gunicorn
- Set up proper security headers
- Enable HTTPS
- Configure database backup
- Set up monitoring

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Bootstrap
- HTML/CSS
