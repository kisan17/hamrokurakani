from hamrokurakani import create_app, socketio
from hamrokurakani.models import *

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message}


if __name__ == '__main__':
    app.jinja_env.cache = {}
    socketio.run(app, debug=True)
