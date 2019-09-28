from app import create_app, db
from app.models import User, Movie, Interaction, Discount


app = create_app()


# Create shell context for debugging with `flask shell`
@app.shell_context_processor
def make_shell_context():
    return {'Discount': Discount, 'User': User, 'Movie': Movie, 'Interaction': Interaction, 'db': db}
