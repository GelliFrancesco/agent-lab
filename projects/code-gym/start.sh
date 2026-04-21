#!/bin/bash
cd /Users/fgelli/Workspace/agent-lab/projects/code-gym
export PYTHONPATH="$(pwd)"
python3 app/app.py >> /tmp/codegym.log 2>&1