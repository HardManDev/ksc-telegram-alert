@echo off
chcp 1251 > nul

.\bin\python.exe alert.py ^
    --severity "%SEVERITY%" ^
    --computer "%COMPUTER%" ^
    --domain "%DOMAIN%" ^
    --event "%EVENT%" ^
    --description "%DESCR%" ^
    --rise-time "%RISE_TIME%" ^
    --task-name "%KLCSAK_EVENT_TASK_DISPLAY_NAME%" ^
    --product "%KL_PRODUCT%" ^
    --version "%KL_VERSION%" ^
    --severity-num "%KLCSAK_EVENT_SEVERITY_NUM%" ^
    --host-ip "%HOST_IP%" ^
    --host-conn-ip "%HOST_CONN_IP%"