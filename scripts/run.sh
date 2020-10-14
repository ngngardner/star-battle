#!/bin/bash
( \
    source .env/bin/activate; \
    python ./star_battle/star_battle.py; \
)