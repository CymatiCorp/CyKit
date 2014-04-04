echo off
PATH=C:\Python27\;C:\Python27\Scripts;
echo The Render EEG Graph requires PyGame to run.
echo Plug in Emotiv USB device. 
pause
echo on
Python.exe .\Python\EmotKit\render.py
pause
