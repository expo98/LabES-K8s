#!/usr/bin/env fish
#
for i in (seq 1 50); curl -s -o /dev/null http://127.0.0.1:9080/django; end
sleep 60
minikube kubectl -- get --raw "/apis/external.metrics.k8s.io/v1beta1" | jq | tee evidence/05-external-api.json
minikube kubectl -- get hpa
