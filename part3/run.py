#!/usr/bin/python3
"""HBnB Part 3 entry point"""
from app import create_app
from config import DevelopmentConfig
app = create_app(DevelopmentConfig)
print("DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])
print("instance_path:", app.instance_path)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
