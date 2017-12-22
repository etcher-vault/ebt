
# -*- coding: utf-8 -*-
import os
import re
import sys
from datetime import datetime, timedelta


def __sort_by_date(string):
    return string[6:10] + string[3:5] + string[0:2] + string[11:13] + string[14:16]


def filter_list(path, format='%date', dayexp=None, store_last=None):
    """
    Format принимает текст и символы в формате Python regex, а так-же параметры в формате %parameter
    Список параметров:
    %date - заменяется на regex даты в формате "%d-%m-%Y_%H:%M" (обозначает текущую дату)
    %fdate - заменяется на regex даты в формате "%d-%m-%Y_%H:%M" (обозначает дату полного бэкапа)
    %% заменяется на % (используется как разделитель)

    dayexp - кол-во дней, по проществии которых необходимо удалять бэкап
    store_last - сколько необходимо хранить копий
    path - директория, в которой необходимо искать бэкапы
    Возвращает список бэкапов на удаление.
    Если dayexp и store_last не указанны, то возвращает список всех найденных бэкапов.
    """
    assert isinstance(path, str), '{1}.{2}: variable "{0}" has wrong type.'.format('path', __name__, sys._getframe().f_code.co_name)
    assert isinstance(format, str), '{1}.{2}: variable "{0}" has wrong type.'.format('format', __name__, sys._getframe().f_code.co_name)
    assert isinstance(dayexp, int) or (dayexp is None), '{1}.{2}: variable "{0}" has wrong type.'.format('dayexp', __name__, sys._getframe().f_code.co_name)
    assert isinstance(store_last, int) or (store_last is None), '{1}.{2}: variable "{0}" has wrong type.'.format('store_last', __name__, sys._getframe().f_code.co_name)
    formated_list = list()
    filtered_list = list()
    full_list = list()
    format = str(format).replace('%date', '([\d]{2}[-][\d]{2}[-][\d]{4}[_][\d]{2}[:][\d]{2})')
    format = str(format).replace('%fdate', '([\d]{2}[-][\d]{2}[-][\d]{4}[_][\d]{2}[:][\d]{2})')
    format = format.replace('%%', '[%%]')
    regex = '\A' + format + '\Z'
    comp_regex = re.compile(regex)
    dirs = os.listdir(path)
    for dir in dirs:
        if re.match(comp_regex, dir) is not None:
            formated_list.append(dir)
    formated_list.sort(reverse=True, key=__sort_by_date)

    if (dayexp is None) and (store_last is None):
        filtered_list = formated_list
    if dayexp is not None:
        dayexp_delta = timedelta(days=dayexp)
        for backup in formated_list:
            if datetime.strptime(backup.split('%')[0], '%d-%m-%Y_%H:%M') + dayexp_delta <= datetime.now():
                if backup not in filtered_list:
                    filtered_list.append(backup)
    if store_last is not None:
        for backup in formated_list[store_last:]:
            if backup not in filtered_list:
                filtered_list.append(backup)

    for element in filtered_list:
        full_list.append(path + '/' + element)
    return full_list


def last_backup(path, format='%date'):
    backup = filter_list(path=path, format=format)
    return backup[0]
