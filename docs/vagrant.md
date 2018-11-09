
Preparation of Vagrant images:

Create a file `Vagrantfile`:

```
Vagrant.configure("2") do |config|
    config.vm.box = "centos/7"
    config.vm.provision "shell" do |s|
      ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
      s.inline = <<-SHELL
        echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
        mkdir /root/.ssh
        echo #{ssh_pub_key} >> /root/.ssh/authorized_keys
        chmod 0700 /root/.ssh
        chmod -R 0600 /root/.ssh/*
      SHELL
    end
    config.vm.network "private_network", ip: "192.168.150.10"
    config.vm.network "forwarded_port", guest: 22, host: 2222, id: "ssh"
    config.vm.network "forwarded_port", guest: 80, host: 10080
end
```

Attention to configure you ssh key necessary to login in SSH server of vagrant machine

Now, you can up the machine:

```
vagrant up
```

You can use these port maps:

2222 -> 22
10080 -> 80

On the Ansible, you can set a file of hosts as show bellow:

```
[centreon-web]
centreon-server ansible_port=2222 ansible_host=172.17.0.1

[centreon-poller]
poller ansible_port=2223 ansible_host=172.17.0.1

[webserver]
nginx-server ansible_port=2224 ansible_host=172.17.0.1
```
