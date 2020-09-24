import settings

import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_restful import Api

from jobs.job_notify_on_moh_update import job_notify_on_moh_update
from resources.publish_resource import PublishResource
from resources.notify_resource import NotifyResource

scheduler = BackgroundScheduler()

app = Flask(__name__)
api = Api(app)

api.add_resource(PublishResource, '/v1/publish')
api.add_resource(NotifyResource, '/v1/notify')

if __name__ == '__main__':
    job_notify_on_moh_update()
    scheduler.add_job(job_notify_on_moh_update, 'interval', seconds=int(os.getenv('JOB_INTERVAL_IN_SECONDS')))
    scheduler.start()
    app.run(port=6000, debug=False)
