class User(db.Model):
    # ...existing code...
    country = db.Column(db.String(64))
    governorate = db.Column(db.String(64))
    city = db.Column(db.String(64))
    education_level = db.Column(db.String(32))
    university = db.Column(db.String(128))
    # ...existing code...