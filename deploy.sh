#!/bin/bash
screen -dmS news gunicorn -w 1 -b 0.0.0.0:5000 --pythonpath '/var/www/news' app:app
