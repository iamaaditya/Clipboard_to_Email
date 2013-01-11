import sys
import smtplib
 
from email.mime.text import MIMEText
#Required for email modules
import ctypes
 
#Get required functions, strcpy..
strcpy = ctypes.cdll.msvcrt.strcpy
ocb = ctypes.windll.user32.OpenClipboard    #Basic Clipboard functions
ecb = ctypes.windll.user32.EmptyClipboard
gcd = ctypes.windll.user32.GetClipboardData
scd = ctypes.windll.user32.SetClipboardData
ccb = ctypes.windll.user32.CloseClipboard
ga = ctypes.windll.kernel32.GlobalAlloc    # Global Memory allocation
gl = ctypes.windll.kernel32.GlobalLock     # Global Memory Locking
gul = ctypes.windll.kernel32.GlobalUnlock
GMEM_DDESHARE = 0x2000
 
def Get( ):
  ocb(None) # Open Clip, Default task
 
  pcontents = gcd(1)
 
  data = ctypes.c_char_p(pcontents).value
 
  #gul(pcontents) ?
  ccb()
 
  return data
 
def Paste( data ):
  ocb(None) # Open Clip, Default task
 
  ecb()
 
  hCd = ga( GMEM_DDESHARE, len( bytes(data,"ascii") )+1 )
 
  pchData = gl(hCd)
 
  strcpy(ctypes.c_char_p(pchData),bytes(data,"ascii"))
 
  gul(hCd)
 
  scd(1,hCd)
 
  ccb()
 
clp = Get()
print(clp)
 
 
# Create a text/plain message
msg = MIMEText(str(clp))
msg['Subject'] = 'put the subject you require, I keep it fix to some obsure word'
#idea behind using obsure code is to help me arrange emails
#you could also use sys.argv for subject but I want to keep the process minimal & quick
 
msg['From']	= "YourEmailAddress"
msg['To'] 	= "RecipientAddress"
 
s = smtplib.SMTP('smtp.gmail.com', 587) 
# these values are for gmail, you may want to change it if others
s.ehlo()
s.starttls()
passwordGl = 'your email password here'
 
s.login(msg['From'], passwordGl)
try:
   # Python 3.2.1
   print(s.send_message(msg))
except AttributeError:
   # Python 2.7.2
   s.sendmail(msg['From'], [msg['To']], msg.as_string())
 
s.quit()