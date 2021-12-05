set /p ip="Enter IP: 192.168.1."
for /l %%x in (1, 1, 1000) do (
   echo %%x
   start cmd /k "ping 192.168.1.%ip% & exit"
)