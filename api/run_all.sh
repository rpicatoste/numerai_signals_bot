#!/bin/bash
set -e

source ~/anaconda3/bin/activate nsb

python src/data/database_generator.py

python src/models/model_trainer.py
