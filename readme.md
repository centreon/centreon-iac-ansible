# Ansible Centreon

Table of Contents

- [Overview](#overview)
  - [Ansible Playbooks](#ansible-playbooks)
  - [Roles](#roles)
- [Versions](#versions)
  - [18.10.0](#18.10.0)
- [Requirements](#requirements)
  - [Operating systems](#operating-systems)
  - [Control Machine](#control-machine)
- [Installation](#installation)
- [Role Variables](#role-variables)
  - [Default Values](#default-values)
- [Examples](#examples)
  - [Installation](#simple-installation)
  - [Using Vagrant](docs/vagrant.md)
  - [Using AWS Amazon](docs/ec2.md)
  - [Using Google Cloud](docs/google-cloud.md)
  - [Using Microsoft Azure](#microsoft-azure)
  - [Using Digital Ocean](#digital-ocean)
  - [Using Vultr](#vultr)
- [Screencasts](#screencasts)
- [License](LICENSE)

## Overview

This playbook is a set of scripts and code that assist in automating the installation process and initial setup of the Centreon environment. With Ansible, you have the ability to customize basic system settings and remotely deploy the entire environment.

Everything is based on a single configuration file, containing basic database access and configuration information.

It is also possible to implement and automate the installation of Plugins of the [Plugins Pack](https://documentation.centreon.com/docs/centreon/en/latest/quick_start/basic_plugins.html)

### Ansible Playbooks

Playbooks express configurations, deployment, and orchestration in Ansible. The Playbook format is YAML. Each Playbook maps a group of hosts to a set of roles. Each role is represented by calls to Ansible tasks.

See more information: [Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)

### Roles

Centreon Web Playbook with MySQL Server

- Disable selinux
- Add Centreon Open Source repository
- Import keys from repository
- Install packages to Centreon poller
- Setup timezone to PHP
- Set custom option to Mysql in CentOS 7
- Generate SSH key (used by remote Centreon Poller)
- Start and enable services necessaries
- Setup firewall rules

Centreon Poller Playbook

- Disable selinux
- Add Centreon Open Source repository
- Import keys from repository
- Install packages to Centreon poller
- Set authorized previously created keys (copy from Centreon-Web)
- Enable and try start centengine service

## Versions

### 18.10.0

Version with synchronized functions for version 18.10.0 of the Centreon

## Requirements

### Operating systems

This role will work on the following operating systems:

- Red Hat / Centos

Control Machine:

- Ansible tools
- Access SSH to remote hosts

Install last version of Ansible

[Installation Control Machine](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-the-control-machine)

## Installation

### Using GIT

```bash
cd ~/work-dir
git clone https://github.com/centreon/centreon-iac-ansible.git
cd centreon-iac-ansible
```

### Using Ansible Galaxy

Comming soon

## Role Variables

Task: mariadb-server

- `mysql_root_password`: (string) Password to use with user root

Task: centreon-web

- `php_timezone`: (string)

Timezone to configuration of PHP
[PHP Timezones](http://php.net/manual/en/timezones.php)

- `mysql_hostname`: (string) Hostname or IP to use for connection with Mysql database
- `mysql_port`: (string) Port number to use for connection with Mysql database
- `mysql_root_password`: (string) Password used by user root (you can use variable from mariadb-server task)
- `mysql_centreon_db`: (string) Database name used by Centreon
- `mysql_centstorage_db`: (string) Database name used by Centreon Storage
- `mysql_centreon_username`: (string) Username used by Centreon
- `mysql_centreon_password`: (string) Password user used by Centreon
- `centreon_admin_password`: (string) Password used by user admin (main administrator user)
- `repository`: (string) Centreon repository RPM package URL (Default: `http://yum.centreon.com/standard/18.10/el7/stable/noarch/RPMS/centreon-release-18.10-2.el7.centos.noarch.rpm`)
- `plugin_pack`: (array)

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

### Default values

```yaml
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

## Examples

### Simple Installation

Simple Installation using a Centos clean install and configure a new Host with Centreon

You need a installation of CentOS 7 with SSH server enabled

[Using Vagrant images to prepare Centreon](docs/vagrant.md)

on the control machine, export the ssh key to new host:

```bash
ssh-copy-id root@[remote-ip-or-hostname]
```

Create a new file of hosts with the configuration to connect in the remote host, example:

```bash
vi hosts.deploy
[centreon-server]
centreon-web ansible_port=22 ansible_host=[remote-ip-or-hostname]
```

Create a new file with format YAML to deploy components for installation of Centreon Web

```bash
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

```bash
ansible-playbook -i hosts.deploy centreon-deploy.yml
```
