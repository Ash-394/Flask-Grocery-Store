from flask import jsonify, Blueprint, request
from flask_restful import Api, Resource


api = Blueprint('api', __name__)
api_rest = Api(api)

# API endpoint to get all sections and add new section
class SectionsResource(Resource):
    
    def get(self):
        from .models import db, Section
        sections = Section.query.all()
        section_data = [{"id": section.id, "name": section.name} for section in sections]
        return section_data

    def post(self):
        from .models import db,Section
        name = request.json.get('name')
        if not name:
            return {"error": "Section name is required"}, 400

        section = Section(name=name)
        db.session.add(section)
        db.session.commit()

        return {"success": True}, 201
    def put(self):
        return {"error":"HTTP PUT method is not allowed for this URL."}, 405

    def delete(self):
        return {"error":"HTTP DELETE method is not allowed for this URL."}, 405


# API endpoint to get, update, and delete a specific section by ID
class SectionResource(Resource):
    def get(self, section_id):
        from .models import db, Section
        section = Section.query.get(section_id)
        if not section:
            return {"error":"Section not found"}, 404

        section_data = {
            "id": section.id,
            "name": section.name
        }
        return jsonify(section_data)

    def post(self, section_id):
        return {"error":"HTTP POST method is not allowed for this URL."}, 405

    def put(self, section_id):
        from .models import db, Section
        section = Section.query.get(section_id)
        if not section:
            return {"error":"Section not found"}, 404

        name = request.json.get('name')
        if not name:
            return {"error": "Section name is required"}, 400

        section.name = name
        db.session.commit()

        return jsonify(success=True)

    def delete(self, section_id):
        from .models import db, Section
        section = Section.query.get(section_id)
        if not section:
            return {"error":"Section not found"}, 404

        db.session.delete(section)
        db.session.commit()

        return jsonify(success=True)


# API endpoint to get all products also add a new product
class ProductsResource(Resource):
    def get(self):
        from .models import Product
        products = Product.query.all()
        product_data = [{
            "id": product.id,
            "name": product.name,
            "manufacture_date": product.manufacture_date,
            "price": product.price,
            "quantity": product.quantity,
            "image_url": product.image_url,
            "section_id": product.section_id
        } for product in products]
        return jsonify(product_data)

    def post(self):
        from .models import db,Product
        name = request.json.get('name')
        manufacture_date = request.json.get('manufacture_date')
        price = request.json.get('price')
        quantity = request.json.get('quantity')
        image_url = request.json.get('image_url')
        section_id = request.json.get('section_id')

        if not name or not price or not quantity or not section_id:
            return {"error":"Name, price, quantity, and section ID are required fields."}, 400

        product = Product(name=name, manufacture_date=manufacture_date, price=price, quantity=quantity,
                          image_url=image_url, section_id=section_id)
        db.session.add(product)
        db.session.commit()

        return {"success": True}, 201
    
    def put(self):
        return {"error":"HTTP PUT method is not allowed for this URL."}, 405

    def delete(self):
        return {"error":"HTTP DELETE method is not allowed for this URL."}, 405


# API endpoint to get, update, and delete a specific product by ID
class ProductResource(Resource):
    def get(self, product_id):
        from .models import Product
        product = Product.query.get(product_id)
        if not product:
            return {"error":"Product not found"}, 404

        product_data = {
            "id": product.id,
            "name": product.name,
            "manufacture_date": product.manufacture_date,
            "price": product.price,
            "quantity": product.quantity,
            "image_url": product.image_url,
            "section_id": product.section_id
        }
        return jsonify(product_data)

    def post(self, product_id):
        return {"error":"HTTP POST method is not allowed for this URL."}, 405

    def put(self, product_id):
        from .models import db,Product
        product = Product.query.get(product_id)
        if not product:
            return {"error":"Product not found"}, 404

        name = request.json.get('name')
        manufacture_date = request.json.get('manufacture_date')
        price = request.json.get('price')
        quantity = request.json.get('quantity')
        image_url = request.json.get('image_url')
        section_id = request.json.get('section_id')

        if not name or not price or not quantity or not section_id:
            return {"error":"Name, price, quantity, and section ID are required fields."}, 400

        product.name = name
        product.manufacture_date = manufacture_date
        product.price = price
        product.quantity = quantity
        product.image_url = image_url
        product.section_id = section_id

        db.session.commit()

        return jsonify(success=True)

    def delete(self, product_id):
        from .models import db,Product
        product = Product.query.get(product_id)
        if not product:
            return {"error":"Product not found"}, 404

        db.session.delete(product)
        db.session.commit()

        return {"success": True}, 201

api_rest.add_resource(SectionsResource, '/api/sections')
api_rest.add_resource(ProductsResource, '/api/products')
api_rest.add_resource(SectionResource, '/api/sections/<int:section_id>')
api_rest.add_resource(ProductResource, '/api/products/<int:product_id>')



