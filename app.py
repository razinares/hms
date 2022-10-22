# Imports the whole application from application folder
from application import app

if __name__ == '__main__':
    app.run(port=5000, debug=True)