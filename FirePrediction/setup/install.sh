#!/usr/bin/env bash

locale-gen UTF-8

echo "Install packages ..."
# Update
apt-get update -y && apt-get upgrade -y

# Java
sudo apt-add-repository -y ppa:webupd8team/java > /dev/null 2>&1
sudo add-apt-repository -y ppa:git-core/ppa > /dev/null 2>&1
sudo apt-get update > /dev/null 2>&1
sudo apt-get install -y git
sudo apt-get install -y oracle-java8-installer

# Python
sudo apt-get install python-software-properties
sudo apt-get install -y python-dev python-pip python-setuptools 

# Zip
sudo apt-get install -y zip

# JQ: helps parsing json on bash
sudo apt-get install jq