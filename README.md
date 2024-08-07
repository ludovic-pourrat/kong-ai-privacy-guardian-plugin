# Kong AI Privacy Guardian Plugin

This plugin is AI privacy guardian by detecting PII within the AI prompting and can act in 3 ways

- public classification, does nothing
- confidential classification, the detected PII and redacted with an hash and a token
- secret classification, a 403 response is provided if a PII is detected

This plugin is working on top of the Kong AI gateway feature.

## Build

docker-compose build

## Run it

docker-conpose up