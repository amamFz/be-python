from app import app, db
from flask import request, jsonify
from models import Friend


# Dapatkan semua data teman
@app.route("/api/friends", methods=["GET"])
def get_friends():
    friends = Friend.query.all()
    if not friends:
        return (
            jsonify({"message": "No friends found!"}),
            404,
        )  # Handle jika tidak ada data

    try:
        result = [friend.to_json() for friend in friends]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Menambahkan data teman
@app.route("/api/friends", methods=["POST"])
def add_friend():
    try:
        data = request.json

        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Field '{field}' is required"}), 400

        name = data.get("name")
        role = data.get("role")
        description = data.get("description")
        gender = data.get("gender")

        # Ambil gambar avatar
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_friend = Friend(
            name=name,
            role=role,
            description=description,
            gender=gender,
            img_url=img_url,
        )

        db.session.add(new_friend)

        db.session.commit()

        return jsonify({"message": "Teman berhasil ditambahkan"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Menghapus data teman
@app.route("/api/friends/<int:id>", methods=["DELETE"])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)
        if not friend:
            return jsonify({"message": "Friend not found!"}), 404

        db.session.delete(friend)
        db.session.commit()

        return jsonify({"message": "Friend deleted!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Mengupdate data teman
@app.route("/api/friends/<int:id>", methods=["PUT"])
def update_friend(id):
    try:
        friend = Friend.query.get(id)
        if not friend:
            return jsonify({"message": "Friend not found!"}), 404

        data = request.json

        friend.name = data.get("name", friend.name)
        friend.role = data.get("role", friend.role)
        friend.description = data.get("description", friend.description)
        friend.gender = data.get("gender", friend.gender)

        if friend.gender == "male":
            friend.img_url = (
                f"https://avatar.iran.liara.run/public/boy?username={friend.name}"
            )
        elif friend.gender == "female":
            friend.img_url = (
                f"https://avatar.iran.liara.run/public/girl?username={friend.name}"
            )
        else:
            friend.img_url = None

        db.session.commit()
        return jsonify({"message": "Friend updated!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
