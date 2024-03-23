#!/bin/bash

# команды для миграций

gunicorn --bind=0.0.0.0:8000 config.wsgi