from flask_marshmallow import Marshmallow

ma = Marshmallow()

class StudentSchema(ma.Schema):
    class Meta:
        fields =['name', 'age', 'email', 'mobile_number']
