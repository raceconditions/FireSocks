import serial
import time
from flask import render_template, Blueprint, redirect, url_for
from services.igniter import ignite

ignite_api = Blueprint('ignite_api', __name__, template_folder='templates')

@ignite_api.route('/ignite/<channel>', methods=['GET'])
def ignite_channel(channel):
    ignite(channel)
    return redirect(url_for("home_api.control"))
