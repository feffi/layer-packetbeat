import charms.apt
from charms.reactive import when
from charms.reactive import when_not
from charms.reactive import when_any
from charms.reactive import set_state
from charms.reactive import remove_state

from charmhelpers.core.hookenv import status_set
from charmhelpers.core.host import service_restart

from elasticbeats import render_without_context
from elasticbeats import enable_beat_on_boot
from elasticbeats import push_beat_index


@when_not('apt.installed.packetbeat')
def install_filebeat():
    status_set('maintenance', 'Installing packetbeat')
    charms.apt.queue_install(['packetbeat'])


@when('beat.render')
@when_any('elasticsearch.available', 'logstash.available')
def render_filebeat_template():
    render_without_context('packetbeat.yml', '/etc/packetbeat/packetbeat.yml')
    remove_state('beat.render')
    service_restart('packetbeat')
    status_set('active', 'Packetbeat ready')


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
