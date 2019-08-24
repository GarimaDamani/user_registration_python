from flask import Flask
from .config import application as ap

app = Flask(__name__, template_folder=ap.template_location)
