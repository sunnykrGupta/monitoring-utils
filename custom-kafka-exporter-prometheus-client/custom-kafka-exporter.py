#!/usr/bin/env python

'''

Prometheus instrumentation library for Python applications
https://github.com/prometheus/client_python#custom-collectors

Custom python exporter for exposing metrics curated from external monitoring systems.

'''

import time
import requests
import urllib.parse
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

# custom import
import config

#------------------------------------------


def return_prom_query(query_type, job):
    if query_type == 'cluster':
        prom_query = ('sum without(instance)(rate(kafka_server_brokertopicmetrics_messagesin_total{job="%s",topic=""}[5m]))' % (job) )
        return prom_query

    if query_type == 'cluster_topic':
        # cluster RPS query
        prom_query = ('sum without(instance)(rate(kafka_server_brokertopicmetrics_messagesin_total{job="%s",topic!=""}[5m]))' % (job) )
        return prom_query

    return None


# query and get metrics to expose
def get_cluster_rps():

    metrics_container =  []


    for job in config.job_Names:
        print("\n ============= Cluster RPS : %s =============" % (job) )

        # cluster RPS query
        prom_query = return_prom_query('cluster', job)

        if prom_query is not None:
            API_Query_URI = config.API_URI + urllib.parse.quote_plus(prom_query)

            try:
                result = requests.get(API_Query_URI)

                if result.json()['status'] == 'success':
                    metrics_json =  result.json()['data']

                    if metrics_json['resultType'] == 'vector' and len(metrics_json['result']) > 0:

                        for x in metrics_json['result']:
                            metrics_container.append(x)
                    else:
                        print("Not-Available")
            except Exception as e:
                print(e)
        else:
            pass


    return metrics_container


# query and get metrics to expose
def get_cluster_topic_rps():

    metrics_container =  []

    for job in config.job_Names:
        print("\n============= TOPIC RPS : %s =============" % (job) )

        # cluster topic RPS query
        prom_query = return_prom_query('cluster_topic', job)

        if prom_query is not None:
            API_Query_URI = config.API_URI + urllib.parse.quote_plus(prom_query)

            result = requests.get(API_Query_URI)

            try:
                result = requests.get(API_Query_URI)

                if result.json()['status'] == 'success':
                    metrics_json =  result.json()['data']

                    if metrics_json['resultType'] == 'vector' and len(metrics_json['result']) > 0:

                        for x in metrics_json['result']:
                            metrics_container.append(x)
                    else:
                        print("Not-Available")
            except Exception as e:
                print(e)
        else:
            pass

    for x in metrics_container:
        print(x)
    return metrics_container



#---------------------------------------------

'''
Metrics type should `gauge`
- https://cloud.google.com/monitoring/api/v3/metrics-details#metrics
'''
class CustomCollector(object):

    def collect(self):

        # topic level metrics
        topic_metrics_container = get_cluster_topic_rps()
        #print(topic_metrics_container)

        if len(topic_metrics_container) > 0:
            topic = GaugeMetricFamily('kafka_server_topic_request_per_sec', 'Kafka Topic wide metrics', labels=['cluster','topic'])

            for x in topic_metrics_container:
                cluster_name = x['metric']['job']
                topic_name = x['metric']['topic']
                topic.add_metric([cluster_name,topic_name], float(x['value'][1]) )

        # cluster level metrics
        cluster_metrics_container = get_cluster_rps()
        #print(cluster_metrics_container)

        if len(cluster_metrics_container) > 0:
            cluster = GaugeMetricFamily('kafka_cluster_request_per_sec', 'Kafka Cluster wide metrics', labels=['cluster'])

            for x in cluster_metrics_container:
                print([x['metric']['job']], x['value'][1])
                cluster.add_metric([x['metric']['job']], float(x['value'][1]) )

        yield topic
        yield cluster


# Register your Collector
REGISTRY.register(CustomCollector())




if __name__ == '__main__':
    # Start up the server to expose the metrics.
    print("\n\n\tExporter listening on port : %s" % (config.exporter_port))
    start_http_server(config.exporter_port)

    #print(get_cluster_rps())
    #print(get_cluster_topic_rps())

    # Generate some requests.
    while True:
        time.sleep(60)
