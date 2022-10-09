#!/bin/bash
set -e

source ~/anaconda3/bin/activate nsb

python src/run_all.py api/configurations/cfg.yaml
