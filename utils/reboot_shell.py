#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
import os
import subprocess

from config import BASE_DIR
from utils.boot_setting import first_boot, migration_path, migrations, migrate_flag

migrate_path = BASE_DIR + "/migrate_patch.py"


def migrate_init():
    """
    migrate
    :return:
    """
    if os.path.exists(first_boot):
        if os.path.exists(migration_path):
            os.system("rm -r {folder}".format(folder=migration_path))
        # 迁移路径不存在,创建迁移路径
        os.mkdir(migration_path)
        os.system('bash {web_dir}/utils/delete_db.sh'.format(web_dir=BASE_DIR))
        os.system('bash {web_dir}/utils/create_db.sh'.format(web_dir=BASE_DIR))

        p = subprocess.Popen([
            "python3 {web_dir}/{manage_file} db init -d {migrations} --multidb;python3 {web_dir}/{manage_file} db migrate -d {migrations} -m 'version{version_num}';"
            "python3 {web_dir}/{manage_file} db upgrade -d {migrations}".format(web_dir=BASE_DIR,
                                                                                manage_file='migrate_run.py',
                                                                                migrations=migrations,
                                                                                version_num="1")],
            shell=True)
        p.wait()
        os.remove(first_boot)

    if os.path.exists(migrate_flag):
        p = subprocess.Popen(["python3 {migrate_path}".format(migrate_path=migrate_path)], shell=True,
                             stdout=subprocess.PIPE)
        p.wait()
        os.remove(migrate_flag)


def data_init():
    """
    Parameters that need to be initialized when starting up
    :return:
    """
    pass
