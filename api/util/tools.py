#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


def format_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%y/%m/%d") if timestamp else ''