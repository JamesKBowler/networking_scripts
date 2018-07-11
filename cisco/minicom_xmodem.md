## Using Minicom XModem to upload IOS to Cisco switch
sudo minicom -s

**Setup Minicom**

Select `Filenames and paths`  
Press `B`  
Then point to the directory of the IOS file  
Select `Serial port setup`  
Press `A`  
Type in the path of serial device `/dev/ttyUSB0`  
Press `E`  
Press `C`  
`Save setup as dfl`  
`Exit`  

**Upload the IOS**

Take a look in flash and format if required
```shell
dir flash:
format flash:
```
Change the baud rate  
```
set BAUD 115200
```
Close the terminal and reconnect  
```
sudo minicom -b 115200
```

Once connected with Minicom
```
copy xmodem:<image name> flash:<image name>
```
Press `Ctrl-A` then `Z`  
Press `S`  
Select `xmodem`  
Press `Enter`  

Once upload is complete reset the baud rate.
```shell
unset BAUD 115200
```
Close the terminal and reconnect
```
sudo minicom
```

**Boot the new IOS**

Take peak in flash for the IOS file name, then boot the new IOS
```
dir flash:
boot flash:<image file name here>
