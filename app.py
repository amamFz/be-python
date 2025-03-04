from app import create_app  # Ambil fungsi create_app dari __init__.py

app = create_app()  # Buat instance Flask menggunakan create_app()

if __name__ == "__main__":
    app.run(debug=True)
