#! /bin/bash
pip install -r requirements.txt
flask db upgrade &&
waitress-serve --call --port=$PORT 'app:create_app'