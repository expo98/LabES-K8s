#!/bin/bash
echo "time,current,desired,metric"
while true; do
  echo "$(date +%T),$(minikube kubectl -- get hpa demo-app-hpa -o jsonpath='{.status.currentReplicas},{.status.desiredReplicas},{.status.currentMetrics[0].resource.current.averageUtilization}{.status.currentMetrics[0].external.current.averageValue}')"
  sleep 5
done
