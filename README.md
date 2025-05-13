# Foodgram-st
Документация [**на Русском языке (RU)**](https://github.com/I-love-linux-12-31/foodgram-st/blob/main/README_RU.md)
## Project Description

Foodgram is a web application and API for publishing recipes and creating a list of necessary ingredients, built using Django 5. 
Authorized users can publish recipes, add favorite recipes to their bookmarks, 
subscribe to other authors' publications, and create a shopping list for selected recipes.

Any site visitor can browse the recipe catalog.

**Author: Yaroslav Kuznetsov**

## Project Structure

### Main Components
* backend - API and administrator web interface
  * run_dev_server.sh - Server launch script
  * container-entry-point.sh - Server launch script in container (Runs automatically when needed)
  * load_ingredients.py - Script for loading ingredient list into database (Runs automatically)
  * create_test_data.py - Script for loading demo data into database (Runs automatically or manually, depending on configuration)
* frontend - User interface
* gateway / nginx - Web server
* db (Container only, optional) - Database: PostgreSQL

### Additional Components
* infra - Configuration for running the frontend without other services
* data - Prepared data (link for compatibility)
* docs - Documentation
* postman-collection - API tests

### Files
* docker-compose.yaml - Docker-compose configuration
* docker-example.env - Example file with environment variables for application launch
* README.md / README_RU.md - Project description
* setup.cfg - Linter configuration

## Technologies
### Backend
* Python 3.13
* Django 5.2
* Django REST Framework
* PostgreSQL

### Frontend
* JavaScript
* React

### Other
* Docker / Podman
* NGINX

## Deployment

⚠️ After launch(container creation), the application may need **3-7 minutes** to startup (on first run).

The environment variable ``DEMO_DATA=1`` controls the loading of demonstration data.
Authentication data for test users:

user<int>@example.com: password123

User user1@example.com is an administrator

### Containerized Version: Quick Deploy
No project download required!
**Supported only on Linux!**

Dependencies:
* docker-compose/podman-compose
* wget
* curl
* bash

Docker-compose:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/I-love-linux-12-31/foodgram-st/refs/heads/main/fast_deploy.sh)
```
Podman-compose:
```bash
USE_PODMAN=1 bash <(curl -fsSL https://raw.githubusercontent.com/I-love-linux-12-31/foodgram-st/refs/heads/main/fast_deploy.sh)
```

What the script does:
1) Downloads configuration files
2) Launches containers via docker/podman compose

### Containerized Version: With Building from sources
```bash
git clone https://github.com/I-love-linux-12-31/foodgram-st.git
cd foodgram-st
```

Docker-compose:
```bash
cp ./docker-example.env ./docker.env # Create .env file from template
# Edit docker.env file 
docker-compose build 
docker-compose up
```

### Running Only the Backend Server
Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Environment variables are automatically loaded from the ``backend/.env`` file.
If it's located in a different directory or has a different name, you'll need to load it manually.

Activating the .env file, where ".env" is the name/path to the file:
```bash
set -a
source .env
```

**⚠️ Note:** ``DEBUG=1`` not only enables debug mode but also tells the backend to handle static requests itself, without nginx.

#### Production
```bash
cd backend
set -a
source .env
python3 -m gunicorn --bind 0.0.0.0:8000 backend.wsgi
```

Alternative method:
```bash
cd backend
DEBUG=0 ./run_dev_server.sh
```

#### Development Server
```bash
cd backend
DEBUG=1 ./run_dev_server.sh
```

## Tests
⚠️ Postman tests are NOT compatible with all demo data. ``DEMO_DATA=0`` recommended.    
### Linter
```bash
ruff check backend/
```

```bash
flake8 | grep W
flake8 | grep E
```

### Postman
See docs in postman_collection folder
