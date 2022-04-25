#!/bin/bash

sudo mkdir -p /etc/bluesky
sudo touch /etc/bluesky/kafka.yml

# TODO: add a realistic config file so that `nslsii.configure_base(..., publish_documents_with_kafka=True)` does not fail.
