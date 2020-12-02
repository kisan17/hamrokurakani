from hamrokurakani import create_app, socketio
from hamrokurakani.models import *
import subprocess
import sys

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message}

if __name__ == '__main__':
    socketio.run(app, debug=True)
