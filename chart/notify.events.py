#!/usr/bin/env python
# coding: utf-8

import sys
import json
import requests
from urllib.parse import urlencode


class Zabbix:

    _host = None
    _id = 1
    _auth = None
    _version = None

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

    def version(self):
        self._version = self._api_request('apiinfo.version', [])
        self._version = self._version.split('.')

        return self._version

    def login(self, user, password):
        self._auth = None

        self._auth = self._api_request('user.login', {
            'user': user,
            'password': password,
        })

    def trigger_get(self, id):
        if not self._auth:
            raise Exception('Authorize required!')

        triggers = self._api_request('trigger.get', {
            'triggerids': id,
            'output': [
                'priority',
                'status',
            ],
            'limit': 1,
        })

        return triggers[0]

    def item_get_ids(self, trigger_id):
        if not self._auth:
            raise Exception('Authorize required!')

        items = self._api_request('item.get', {
            'triggerids': trigger_id,
            'output': [
                'itemid',
            ],
        })

        item_ids = []

        for i in range(0, len(items)):
            item_ids.append(items[i]['itemid'])

        return item_ids

    def graph_get_ids(self, item_ids):
        if not self._auth:
            raise Exception('Authorize required!')

        graphs = self._api_request('graph.get', {
            'itemids': item_ids,
            'output': [
                'graphid'
            ]
        })

        graph_ids = []

        for i in range(0, len(graphs)):
            graph_ids.append(graphs[i]['graphid'])

        return graph_ids

    def graph_render(self, graph_id, period, width, height) -> str:
        if not self._auth:
            raise Exception('Authorize required!')

        query = {
            'graphid': graph_id,
            'width': width,
            'height': height,
        }

        if self._version[0] == '3':
            query.update({
                'profileIdx': 'web.screens',
                'period': period,
            })
        elif self._version[0] == '4':
            query.update({
                'profileIdx': 'web.graphs.filter',
                'from': 'now-{0}'.format(period),
                'to': 'now',
            })

        response = requests.get(self._host + 'chart2.php?' + urlencode(query), cookies={'zbx_sessionid': self._auth})

        if response.status_code != 200:
            raise Exception('Can\'t get chart image!')

        return response.content

if __name__ == '__main__':

    args = sys.argv

    to = args[1]
    subject = args[2]
    message = args[3]
    trigger_id = args[4]

    json_file = open('notify.events.json')
    config = json.load(json_file)

    zabbix = Zabbix(config['zabbix']['host'])

    version = zabbix.version()

    if version[0] not in ('3', '4'):
        raise Exception('Unsupperted zabbix version!')

    zabbix.login(config['zabbix']['user'], config['zabbix']['password'])

    trigger = zabbix.trigger_get(trigger_id)
    item_ids = zabbix.item_get_ids(trigger_id)
    graph_ids = zabbix.graph_get_ids(item_ids)

    files = {}

    if len(graph_ids) > 0:
        for i in range(0, len(graph_ids)):
            try:
                image = zabbix.graph_render(graph_ids[i], config['chart']['period'], config['chart']['width'], config['chart']['height'])

                files.update({
                    'chart[{0}]'.format(i): ('chart.png', image, 'image/png'),
                })
            except Exception as e:
                print('Can\'t create chart: ' + str(e))
                break

    severity = trigger['priority']

    if trigger['status'] == 0:
        status = 'PROBLEM'
    else:
        status = 'OK'

    data = {
        'subject': subject,
        'message': message,
        'severity': severity,
        'status': status,
    }

    res = requests.post('https://notify.events/api/v1/channel/source/{0}/execute'.format(to), data=data, files=files)

    if res.status_code != 200:
        raise Exception('Can\'t send notification')
