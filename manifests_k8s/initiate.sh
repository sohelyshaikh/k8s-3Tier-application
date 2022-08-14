#!/bin/bash

kubectl -n final apply -f pvc.yaml
kubectl -n final apply -f mysecrets.yaml
kubectl -n final apply -f myconfigMap.yaml
kubectl -n final apply -f mysql-initdb-config.yaml 
kubectl -n final apply -f mysql.yaml
kubectl -n final apply -f service.yaml
kubectl -n final apply -f pod-frontend.yaml
kubectl -n final apply -f lb-service.yaml
kubectl -n final get all
sleep 10
echo "waiting for 10 seconds..."
kubectl -n final get all