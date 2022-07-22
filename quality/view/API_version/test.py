#IP查询
import  socket
# ip=socket.gethostbyname('www.baidu.com')
# print(ip)

#whois 查询
from whois import whois
data=whois('www.baidu.com')
print(data)