from app import create_app

# WSGI entry point
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)