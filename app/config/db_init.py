from app import app


def initialize_database():
    if not app.debug:
        confirm_prod = input("You are in production mode. Are you sure you want to initialize the database? (yes/no): ")
        if confirm_prod.lower() != 'yes':
            print("Database initialization aborted.")
            return

    print("Initializing database...")
    from app import db
    from app.models.role import Role
    from app.models.user import User
    from app.models.user_roles import UserRoles
    import bcrypt

    if not Role.query.filter_by(name="ADMIN").first():
        admin_role = Role(name="ADMIN")
        db.session.add(admin_role)
        db.session.commit()

    if not Role.query.filter_by(name="USER").first():
        user_role = Role(name="USER")
        db.session.add(user_role)
        db.session.commit()

    if not User.query.filter_by(username="admin").first():
        salt = bcrypt.gensalt()
        admin_user = User(
            username="admin",
            password=bcrypt.hashpw("Admin1234=!".encode('utf8'), salt),
            firstname="Admin",
            lastname="Admin"
        )
        admin_user_role = UserRoles(user=admin_user, role=Role.query.filter_by(name="ADMIN").one())
        admin_user.user_roles.append(admin_user_role)
        db.session.add(admin_user)

        user_user_role = UserRoles(user=admin_user, role=Role.query.filter_by(name="USER").one())
        admin_user.user_roles.append(user_user_role)
        db.session.add(admin_user)
        db.session.commit()