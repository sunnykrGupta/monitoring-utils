
## How to query prometheus server via HTTP

    > https://prometheus.io/docs/prometheus/latest/querying/api/

Instant queries

The following endpoint evaluates an instant query at a single point in time:

```
GET /api/v1/query
```

URL query parameters:

    query=<string>: Prometheus expression query string.
    time=<rfc3339 | unix_timestamp>: Evaluation timestamp. Optional.
    timeout=<duration>: Evaluation timeout. Optional. Defaults to and is capped by the value of the -query.timeout flag.



# Cluster level RPS
$ curl 'http://localhost:9090/api/v1/query?query=sum without(instance)(rate(kafka_server_brokertopicmetrics_messagesin_total{job="my_kafka_cluster",topic=""}[5m]))'

After URL encoding :

> http://localhost:9090/api/v1/query?query=sum+without%28instance%29%28rate%28kafka_server_brokertopicmetrics_messagesin_total%7Bjob%3D%22my_kafka_cluster%22%2Ctopic%3D%22%22%7D%5B5m%5D%29%29

Result : {  "status":"success",
            "data":{
                "resultType":"vector",
                "result":[{
                        "metric":{"job":"my_kafka_cluster"},
                        "value":[1554108126.065,"39047.558333333334"]}]
        }}%


# for getting topic wise RPS
$ curl 'http://localhost:9090/api/v1/query?query=sum without(instance)(rate(kafka_server_brokertopicmetrics_messagesin_total{job="my_kafka_cluster",topic!=""}[5m]))'

After URL encoding :

> http://localhost:9090/api/v1/query?query=sum+without%28instance%29%28rate%28kafka_server_brokertopicmetrics_messagesin_total%7Bjob%3D%22my_kafka_cluster%22%2Ctopic%21%3D%22%22%7D%5B5m%5D%29%29'
