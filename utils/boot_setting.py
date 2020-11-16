#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: gym
@Software: PyCharm
"""

first_boot = "/data/flags/sys-first-boot"  # For the first version, the original database needs to be created
migrate_flag = "/data/flags/sys-migrate-db"  # Project upgrade, new database, data table

migration_path = '/data/database/orig/'  # Migration file storage path
migrations = '/data/database/orig/migrations'  # Migration file


def boot_run():
    """
    When booting up, all methods that need to be executed
    :return:
    """
    from utils.reboot_shell import migrate_init, data_init
    migrate_init()
    data_init()
