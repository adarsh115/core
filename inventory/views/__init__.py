from .common import *
from .inventory_management_views import *
from .item_views import *
from .order_views import *
from .supplier_views import *
from .warehouse_views import *
from .scrapping_views import *
from .storage_media_views import *
from .reports import *
from .item import *
from background_task.models import Task
from inventory.schedules import run_inventory_service

try:
    if not Task.objects.filter(task_name="inventory.schedules.run_inventory_service").exists():
        run_inventory_service(repeat=Task.DAILY)
except:
    pass
