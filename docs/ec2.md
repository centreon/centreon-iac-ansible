# Deploy Centreon with Ansible and Amazon EC2

Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#usage)
  - [Ubuntu](#using-ubuntu-linux)
  - [Centos/RedHat](#using-centos-redhat)
- [Ansible](#installation-of-ansible)
- [Centreon Deploy](#centreon-deploy)

## Overview

This tutorial is intended to guide and exemplify the use of the Ansible tool to deploy a **Centreon** environment in Amazon EC2 service.

The idea is to show how easy it is to implement and automate the entire creation and maintenance process of **Centreon** in a cloud, from instance creation to configuration.

## Requirements

To use automation with Amazon EC2, we first need to perform some tasks in the admin panel on AWS, to do this, you will need to create the access keys.

See more in [this link](https://docs.aws.amazon.com/general/latest/gr/managing-aws-access-keys.html).

## Installation

### Using Ubuntu Linux

If you already have a system ready to use Ansible, skip to the [Ansible installation step](#Installation_of_Ansible).

#### With Vagrant

Create a new environment

```bash
mkdir ubuntu-ansible
cd ubuntu-ansible
vagrant init ubuntu/bionic64
vagrant up
vagrant ssh
```

Add basic tools

```bash
sudo apt update
sudo apt install -y curl less neovim dialog libterm-readline-gnu-perl
```

#### With Docker

Create a new environment

```bash
docker run -it --hostname ubuntu-ansible ubuntu:latest
```

Add basic tools

```bash
apt update
apt install -y sudo curl less neovim dialog libterm-readline-gnu-perl
```

### Using Centos/Redhat Linux

If you already have a system ready to use Ansible, skip to the [Ansible installation step](#installation-of-ansible).

#### With Vagrant

Create a new environment

```bash
mkdir centos-ansible
cd centos-ansible
vagrant init centos/7
vagrant up
vagrant ssh
```

Add basic tools

```bash
sudo yum upgrade -y
sudo yum install -y epel-release
sudo yum install -y curl less git
```

#### With Docker

Create a new environment

```bash
docker run -it --hostname centos-ansible centos:7
```

Add basic tools

```bash
yum upgrade -y
yum install -y epel-release
yum install -y sudo curl less git
```

### Installation of Ansible

It is recommended that you always use the latest stable version of Ansible. The project supports a wide range of operating systems. You can see more information at [this link](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).

#### Ubuntu

```bash
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt-get install -y ansible
```

#### Centos/Redhat

```bash
sudo yum install -y ansible
```

### Centreon Deploy

Now prepare the environment with the Ansible module for the deploy of the **Centreon**, for this, we will use the repository of the implementation module of **Centreon** through Git.

```bash
git clone https://github.com/centreon/centreon-iac-ansible.git
cd centreon-iac-ansible
```

Here, I'm going to use the sample deploy file provided in the Centreon module repository:

```bash
cp docs/examples/ec2-centreon.yml .
```

Edit the file `ec2-centreon.yml` with your values from Amazon EC2:

```yaml
    - name: Provision a set of instances
      ec2:
         aws_access_key: "XXXXXXXXXXXXXXXXXX"
         aws_secret_key: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
         key_name: your_key_name
         instance_type: t2.micro
         image: "ami-e0eac385"
         region: us-east-2
         group: ansible-lab
         wait: true
         exact_count: 1
         count_tag:
            Name: Centreon
         instance_tags:
            Name: Centreon
      register: ec2
```

Set the `instance_type` and `region` according to your needs and save the file.

With this and with your proper settings of deploy of the **Centreon**, just run the deploy command of Ansible

```bash
ansible-playbook gc-centreon.yml
```
