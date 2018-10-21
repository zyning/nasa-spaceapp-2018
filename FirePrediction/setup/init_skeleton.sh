#!/bin/bash
NYC_RAW_DIR="../firecaster_model/data/raw"
NYC_INTREIM_DIR="../firecaster_model/data/intreim"
NYC_PROCESSED_DIR="../firecaster_model/data/processed"

if [ -d $NYC_RAW_DIR ]; then rm -Rf $NYC_RAW_DIR; fi
if [ -d $NYC_INTREIM_DIR ]; then rm -Rf $NYC_INTREIM_DIR; fi
if [ -d $NYC_PROCESSED_DIR ]; then rm -Rf $NYC_PROCESSED_DIR; fi

mkdir -p $NYC_RAW_DIR
mkdir -p $NYC_INTREIM_DIR
mkdir -p $NYC_PROCESSED_DIR

