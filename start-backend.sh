#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/backend"
mvn -q -DskipTests package
exec java -jar target/incident-desk-0.0.1-SNAPSHOT.jar
