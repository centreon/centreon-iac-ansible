

Itens necessary to use:


Control Machine:

- Ansible tools
- Access SSH to remote hosts

Install last version of Ansible

https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-the-control-machine


Centreon Playbook Set
=====================

Tasks
-----

- Common
  Common tasks to provide resources to use Centreon on the machine (requeri by others tasks)
- MariaDB Server
  Database server to storage data from Centreon
- Centreon Web
  Complete install of Centreon with Web GUI interface and tools
- Centreon Configuration
  A set of tasks to configuration objects on the Centreon using clapi features
- Centreon Poller
  Task to install a Centreon Poller host

Installation
------------

Using GIT:

  cd ~/work-dir
  git clone https://github.com/centreon/centreon-ansible.git
  git checkout version_18_10

Using Ansible Galaxy

  Comming soon

Variables to use with Playbook:

Task: mariadb-server

	mysql_root_password - (string) Password to use with user root

Task: centreon-web

	php_timezone - (string)
		Timezone to configuration of PHP
		http://php.net/manual/en/timezones.php
	mysql_hostname - (string) Hostname or IP to use for connection with Mysql database
    mysql_port - (string) Port number to use for connection with Mysql database
    mysql_root_password - (string) Password used by user root (you can use variable from mariadb-server task)
    mysql_centreon_db - (string) Database name used by Centreon
    mysql_centstorage_db - (string) Database name used by Centreon Storage
    mysql_centreon_username - (string) Username used by Centreon
    mysql_centreon_password - (string) Password user used by Centreon
    centreon_admin_password - (string) Password used by user admin (main administrator user)
    plugin_pack - (array)
		A array of plugins pack to install
		Valid values:
		- base-generic
		- Centreon
		- Centreon DB
		- Centreon Poller
		- Cisco standard
		- Linux SNMP
		- MySQL DB
		- Printer standard
		- UPS Standard
		- Windows SNMP
		- DHCP Server
		- DNS Service
		- FTP Server
		- HTTP Server
		- LDAP Server
		- 3com Network
		- AIX SNMP
		- AKCP Sensor
		- Alcatel OXE
		- Apache Server

Default values:
```
  php_timezone: "Europe/Paris"
  mysql_centreon_hostname: "localhost"
  mysql_centstorage_hostname: "localhost"
  mysql_port: "3306"
  mysql_root_password: "p4ssw0rd"
  mysql_centreon_username: "centreon"
  mysql_centreon_password: "p4ssw0rd"
  mysql_centreon_db: "centreon"
  mysql_centstorage_db: "centreon_storage"
  centreon_admin_password: "p4ssw0rd"
```

Install and configure a new Host with Centreon

You need a installation of CentOS 7 with SSH server enabled

[Using Vagrant images to prepare Centreon](vagrant.md)

on the control machine, export the ssh key to new host:

```
ssh-copy-id root@[remote-ip-or-hostname]
```

Create a new file of hosts with the configuration to connect in the remote host, example:

```
vi hosts.deploy
[centreon-server]
centreon-web ansible_port=22 ansible_host=[remote-ip-or-hostname]
```

Create a new file with format YAML to deploy components for installation of Centreon Web

```
vi centreon-deploy.yml
---
- name: Centreon-Web
  hosts: centreon-server
  remote_user: root

  roles:
    - "roles/common"
    - role: "roles/mariadb-server"
      mysql_root_password: "p4ssw0rd"

    - role: "roles/centreon-web"
      php_timezone: "Europe/Paris"
      mysql_hostname: "localhost"
      mysql_port: "3306"
      mysql_root_password: "p4ssw0rd"
      mysql_centreon_db: "centreon"
      mysql_centstorage_db: "centreon_storage"
      mysql_centreon_username: "centreon"
      mysql_centreon_password: "p4ssw0rd"
      centreon_admin_password: "p4ssw0rd"
      plugin_pack:
        - "base-generic"
        - "Linux SNMP"
```

Now, you can apply the deploy in remote server, use these command:

```
ansible-playbook -i hosts.deploy centreon-deploy.yml
```

[![asciicast](https://asciinema.org/a/gAW0W68xd7DTa0hiGeO0ZtLPQ.svg)](https://asciinema.org/a/gAW0W68xd7DTa0hiGeO0ZtLPQ)


Deploy a host to monitoring as a example:

- CentOS 7
- SNMP
- Nginx

Install playbook's necessary to apply:

```
ansible-galaxy install geerlingguy.nginx
ansible-galaxy install scathatheworm.net-snmp
```


Prepare a file to deploy components by Ansible:

```
---
- name: Nginx Server
  hosts: webserver
  remote_user: root
  roles:
    - role: geerlingguy.nginx
    - role: scathatheworm.net-snmp
      snmpd_community_acl:
      - type: rocommunity
        community_name: public

- name: Add monitor to Centreon
  hosts: centreon-web
  remote_user: root
  roles:
  - role: "roles/centreon-config"
    centreon_admin_password: "p4ssw0rd"
    host_list:
      - {
        'host': 'nginx_webserver',
        'alias': 'Web Server tests',
        'address': '192.168.150.100',
        'template': 'generic-active-host-custom|OS-Linux-SNMP-custom',
        'instance': 'central',
        'snmp_community': ' public',
        'snmp_version': '1',
        'notes': ' this is a example of notes',
        'state': 'enabled' # enabled, disabled, absent
      }
    service_list:
      - {
        'name': 'port_80',
        'host': 'nginx_webserver',
        'template': 'generic-active-service',
        'check_command': 'check_centreon_dummy',
        'notes': 'other example of notes',
        'state': 'enabled' # enabled, disabled, absent
        }
```

Now, you can apply the deploy in remote server, use these command:

```
ansible-playbook -i hosts.deploy nginx-deploy.yml
```

[![asciicast](https://asciinema.org/a/2Y7fLQhJKCn6tqdk32ByORsGj.svg)](https://asciinema.org/a/2Y7fLQhJKCn6tqdk32ByORsGj)
