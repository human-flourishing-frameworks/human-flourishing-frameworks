@echo off
set LANTERN_LLM_PROVIDER=openai
set LANTERN_OPENAI_BASE_URL=http://127.0.0.1:1234/v1
set LANTERN_OPENAI_MODEL=qwen2.5-coder-7b-instruct
set OPENAI_API_KEY=lm-studio
set LANTERN_LLM_TIMEOUT=120
set LANTERN_LLM_MAX_TOKENS=900
cd /d C:\tmp\hff-lantern-recovery
python apps\lantern-local-chat\local_lantern_server.py --host 127.0.0.1 --port 8766
