# Grocery Store
- A Flask-based multi-user e-commerce app facilitates grocery shopping with efficient product management.

### Features and functions
- CRUD operations for sections and products \via the API.
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