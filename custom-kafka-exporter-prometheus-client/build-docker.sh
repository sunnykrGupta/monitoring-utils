if [ -z "$1" ]
  then
    echo "ERROR !! Docker version argument empty"
    echo ; echo "Usage : sh docker-build.sh <version>"
else
    docker build -t gcr.io/my-org/k8s/monitoring/python/custom-kafka-exporter:$1 .
fi
