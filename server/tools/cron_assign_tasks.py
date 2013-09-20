# coding: utf8
import os
os.sys.path.append(os.getcwd())

from models import UpdateTask


if __name__ == '__main__'():
    '''
    Cronjob 2分钟跑一次:
    '''
    if UpdateTask.is_no_tasks():
        UpdateTask.assign_tasks()
