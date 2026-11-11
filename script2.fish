#!/usr/bin/env fish
#
for i in 1 2 3 4 5
    curl -s -o /dev/null -w "process: %{http_code} %{time_total}s\n" http://127.0.0.1:9080/patients/notes/process/
end

for i in 1 2 3 4 5
    curl -s -o /dev/null -w "notes GET: %{http_code} %{time_total}s\n" http://127.0.0.1:9080/patients/notes/
end

curl -s -o /dev/null -w "notes POST: %{http_code} %{time_total}s\n" -X POST -H "Content-Type: application/json" -d '{"patient_id":3,"text":"follow-up visit, stable"}' http://127.0.0.1:9080/patients/notes/
