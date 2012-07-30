rem c:\Python26\Lib\site-packages\PyQt4\pyuic4 %1 > "ui_"%~n1".py" 

for %%f in (*.ui) do (

	echo %%~nf
	c:\Python26\Lib\site-packages\PyQt4\pyuic4 %%~nf.ui > ui_%%~nf.py
)


