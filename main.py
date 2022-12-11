# Entry point of application
from website import create_app
# Website folder is a Python package due to __init__.py

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
