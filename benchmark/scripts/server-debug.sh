#!/bin/bash

export FLASK_APP=analysis.py
export FLASK_ENV=development

flask run --port 8085
