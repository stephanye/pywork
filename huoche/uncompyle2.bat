:: author: pcat
:: http://pcat.cnblogs.com
@echo off
if defined python_home (
    python "%python_home%\Scripts\uncompyle2" %1 %2 %3 %4 %5 %6 %7 %8 %9
)else (
    echo "you need to set PYTHON_HOME"
)