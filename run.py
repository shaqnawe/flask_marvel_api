from app import create_app
from app.blueprints.authentication.models import User
from app.blueprints.home.models import Character

app = create_app()

@app.shell_context_processor
def application_context():
    return {
        'User': User,
        'Character': Character
    }