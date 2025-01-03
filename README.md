
# Material Management and Order Processing API  

This project provides APIs for managing materials, processing orders, generating reports, and tracking usage trends. It includes Swagger and Schema Viewer integration for interactive API documentation and schema exploration.  

---

## Table of Contents  
- [Features](#features)  
- [Project Structure](#project-structure)  
- [Setup Instructions](#setup-instructions)  
  - [Database Configuration](#database-configuration)  
  - [Installation](#installation)  
- [API Routes](#api-routes)  
- [Schema and Documentation](#schema-and-documentation)  
- [Running the Project](#running-the-project)  
- [Running Test Cases](#running-test-cases)  

---

## Features  
- **Material Management**: CRUD operations for materials.  
- **Order Processing**: Manage customer orders.  
- **Reports**: Generate stock and usage reports.  
- **Interactive API Documentation**: Swagger UI for API exploration.  
- **Schema Viewer**: Explore database schema visually.  

---

## Project Structure  

The project is organized as follows:  
- `construction_api/`: Contains the main project files, such as `settings.py`, `urls.py`, and `wsgi.py`.  
- `materials/`: This is the API app folder, containing:  
  - `views.py`: API logic for materials, orders, and reports.  
  - `serializers.py`: Serializers for data validation and transformation.  
  - `testcases.py`: Contains test cases for validating the API functionality.  

---

## Setup Instructions  

### Database Configuration  
1. Open the `construction_api/settings.py` file.  
2. Configure the database settings under the `DATABASES` section. Example for PostgreSQL:  
    ```python  
    DATABASES = {  
        'default': {  
            'ENGINE': 'django.db.backends.postgresql',  
            'NAME': 'your_db_name',  
            'USER': 'your_db_user',  
            'PASSWORD': 'your_db_password',  
            'HOST': 'localhost',  
            'PORT': '5432',  
        }  
    }  
    ```  

### Installation  
1. Clone the repository:  
    ```bash  
    git clone https://github.com/your-username/your-repo.git  
    cd your-repo  
    ```  

2. Install dependencies:  
    ```bash  
    pip install -r requirements.txt  
    ```  

3. Apply migrations to create the necessary database tables:  
    ```bash  
    python manage.py makemigrations  
    python manage.py migrate  
    ```  

4. Create a superuser for admin access (optional):  
    ```bash  
    python manage.py createsuperuser  
    ```  

---

## API Routes  

### Material Management  
- `GET /materials/materials/` - List all materials.  
- `POST /materials/materials/` - Create a new material.  
- `GET /materials/materials/{id}/` - Retrieve a material by ID.  
- `PUT /materials/materials/{id}/` - Update a material by ID.  
- `DELETE /materials/materials/{id}/` - Delete a material by ID.  

### Order Processing  
- `GET /materials/orders/` - List all orders.  
- `POST /materials/orders/` - Create a new order.  
- `GET /materials/orders/{id}/` - Retrieve an order by ID.  
- `PUT /materials/orders/{id}/` - Update an order by ID.  
- `DELETE /materials/orders/{id}/` - Delete an order by ID.  

### Reports  
- `GET /reports/stock-levels/` - Get stock reports.  
- `GET /usage-trends/<int:material_id>/` - Get usage trends.  
- `GET /price-fluctuations/<int:material_id>/` - Gets price fluctuations of a particular product.
  
---

## Schema and Documentation  

### Swagger UI  
Swagger UI provides interactive API documentation.  
Add the following route to your `construction_api/urls.py`:  
```python  
path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')  
```  
Access Swagger at: `http://127.0.0.1:8000/swagger/`  

### Schema Viewer  
Schema Viewer offers a graphical view of the database schema.  
Add the following route to your `construction_api/urls.py`:  
```python  
path('schema-viewer/', include('schema_viewer.urls')),  
```  
Access Schema Viewer at: `http://127.0.0.1:8000/schema-viewer/`  

---

## Running the Project  
1. Start the Django development server:  
    ```bash  
    python manage.py runserver  
    ```  
2. Access the application at `http://127.0.0.1:8000/`.  
3. Explore the APIs using the Swagger UI or Schema Viewer.  

---

## Running Test Cases  
The test case file not complete configure yet.

---  
