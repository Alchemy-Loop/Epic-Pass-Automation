@echo off
FOR /f %%p in ('where python3.8.exe') do SET PYTHONPATH=%%p
echo %PYTHONPATH%
set DIRECTORY=%CD%
set COMBINED="%DIRECTORY%\main.py"
%PYTHONPATH% %COMBINED%
pause