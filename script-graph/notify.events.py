#!/usr/bin/env python
# coding: utf-8

import sys
import json
import requests
from urllib.parse import urlencode

import config


class Zabbix:

    _host = None
    _id = 1
    _auth = None

    def __init__(self, host):
        self._host = host

    def _api_request(self, method: str, params):
        headers = {
            'Content-Type': 'application/json-rpc',
        }

        data = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': self._id,
            'auth': self._auth,
        }

        self._id += 1

        response = requests.post(self._host + 'api_jsonrpc.php', data=json.dumps(data), headers=headers)

        if response.status_code != 200:
            raise Exception('Api request error!')

        response_data = json.loads(response.content)

        if 'error' in response_data.keys():
            raise Exception(response_data['error']['data'])

        return response_data['result']

    def login(self, user, password):
        self._auth = None

        self._auth = self._api_request('user.login', {
            'user': user,
            'password': password,
        })

    def graph(self, name, itemids, period, width, height) -> str:
        if not self._auth:
            raise Exception('Authorize required!')

        colors = [
            'f44336',
            '9c27b0',
            '3f51b5',
            '03a9f4',
            '009688',
            '8bc34a',
            'ffeb3b',
            'ff9800',
            '795548',
        ]

        query = {
            'from': 'now-{0}'.format(period),
            'to': 'now',
            'period': period,
            'name': name,
            'width': width,
            'height': height,
            'graphtype': 0,
            'legend': 1,
        }

        for i in range(0, len(itemids)):
            if itemids[i] == "":
                break

            query.update({
                'items[{0}][itemid]'.format(i): itemids[i],
                'items[{0}][sortorder]'.format(i): 0,
                'items[{0}][drawtype]'.format(i): 2,
                'items[{0}][color]'.format(i): colors[i],
            })

        response = requests.get(self._host + 'chart3.php?' + urlencode(query), cookies={'zbx_sessionid': self._auth})

        if response.status_code != 200:
            raise Exception('Can\'t get graph image!')

        return response.content


if __name__ == '__main__':

    token = sys.argv[1]
    subject = sys.argv[2]
    message = sys.argv[3]
    severity = sys.argv[4]
    itemids = sys.argv[5]
    itemids = itemids.split(',')

    zabbix = Zabbix(config.zabbix_host)

    files = {}

    try:
        zabbix.login(config.zabbix_user, config.zabbix_password)

        image = zabbix.graph(subject, itemids, config.graph_period, config.graph_width, config.graph_height)

        files.update({
            'graph': ('graph.png', image, 'image/png'),
        })
    except Exception as e:
        print('Can\'t create graph: ' + str(e))

    query = {
        'subject': subject,
        'message': message,
        'severity': severity,
    }

    res = requests.post('https://dev.notify.events/api/v1/channel/source/{0}/execute?{1}'.format(token, urlencode(query)), files=files)

    if res.status_code != 200:
        raise Exception('Can\'t send notification')
