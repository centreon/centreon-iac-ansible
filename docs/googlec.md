# Deploy Centreon with Ansible and Google Cloud Compute

Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#usage)
  - [Ubuntu](#using-ubuntu-linux)
  - [Centos/RedHat](#using-centos-redhat)
- [Ansible](#installation-of-ansible)
- [Centreon Deploy](#centreon-deploy)
- [Screencast](#screencast)

## Overview

This tutorial is intended to guide and exemplify the use of the Ansible tool to deploy a **Centreon** environment in Google cloud service.

The idea is to show how easy it is to implement and automate the entire creation and maintenance process of **Centreon** in a cloud, from instance creation to configuration.

## Requirements

To use automation with Google Cloud, we first need to perform some tasks in the admin panel on Google, to do this, you will need to create the credentials.

It’s easy to create a GCP account with credentials for Ansible. You have multiple options to get your credentials - here are two of the most common options:

- Service Accounts (Recommended): Use JSON service accounts with specific permissions.
- Machine Accounts: Use the permissions associated with the GCP Instance you’re using Ansible on.

For the following examples, we’ll be using service account credentials.

To work with the GCP modules, you’ll first need to get some credentials in the JSON format:

1. [Create a Service Account](https://developers.google.com/identity/protocols/OAuth2ServiceAccount#creatinganaccount)
2. [Download JSON credentials](https://support.google.com/cloud/answer/6158849?hl=en&ref_topic=6262490#serviceaccounts)

See more in [this link](https://docs.ansible.com/ansible/latest/scenario_guides/guide_gce.html).

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

You will need some libraries to support Google Cloud Compute

#### Ubuntu

```bash
sudo apt install -y python-google-auth python-requests python-libcloud
```

#### Centos/Redhat

```bash
sudo yum install -y python-requests python2-libcloud
```

### Centreon Deploy

Now prepare the environment with the Anson module for the deploy of the Centeron, for this, we will use the repository of the implementation module of Centeron through Git.

```bash
git clone https://github.com/centreon/centreon-iac-ansible.git
cd centreon-iac-ansible
```

You will now need to prepare your deploy yaml file and the access key provided by Google in json format, as per the instructions in this site.

Here, I'm going to use the sample deploy file provided in the Centreon module repository:

```bash
cp docs/examples/gc-centreon.yml .
```

Edit the file `gc-centreon.yml` with your values from Google Compute:

```yaml
  vars:
    service_account_email: XXXXXXXXX-compute@developer.gserviceaccount.com
    credentials_file: centreon-XXXXXXXXX.json
    project_id: centreon-XXXXXXX
    machine_type: f1-micro
    image: centos-7
```

Set the `machine_type` according to your needs and save the file.

Now you will need to create or use your public ssh key to use in Google Compute instances, if you do not already have it, use the command below to create and get the public key

![SSH keygen](images/sshkeygen.gif)

#### Tip

To avoid stops with key issues in ssh, add this line in the configuration file of your ssh

```bash
cat <<EOF >> ~/.ssh/config
Host *
    StrictHostKeyChecking no
EOF
chmod 0600 ~/.ssh/config
```

Use the public key in the new instances by adding in the block on the file `gc-centreon.yml`

```yaml
metadata: '{"ssh-keys":"admin: ... add your public ssh key here ... "}'
```

With this and with your proper settings of deploy of the Centeron, just run the deploy command of Ansible

```bash
ansible-playbook gc-centreon.yml
```

## Screencast

You can follow here a complete screencast of deploy in Google Compute
[![Centreon Ansible with Google](http://img.youtube.com/vi/N3bkI40HXoY/0.jpg)](http://www.youtube.com/watch?v=N3bkI40HXoY)
