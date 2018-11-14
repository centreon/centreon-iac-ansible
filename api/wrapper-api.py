#!/usr/bin/env python
#
# wrapper.py <resource> <action>
#
from sys import exit, argv
import json
import requests
import yaml

URI = 'http://127.0.0.1:10080/centreon'
API = URI + '/api/index.php?action=action&object=centreon_clapi'
AUTH = URI + '/api/index.php?action=authenticate'

resource = argv[1]
action = argv[2]

mapobjects = {
    'aclaction': {
        'index': 'name',
        'required': ['name', 'description']
    },
    'aclgroup': {
        'index': 'name',
        'required': ['name', 'alias', 'activate']
    },
    'aclmenu': {
        'index': 'name',
        'required': ['name', 'alias']
    },
    'aclresource': {
        'index': 'name',
        'required': ['name', 'alias']
    },
    'centbrokercfg': {
        'index': 'name',
        'required': ['name', 'brokercfg']
    },
    'command': {
        'index': 'name',
        'required': ['name', 'type', 'cmdline']
    },
    'contacts': {
        'index': 'name',
        'required': [
            'name', 'alias', 'email', 'password', 'admin',
            'gui', 'language', 'auth_type'
        ]
    },
    'cg': {
        'index': 'name',
        'required': ['name', 'alias']
    },
    'dep': {
        'index': 'name',
        'required': ['name', 'description', 'type', 'parent']
    },
    'downtime': {
        'index': 'name',
        'required': ['name', 'description']
    },
    'enginecfg': {
        'index': 'name',
        'required': ['name', 'instance', 'description']
    },
    'host': {
        'index': 'name',
        'required': [
            'name', 'alias', 'address', 'template', 'instance',
            'hostgroup'
        ],
        'attrs': ['geo_coords', '2d_coords', '3d_coords', 'action_ur',
                  'activate', 'active_checks_enabled', 'address', 'alias',
                  'check_command', 'check_command_arguments', 'check_interval',
                  'check_freshness', 'check_period',
                  'contact_additive_inheritance', 'cg_additive_inheritance',
                  'event_handler', 'event_handler_arguments',
                  'event_handler_enabled', 'first_notification_delay',
                  'flap_detection_enabled', 'flap_detection_options',
                  'host_high_flap_threshold', 'host_low_flap_threshold',
                  'icon_image', 'icon_image_alt',
                  'max_check_attempts', 'notes', 'notes_url',
                  'notifications_enabled', 'notification_interval',
                  'notification_options', 'notification_period',
                  'recovery_notification_delay', 'obsess_over_host',
                  'passive_checks_enabled', 'process_perf_data',
                  'retain_nonstatus_information', 'retain_status_information',
                  'retry_check_interval', 'snmp_community', 'snmp_version',
                  'stalking_options', 'statusmap_image',
                  'host_notification_options', 'timezone']
    },
    'hg': {
        'index': 'name',
        'required': ['name', 'alias']
    },
    'instance': {
        'index': 'name',
        'required': ['name', 'address', 'ssh']
    },
    'ldap': {
        'index': 'name',
        'required': ['name', 'description']
    },
    'resourcecfg': {
        'index': 'name',
        'required': ['name', 'value', 'instance', 'description']
    },
    'stpl': {
        'index': 'description',
        'required': ['description', 'alias', 'template']
    },
    'service': {
        'index': ['host name', 'description'],
        'required': ['host name', 'description', 'template'],
        'attrs': ['template', 'is_volatile',
                  'check_period', 'check_command', 'check_command_arguments',
                  'max_check_attempts', 'normal_check_interval',
                  'retry_check_interval', 'active_checks_enabled',
                  'passive_checks_enabled', 'notifications_enabled',
                  'contact_additive_inheritance', 'cg_additive_inheritance',
                  'notification_interval', 'notification_period',
                  'notification_options', 'first_notification_delay',
                  'recovery_notification_delay', 'obsess_over_service',
                  'check_freshness', 'freshness_threshold',
                  'event_handler_enabled', 'flap_detection_enabled',
                  'retain_status_information', 'retain_nonstatus_information',
                  'event_handler', 'event_handler_arguments', 'notes',
                  'notes_url', 'action_url', 'icon_image', 'icon_image_alt',
                  'comment', 'service_notification_options']
    },
    'sg': {
        'index': 'name',
        'required': ['name', 'alias']
    },
    'sc': {
        'index': 'name',
        'required': ['name', 'description']
    },
    'tp': {
        'index': 'name',
        'required': ['name', 'alias']
    },
    'trap': {
        'index': 'name',
        'required': ['name', 'oid']
    },
    'vendor': {
        'index': 'name',
        'required': ['name', 'alias']
    }
}

gettoken = requests.post(AUTH, data={
    'username': 'admin',
    'password': 'p4ssw0rd'
})

if gettoken.status_code == 200:
    token = json.loads(gettoken.text)
    header = {
        'centreon-auth-token': token['authToken']
    }
else:
    print('Error in get the token')
    exit(1)


def do_request(name, action, data=None):
    try:
        if data:
            bodyData = {
                'action': action,
                'object': name,
                'values': data
            }
        else:
            bodyData = {
                'action': action,
                'object': name
            }
        req = requests.post(API, headers=header, json=bodyData)
        if req.status_code == 200:
            return json.loads(req.text)
        else:
            print('Error in get objects list')
            exit(1)
    except ValueError:
        print('Error in try post data')
        exit(1)


with open('config.yml') as _f:
    obj = yaml.load(_f.read())  # Parse yaml object
for name in obj.keys():

    # Verify if exists object
    for item in obj[name]:
        listobjects = do_request(name, 'show')['result']
        if not isinstance(mapobjects[name]['index'], list):
            if item[mapobjects[name]['index']] not in [
                _o[mapobjects[name]['index']] for _o in listobjects
            ]:
                # not exist, add object
                if item['state'] != 'absent':
                    addObject = do_request(
                        name,
                        'add',
                        ';'.join(
                            [item[i] for i in mapobjects[name]['required']]
                        )
                    )
                    if addObject:
                        print('New object %s added' % name)
            else:
                print(item)
                rstate = [i['activate'] for i in listobjects if (
                    i['name'] == item['name']
                )][0]
                if item['state'] == 'disabled' and rstate == '1':
                    # Disable object
                    # Necessary here get attribute value to test the active
                    # state of object (for now, confirm the status)
                    disable = do_request(
                        name,
                        'setparam',
                        '%s;%s;%s' % (
                            item[mapobjects[name]['index']],
                            'activate',
                            '0'
                        )
                    )
                    if disable:
                        print('Object %s was disabled' % name)
                elif item['state'] == 'absent':
                    # Remove object
                    delete = do_request(
                        name, 'del', item[mapobjects[name]['index']]
                    )
                    if delete:

                        print('Object %s deleted' % name)
        else:
            # make a list of tuples with values of index by pulled list
            values = []
            for s in listobjects:
                tup = tuple()
                for i in mapobjects[name]['index']:
                    tup = (*tup, s[i])
                values.append(tup)
            # Now make a tuple with actual value from provider
            actual = tuple()
            for i in mapobjects[name]['index']:
                actual = (*actual, item[i])
            # compare tuple with the list of tuples
            if actual not in values:
                # not exist, add object
                if item['state'] != 'absent':
                    addObject = do_request(
                        name,
                        'add',
                        ';'.join(
                            [item[i] for i in mapobjects[name]['required']]
                        )
                    )
                    if addObject:
                        print('New object %s added' % name)
            else:
                print(item)
                rstate = [i['activate'] for i in listobjects if (
                    i['name'] == item['name']
                )][0]
                if item['state'] == 'disabled' and rstate == '1':
                    # Disable object
                    disable = do_request(
                        name,
                        'setparam',
                        '%s;%s;%s' % (
                            ';'.join(actual),
                            'activate',
                            '0'
                        )
                    )
                    if disable:
                        print('Object %s->%s was disabled' % (
                            name, ';'.join(actual)
                        ))
                elif item['state'] == 'absent':
                    # Remove object
                    delete = do_request(name, 'del', ';'.join(actual))
                    if delete:
                        print('Object %s->%s deleted' % (
                            name, ';'.join(actual))
                        )

        # Now, test parameters and do action based on result
        if 'attrs' in mapobjects[name].keys() and item['state'] != 'absent':
            for attr in item.keys():
                if attr in mapobjects[name]['attrs']:
                    #
                    # Need a endpoint to get a actual list of attributes from
                    # object
                    # For now, always apply attributes
                    #
                    pushattr = do_request(
                        name,
                        'setparam',
                        '%s;%s;%s' % (
                            item[mapobjects[name]['index']] if (
                                not isinstance(
                                    mapobjects[name]['index'], list
                                )
                            ) else ';'.join(actual),
                            attr,
                            item[attr]
                        )
                    )
                    if pushattr:
                        print('Set attribute *%s* to value "%s" in %s object %s' % (
                                attr,
                                item[attr],
                                name,
                                item[mapobjects[name]['index']] if (
                                    not isinstance(
                                        mapobjects[name]['index'], list
                                    )
                                ) else ';'.join(actual)
                            )
                        )
