"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Users, UserData, UserRol, ServiceType, Service, Document, ServiceRols, ServiceDocuments, ServiceToService, ServiceHired, UserFaq, BusinessFaq, Appointment, CalendarAvailability
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import cloudinary
import cloudinary.uploader

api = Blueprint('api', __name__)  

@api.route('/protected', methods=['GET'])
@jwt_required()
def private():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if user:
        return jsonify({"logged": True}), 200
    else:
        return jsonify({"logged": False}), 400

@api.route('/signup', methods=['POST'])
def save_signup_user():
    body_email = request.json.get("email")
    body_password = request.json.get("password")
    body_rol = request.json.get("rol")
    if body_email and body_password:
        if Users.query.filter_by(email = body_email).first() == None:
            user_created = Users(email = body_email, password = body_password, rol = body_rol)
            db.session.add(user_created)
            db.session.commit()
            access_token = create_access_token(identity=user_created.id)
            return jsonify({"logged":True, "token": access_token, "msg": "Usuario creado correctamente", "User": user_created.serialize()}), 200    
        else: return jsonify({"msg": "Error, el email ya existe como usuaria"}), 400   
    else: return jsonify({"msg": "Error, comprueba email y contraseña"}), 400       
     

@api.route('/form', methods=['PUT']) 
@jwt_required()
def save_or_update_user_form():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    body_name = request.json.get("name")
    body_pregnancy_weeks = request.json.get("pregnancy_weeks")
    body_aproximate_birth_date = request.json.get("aproximate_birth_date")
    body_children_number = request.json.get("children_number")
    body_caesarean_sections_number = request.json.get("caesarean_sections_number")
    body_companion = request.json.get("companion")
    body_city = request.json.get("city")
    body_birth_place = request.json.get("birth_place")
    body_current_hospital = request.json.get("current_hospital")
    if current_user_id != None:
        current_user_data = UserData.query.filter_by(user_id = current_user_id).first()
        if current_user_data == None:
            user_created = UserData(user_id = current_user_id, name = body_name, pregnancy_weeks = body_pregnancy_weeks, aproximate_birth_date = body_aproximate_birth_date, children_number = body_children_number, caesarean_sections_number =  body_caesarean_sections_number,  companion = body_companion, city = body_city,  birth_place = body_birth_place, current_hospital = body_current_hospital)
            db.session.add(user_created)
            db.session.commit()
            return jsonify({"msg": "Datos guardados correctamente"}), 200    
        else: 
            current_user_data.name = body_name 
            current_user_data.pregnancy_weeks = body_pregnancy_weeks 
            current_user_data.aproximate_birth_date = body_aproximate_birth_date 
            current_user_data.children_number = body_children_number
            current_user_data.caesarean_sections_number = body_caesarean_sections_number 
            current_user_data.companion = body_companion 
            current_user_data.city = body_city
            current_user_data.birth_place = body_birth_place 
            current_user_data.current_hospital = body_current_hospital
            db.session.commit()
            return jsonify({'msg': "Datos modificados correctamente"}), 200 

    else: return jsonify({"msg": "Error, no se han podido guardar los datos"}), 400      

@api.route('/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    users_serialized = list(map(lambda item: item.serialize(), users)) 
    return jsonify({"response": users_serialized}), 200      


@api.route('/users_data', methods=['GET'])
def get_all_users_data():
    users_data = UserData.query.all()
    users_data_serialized = list(map(lambda item: item.serialize(), users_data)) 
    return jsonify({"response": users_data_serialized}), 200    

@api.route('/profile', methods=['PUT'])
@jwt_required()
def change_user_email_or_password():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    body_email = request.json.get("email")
    body_password = request.json.get("password")
    user_change = Users.query.filter_by(id = current_user_id).first()
    if user_change != None:
        user_change.email = body_email
        db.session.commit()
        return jsonify({"msg": "Datos guardados correctamente"}), 200   
    else: return jsonify({"msg": "Error, no se han podido guardar los datos"}), 400, 401 

@api.route('/login', methods=['POST'])
def login():
    email = request.json.get("Email", None)
    password = request.json.get("Password", None)
    user = Users.query.filter_by(email=email).filter_by(is_active=True).first()
    if user is None:
        return jsonify({"msg": "Incorrect email"}), 400
    user = Users.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg": "Incorrect password"}), 400
    access_token = create_access_token(identity=user.id)
    return jsonify({"logged":True, "token": access_token, "msg": "User logged in correctly", "User": user.serialize()}), 200

@api.route('/user_info', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    current_user_data = UserData.query.filter_by(user_id = current_user_id).first()
    if current_user_id and current_user_data == None:
        return jsonify({"info": user.serialize()}), 200
    elif current_user_id and current_user_data:     
        return jsonify({"info": user.serialize(), "data": current_user_data.serialize() }), 200
    else:
       return jsonify({"user_loggin_info": user.serialize(), "user_data": "No user data" }), 400  
      
@api.route('/deleteUser', methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    user.is_active = False
    db.session.commit()
    return jsonify({"msg": "User deleted, ok"}), 200     


@api.route('/upload', methods=['POST'])
def handle_upload():
    result = cloudinary.uploader.upload(request.files["document"])
    document_url = result["secure_url"]
    document_name = request.documentName["documentName"]

    return jsonify("document correctly upload"), 200

  
#services

@api.route('/services', methods=['GET'])
def services():
    service_response=[]
    services = Service.query.all()
    if services:
        services_serialized = list(map(lambda item: item.serialize(), services))
        for service in services_serialized:
            #get rols
            rols = ServiceRols.query.filter_by(service_id=service["id"])
            rols_serialized = list(map(lambda item: item.serialize(), rols))
            service_rols = []
            for rol in rols_serialized:
                rol_name = UserRol.query.get(rol["rol"])
                service_rols.append(rol_name)
            #get documents
            documents = ServiceDocuments.query.filter_by(service_id=service["id"])
            documents_serialized = list(map(lambda item: item.serialize(), documents))
            services_connected = ServiceToService.query.filter_by(service_id_father=service["id"])
            services_connected_serialized = list(map(lambda item: item.serialize(), services_connected))
            service_complete = {
                "service_id": service["id"],
                "service": service,
                "rols": rols_serialized,
                #"rols_names": service_rols,
                "documents": documents_serialized,
                "services_connected": services_connected_serialized,
            }
            service_response.append(service_complete)

        return jsonify({"response":service_response}), 200    
    else: 
        return jsonify({"No services in database"}), 400
      
 #FAQ
    
@api.route('/user_faq', methods=['GET'])
def get_user_faq():
    user_faq = UserFaq.query.all()
    user_faq_serialized = list(map(lambda user_faq: user_faq.serialize(), user_faq))
    return jsonify({"response": user_faq_serialized}), 200

@api.route('/business_faq', methods=['GET'])
def get_business_faq():
    business_faq = BusinessFaq.query.all()
    business_faq_serialized = list(map(lambda business_faq: business_faq.serialize(), business_faq))
    return jsonify({"response": business_faq_serialized}), 200


#CALENDAR

@api.route('/available_datetime', methods=['GET'])
@jwt_required()
def get_available_datetime():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    dates = CalendarAvailability.query.filter(CalendarAvailability.is_available == True)
    dates_serialized = list(map(lambda x: x.serialize(), dates))
    if user:
        return jsonify({"resp": dates_serialized}), 200
    else: return jsonify({"No se ha podido traer la información"}), 400

@api.route('/available_datetime/<body_date>', methods=['GET'])
@jwt_required()
def get_available_datetime_of_selected_date(body_date):
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    datetime = CalendarAvailability.query.filter(CalendarAvailability.date == body_date, CalendarAvailability.is_available == True)
    datetime_serialized = list(map(lambda x: x.serialize(), datetime))
    if user:
        return jsonify({"resp": datetime_serialized}), 200
    else: return jsonify({"No se ha podido traer la información"}), 400       

@api.route('/services_hired', methods=['GET'])
@jwt_required()
def get_services_hired_by_user():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    if user:
        user_service_hired = ServiceHired.query.filter_by(user_id = current_user_id)
        user_service_hired_serialized =  list(map(lambda x: x.serialize(), user_service_hired))
        services = Service.query.all()
        service_id_name = list(map(lambda x: {'id': x.id, 'service_name':x.name}, services))
        return jsonify({"service_hired_id": user_service_hired_serialized, "services_id_name": service_id_name}), 200
    else: return jsonify({"No se ha podido traer la información"}), 400

@api.route('/appointment', methods=['POST'])
@jwt_required()
def save_user_appointment():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    if user:
        body_date = request.json.get("date")
        body_time = request.json.get("time")
        body_service = request.json.get("service")
        appointment_saved = Appointment(user_id = current_user_id, date = body_date, time = body_time, service = body_service)
        db.session.add(appointment_saved)
        db.session.commit()
        dateTime = CalendarAvailability.query.filter_by(date = body_date).filter_by(time = body_time).first()
        dateTime.is_available = False
        db.session.commit()
        return jsonify({"msg": "Datos guardados correctamente"}), 200   
    else: return jsonify({"msg": "Error, no se han podido guardar los datos"}), 400

@api.route('/appointment', methods=['GET'])
@jwt_required()
def get_user_appointments():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    if user:
        user_appointment = Appointment.query.filter_by(user_id=current_user_id)
        user_appointment_serialized = list(map(lambda x: x.serialize(), user_appointment))
        return jsonify({"resp": user_appointment_serialized}), 200
    else: return jsonify({"No se ha podido traer la información"}), 400

@api.route('/appointment', methods=['PUT'])
@jwt_required()
def modify_user_appointment():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    old_date = request.json.get("old_date")
    old_time = request.json.get("old_time")
    body_date = request.json.get("date")
    body_time = request.json.get("time")
    body_service = request.json.get("service")
    appointment_id = request.json.get("id")
    appointment_change = Appointment.query.filter_by(user_id = current_user_id).filter_by(id = appointment_id).first()
    if appointment_change != None:
        appointment_change.date = body_date
        appointment_change.time = body_time
        appointment_change.service = body_service
        appointment_change.id = appointment_id
        new_dateTime = CalendarAvailability.query.filter_by(date = body_date).filter_by(time = body_time).first()
        new_dateTime.is_available = False
        old_dateTime = CalendarAvailability.query.filter_by(date = old_date).filter_by(time = old_time).first()
        old_dateTime.is_available = True
        db.session.commit()
        return jsonify({"msg": "Se han realizado los cambios"}), 200   
    else: return jsonify({"msg": "Error, no se han podido realizar los cambios"}), 400

@api.route('/appointment', methods=['DELETE'])
@jwt_required()
def delete_user_appointment():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)
    body_date = request.json.get("date")
    body_time = request.json.get("time")
    dateTime = CalendarAvailability.query.filter_by(date = body_date).filter_by(time = body_time).first()
    dateTime.is_available = True
    appointment_id = request.json.get("id")
    appointment = Appointment.query.filter_by(user_id = current_user_id).filter_by(id = appointment_id).delete()
    db.session.commit()
    return jsonify({"msg": "User deleted, ok"}), 200