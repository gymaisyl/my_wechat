#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""
import os
import time
import subprocess

from config import mysql_account, mysql_passwd, BASE_DIR

database_name = "mysql"


class MigratePatch(object):
    """
    The patch of the migration function, in order to solve the migration problem caused by various abnormalities during
    the upgrade migration or other migration process, the version file does not correspond to the problem, or the
    migration file is wrong.
     The program will delete the alembic_version table in the database and clean up all the migration files in the
     flask-migrate migration path, and then re-execute the migration steps
    """

    def __init__(self):
        pass

    def __del__(self):
        """
        :return:
        """
        pass

    @staticmethod
    def cmd():
        cmd_list = [
            "python3 " + BASE_DIR + "/migrate_run.py db init -d /data/database/orig/migrations",
            "python3 " + BASE_DIR + "/migrate_run.py db migrate -d /data/database/orig/migrations  -m 'version'",
            "python3 " + BASE_DIR + "/migrate_run.py db upgrade -d /data/database/orig/migrations"
        ]
        return cmd_list

    @staticmethod
    def create():
        """
        Delete the migration version of the table
        :return:
        """

        with open("/root/create_db.sql", "w", encoding="utf-8") as f:
            f.write("create database if not exists reactinfo charset='utf8';\n")
        time.sleep(2)
        os.system("mysql -u%s -p%s < /root/create_db.sql" % (mysql_account, mysql_passwd))

    @staticmethod
    def run():
        os.system("rm /data/database/orig/migrations -r")
        MigratePatch.create()
        for cmd in MigratePatch.cmd():
            p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
            print(p.communicate()[0].decode("utf8"))
            p.wait()


MigratePatch.run()
