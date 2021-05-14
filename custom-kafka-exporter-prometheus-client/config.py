
# Prometheus Central Server address
# for querying metrics
prom_server_host = "prometheus-central"
prom_server_port = "9090"

API_URI = ("http://%s:%s/api/v1/query?query=" % (prom_server_host, prom_server_port))

# Add prometheus job names
job_Names = ['my_kafka_cluster']


# client port to expose metrics on
# curl on '/' or '/metrics'
exporter_port = 8080
