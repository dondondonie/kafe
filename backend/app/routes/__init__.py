from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
menu_bp = Blueprint('menu', __name__, url_prefix='/api/menu')
inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')
orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')
reservations_bp = Blueprint('reservations', __name__, url_prefix='/api/reservations')
customers_bp = Blueprint('customers', __name__, url_prefix='/api/customers')
analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')
employees_bp = Blueprint('employees', __name__, url_prefix='/api/employees')

from .auth import auth_bp
from .menu import menu_bp
from .inventory import inventory_bp
from .orders import orders_bp
from .reservations import reservations_bp
from .customers import customers_bp
from .analytics import analytics_bp
from .employees import employees_bp
