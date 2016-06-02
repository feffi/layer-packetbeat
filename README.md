# Packetbeat

Network data can tell you a detailed story of what's going on across your
applications. Packetbeat is an open source project that is designed to provide
real‑time analytics for web, database, and other network protocols. Whether
you're in IT operations, security, or a business analyst, you can rapidly
extend Packetbeat's functionality by adding new protocols, metrics, and
analytics.

## Usage

Packetbeat can be added to any principal charm thanks to the wonders of being
a subordinate charm. The following usage example will deploy the elk stack,
so we can visualize our wire data once we've established the link between
packetbeat and Logstash

    juju deploy cs:~containers/bundle/elk-stack
    juju deploy cs:trusty/consul
    juju deploy cs:trusty/packetbeat
    juju add-relation packetbeat:beats-host consul
    juju add-relation packetbeat logstash


### Deploying the minimal Beats formation

If you do not need log buffering and alternate transforms on your data thats
being shipped to ElasticSearch you can simply deploy the 'beats-base' bundle
which stands up Elasticsearch, Kibana, and the three known working Beats
subordinate services.

    juju deploy cs:bundle/beats-core
    juju deploy ubuntu
    juju add-relation filebeat:beats-host ubuntu
    juju add-relation topbeat:beats-host ubuntu
    juju add-relation packetbeat:beats-host ubuntu

### A note about the beats-host relationship

The Beats suite of charms leverage the implicit "juju-info" relation interface
which is special and unique in the context of subordinates. This is what allows
us to relate the beat to any host, but may have some display oddities in the
juju-gui. Until this is resolved, it's recommended to relate beats to their
principal services using the CLI

### Changing whats being shipped


## Testing the deployment

The services provide extended status reporting to indicate when they are ready:

    juju status --format=tabular

This is particularly useful when combined with watch to track the on-going
progress of the deployment:

    watch -n 0.5 juju status --format=tabular

The message for each unit will provide information about that unit's state.
Once they all indicate that they are ready, you can navigate to the kibana
url and view the streamed log data from the Ubuntu host.

    juju status kibana --format=yaml | grep public-address

  open http://&lt;kibana-ip&gt;/ in a browser and begin creating your dashboard
  visualizations

## Scale Out Usage

This bundle was designed to scale out. To increase the amount of log storage and
indexers, you can add-units to elasticsearch.

    juju add-unit elasticsearch

You can also increase in multiples, for example: To increase the number of
Logstash parser/buffer/shipping services:

    juju add-unit -n 2 logstash

To monitor additional hosts, simply relate the Packetbeat subordinate

    juju add-relation packetbeat:beats-host my-charm

And configure as required according to the configuration section above.

## Contact information

- Charles Butler &lt;charles.butler@canonical.com&gt;
- Matt Bruzek &lt;matthew.bruzek@canonical.com&gt;

# Need Help?

- [Beats Upstream](https://github.com/elastic/beats)
- [Other groovy things ~containers has done](http://jujucharms.com/u/containers)
- [Juju mailing list](https://lists.ubuntu.com/mailman/listinfo/juju)
- [Juju Community](https://jujucharms.com/community)
