from app import create_app, db
from app.models import Discount


app = create_app()


# Create shell context for debugging with `flask shell`
@app.shell_context_processor
def make_shell_context():
    return {'Discount': Discount, 'db': db}
