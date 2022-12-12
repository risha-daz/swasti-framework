from flask import Blueprint

blueprint = Blueprint('my_blueprint', __name__)

from . import weekly
from . import daily
from . import audio