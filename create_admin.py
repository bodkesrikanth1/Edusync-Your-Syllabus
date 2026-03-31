from werkzeug.security import generate_password_hash
from db import create_user

password_hash = generate_password_hash("admin")

create_user(
    full_name="Administrator",
    email="admin",
    password_hash=password_hash,
    role="admin"
)

print("✅ Admin user created: admin / admin")
