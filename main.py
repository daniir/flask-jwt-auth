from app import create_app
from config.config import port

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=port)