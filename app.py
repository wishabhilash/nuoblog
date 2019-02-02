from flask import Flask
import pdb

from nuoblog.functions.add_content import main as add_content

app = Flask(__name__)

app.add_url_rule("/add_content", 'add_content', add_content.main, methods=['POST'])