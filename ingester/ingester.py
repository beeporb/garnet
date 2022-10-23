from garnet.celery_config import app
from garnet import preflight
from garnet import tasks
from garnet import tracking

preflight.create_working_dirs()
preflight.load_model()
tracking.wipe_tracking()
