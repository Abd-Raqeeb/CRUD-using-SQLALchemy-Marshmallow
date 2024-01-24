from flask import Flask, request, jsonify
from models import db, Student
from schema import ma, StudentSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Student.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

ma.init_app(app)
db.init_app(app)

student_obj = StudentSchema()
students_obj = StudentSchema(many=True)

@app.route("/add_data/", methods=['POST'])
def add_student():
    data = request.json
    required_data = ['name', 'age', 'email', 'mobile_number']

    for i in required_data:
        if i not in data:
            miss_data = [i for i in required_data if i not in data]
            return jsonify({"error": f"Missing required fields: {', '.join(miss_data)}"}), 400

    new_stud = Student(
        name=data['name'],
        age=data['age'],
        email=data['email'],
        mobile_number=data['mobile_number']
    )
    db.session.add(new_stud)
    db.session.commit()
    print(new_stud)
    return jsonify({"message": "Student added successfully"}), 201  # Changed status code to 201 Created

@app.route("/get_all_data", methods=['GET'])
def get_all():
    data = Student.query.all()
    student_schema = StudentSchema(many=True)
    result = student_schema.dump(data)
    print(result)
    return jsonify({"Data": result}), 200

@app.route("/get_data/<int:id>", methods=['GET'])
def get_one(id):
    data = Student.query.get(id)

    if data is not None:
        student_schema = StudentSchema()
        result = student_schema.dump(data)
        return jsonify({"Data": result}), 200
    else:
        return jsonify({"message": "Student not found"}), 404

@app.route("/update_data/<int:id>", methods=['PUT'])
def update_student(id):
    Id = Student.query.get(id)

    if Id is None:
        return jsonify({"error": "Student not found"}), 404

    data_str = request.json

    required_data = ['name', 'age', 'email', 'mobile_number']

    for i in required_data:
        if i not in data_str:
            miss_data = [i for i in required_data if i not in data_str]
            return jsonify({"error": f"Missing required fields: {', '.join(miss_data)}"}), 400

    Id.age = data_str['age']
    Id.name = data_str['name']
    Id.email = data_str['email']
    Id.mobile_number = data_str['mobile_number']

    db.session.commit()

    student_schema = StudentSchema()
    updated_data = student_schema.dump(Id)

    return jsonify({"message": "Student updated successfully", "updated_data": updated_data}), 200

@app.route("/delete_data/<int:id>", methods=['DELETE'])
def delete_student(id):
    data = Student.query.get(id)

    if data is None:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(data)
    db.session.commit()

    return jsonify({"message": "Student deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
