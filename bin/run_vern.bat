cd %~dp0
:loop
if not "%~nx1"=="" (
  python run_vern.py %~f1 & shift & goto loop
)
pause