""" Celery initialization """
from celery import Celery
from cloudcourseproject.src.config import config

celery = Celery(
    "cloudcourseproject",
    broker=config["CELERY_BROKER_URL"],
    backend=config["CELERY_RESULT_BACKEND"],
    include=[
        "cloudcourseproject.src.authorization.tasks",
        "cloudcourseproject.src.article.tasks"
    ]
)

celery.conf.update(config)
