import uuid
from datetime import datetime


def namefile():
    curr_time = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    return curr_time+"-"+str(uuid.uuid4())