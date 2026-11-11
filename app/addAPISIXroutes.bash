for r in notes-process:/patients/notes/process/ notes-io:/patients/notes/; do
  name=${r%%:*}; uri=${r#*:}
  curl -i -X PUT http://127.0.0.1:9181/apisix/admin/routes/$name \
    -H "X-API-KEY: edd1c9f034335f136f87ad84b625c8f1" -d "{
      \"name\": \"$name\", \"uri\": \"$uri\",
      \"upstream\": {\"type\": \"roundrobin\",
        \"nodes\": {\"demo-app.default.svc.cluster.local:80\": 1}}}"
done