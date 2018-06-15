@echo Writing chapter wordcount to wordcount.html ...
@echo off 
REM this need to be chaged to where your wordcount perd dist is and your tex folders
perl C:\Users\toby\Downloads\TeXcount_3_1\texcount.pl -v -html C:\dev\projects\uni\FinalYearProject\LaTeX\tex\chapters\0*.tex > wordcount.html
REM to run with appendix also, remove the 0* and replace with *
@echo Done.