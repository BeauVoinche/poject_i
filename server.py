from flask_app import app
# ! REMEMBER TO ALWAYS IMPORT THE CONTROLLERS
from flask_app.controllers import user_controller



if __name__=='__main__':
    app.run(debug=True)