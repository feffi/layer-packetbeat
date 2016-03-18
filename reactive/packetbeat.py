from charms.reactive import when
from charms.reactive import when_file_changed
from charms.reactive import when_not
from charms.reactive import set_state
from charms.reactive import remove_state

from charmhelpers.core.hookenv import status_set
from charmhelpers.core.host import service_restart
from charmhelpers.fetch import apt_install

from elasticbeats import render_without_context
from elasticbeats import enable_beat_on_boot
from elasticbeats import push_beat_index


@when('beats.repo.available')
@when_not('packetbeat.installed')
def install_packetbeat():
    status_set('maintenance', 'Installing packetbeat')
    apt_install(['packetbeat'], fatal=True)
    set_state('packetbeat.installed')


@when('beat.render')
def render_packetbeat_template():
    render_without_context('packetbeat.yml', '/etc/packetbeat/packetbeat.yml')
    remove_state('beat.render')
    status_set('active', 'Packetbeat ready')


@when('config.changed.install_sources')
@when('config.changed.install_keys')
def reinstall_packetbeat():
    remove_state('packetbeat.installed')


@when_file_changed('/etc/filebeat/packetbeat.yml')
def restart_packetbeat():
    ''' Anytime we touch the config file, cycle the service'''
    service_restart('packetbeat')


@when('packetbeat.installed')
@when_not('packetbeat.autostarted')
def enlist_packetbeat():
    enable_beat_on_boot('packetbeat')
    set_state('packetbeat.autostarted')


@when('elasticsearch.available')
@when_not('packetbeat.index.pushed')
def push_packetbeat_index(elasticsearch):
    hosts = elasticsearch.list_unit_data()
    for host in hosts:
        host_string = "{}:{}".format(host['host'], host['port'])
    push_beat_index(host_string, 'packetbeat')
    set_state('packetbeat.index.pushed')
