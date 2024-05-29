#!/bin/bash
# run the main.py again, as werkzeug user
su werkzeug -c "cd /home/werkzeug/vinuni_cloud && flask run"
