from app import create_app, manager
import os
app = create_app
if __name__ == '__main__':
    manager.run(app)
    app.run()