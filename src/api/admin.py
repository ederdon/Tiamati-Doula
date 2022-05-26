  
import os
from flask_admin import Admin
from .models import db, Users, UserData, UserRol, ServiceTypes, Service, Documents, ServiceRols
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='ADMIN', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Users, db.session)),
    admin.add_view(ModelView(UserData, db.session))
    admin.add_view(ModelView(UserRol, db.session))
    admin.add_view(ModelView(ServiceTypes, db.session))
    admin.add_view(ModelView(Service, db.session))
    admin.add_view(ModelView(Documents, db.session))
    admin.add_view(ModelView(ServiceRols, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))