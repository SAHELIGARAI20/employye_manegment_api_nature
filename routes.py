from flask import Blueprint, request, jsonify
from models import db, Employee
from sqlalchemy.exc import IntegrityError
api = Blueprint('api', __name__)
@api.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = db.get_or_404(Employee, id)
    return jsonify(employee.to_dict()), 200
@api.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'phone_number', 'email','gender']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    new_employee = Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone_number=data['phone_number'],
        email=data['email'],
        gender=data['gender']
    )
    try:
        db.session.add(new_employee)
        db.session.commit()
        return jsonify(new_employee.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 400
@api.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = db.get_or_404(Employee, id)
    data = request.get_json()
    if 'email' in data and data['email'] != employee.email:
        return jsonify({'error': 'Email cannot be changed'}), 400
    employee.first_name = data.get('first_name', employee.first_name)
    employee.last_name = data.get('last_name', employee.last_name)
    employee.phone_number = data.get('phone_number', employee.phone_number)
    employee.gender = data.get('gender', employee.gender)
    try:
        db.session.commit()
        return jsonify(employee.to_dict()), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@api.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = db.get_or_404(Employee, id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500