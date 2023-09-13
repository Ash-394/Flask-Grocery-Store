# Grocery Store
- A Flask-based multi-user e-commerce app facilitates grocery shopping with efficient product management.

### Features and functions
- CRUD operations for sections and products via the API.
- Multi-user authentication: Admin and user login and sign-up.
- Inventory and product management: Admin can add, edit, and delete products and sections
- Streamlined processing: Users can search for sections and purchase products from one or multiple categories.
- Summary Generation: A summary page visually presents statistics through pie charts and bar charts for products and orders.


### Technologies used
- Flask: A micro web framework used for building the backend of the application.
- Flask-RESTful: An extension for creating RESTful APIs to manage product and section data.
- Flask-SQLAlchemy: An Object-Relational Mapping (ORM) tool that facilitates database interaction and seamless integration with Flask.
- Flask-Login: An extension enabling user authentication and session management.
- SQLite: A relational database utilized for storing product, section, and order data.
- matplotlib: A library used for generating charts and graphs within the application.
- HTML, Jinja2 templates, Bootstrap: Frontend technologies employed for designing the user interface.

### How to run
- Clone this repo using `git clone` or download it as a zip folder
- Open terminal inside the folder
- Install dependencies: ` pip install -r requirements.txt `
- Run the app:`flask --app main run` or `python main.py`

Once the app is started we can click on the url generated where the server is running.

### API Design 
The API was designed using Flask-RESTful. The following endpoints were created: 
- /api/sections: GET and POST methods for retrieving all sections and adding a new section. 
- /api/sections/<int:section_id>: GET, PUT, and DELETE methods to access, update, and delete a 
specific section by ID. 
- /api/products: GET and POST methods for retrieving all products and adding a new product. 
- /api/products/<int:product_id>: GET, PUT, and DELETE methods for accessing, updating, and 
deleting a specific product by ID. 

### Architecture and Features 
- The project follows the MVC (Model-View-Controller) pattern The controllers are defined in the api.py(API endpoints) and routes.py(views) files. 
- The models.py file contains the database models using SQLAlchemy. 
- The templates folder contains the HTML templates for rendering the frontend. The static folder stores static assets like images.

[Video](https://drive.google.com/file/d/1tLJYG6vYCNv_mYgZYcgIWO-v0TX1NG3p/view?usp=sharing)
