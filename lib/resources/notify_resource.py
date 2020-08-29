from flask_restful import Resource

from jobs.job_notify_on_moh_update import job_notify_on_moh_update


class NotifyResource(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        job_notify_on_moh_update()

        return 200
