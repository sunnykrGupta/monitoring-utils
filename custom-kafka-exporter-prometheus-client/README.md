
## Custom-kafka-exporter-prometheus-client

Custom python exporter for exposing metrics curated from external monitoring systems.

### Description

Written prometheus client will be exposing metrics by curating and collecting custom metrics from prometheus-server and exposing metrics to scrape in prometheus format on default prometheus endpoints.


#### Build on top of it:

> https://github.com/prometheus/client_python#custom-collectors



### Client exposing Metrics URI on

- port : `exporter_port`
- endpoint : `/` and `/metrics`


### Important Metrics exposed

```
- kafka_cluster_request_per_sec
- kafka_server_topic_request_per_sec
```

Metrics type should `gauge`

> https://cloud.google.com/monitoring/api/v3/metrics-details#metrics


### Flow :
 - Query prometheus server via HTTP on available endpoints
 - Build a metrics container to be exposed
 - Apply labels properly to exposed in prometheus format


### Pre-requisite

```
requests==2.12.4
prometheus-client==0.6.0
```
