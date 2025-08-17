#!/bin/bash

cd /root/Pseudo/Education/mcp_servers
export PYTHONPATH=/root/Pseudo/Education/.venv/lib/python3.13/site-packages:/root/Pseudo/Education:$PYTHONPATH
/root/Pseudo/Education/.venv/bin/python -m uvicorn mcp_servers.__main__:app --host 0.0.0.0 --port 8000