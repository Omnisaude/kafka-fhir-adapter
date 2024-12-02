#!/bin/bash

sleep 10

exec faust -A kafka_fhir_adapter.main worker -l info