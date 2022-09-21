import asyncio
import netdev
import os
from datetime import datetime
import ssl
import time
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



#bien toan cuc
localtime = datetime.now().strftime("%d_%m_%y %H_%M_%S")
localtimedir = datetime.now().strftime("%d_%m_%y %H_%M")
biendedem = 1
ketqua = [] 
os.makedirs(localtimedir, exist_ok=True)

#Ham tao folder va file
def Createfolder(hostname, showrun):
    try:
        print ('Vo dc ham ne')
        global localtimedir, localtime, biendedem
        print ('dang tao file ne')
        f = open( localtimedir + '/' + hostname + " " + localtime + " " + str(biendedem) + '.txt','w')
        print('tao duoc file r ne')
        print ('dang nhap du lieu ne')
        f.write(showrun)
        print('du lieu co r ne')
        f.close
    except:
        print ('loi r con ga')

def CreateHTMLTableContent(hostname, ip, status) -> str:
    output = str.format("""
    <tr>
        <td>{0}</td>
        <td>{1}</td>
        <td>{2}</td>
    </tr>
    """, hostname, ip, status)
    return output

#Lay ra ket qua va gui gmail
def Guigmail():
    print("Khoi tao qua trinh gui mail")
    global ketqua
    localtimemail = datetime.now().strftime("%d-%m-%Y_%Hh%Mp%S")
    # port = 465  # For SSL
    server = "smtp.gmail.com:587"
    sender_email = "nvtphuc2001@gmail.com"  # Enter your address
    receiver_email = "nvtphuc2001@gmail.com"  # Enter receiver address

    password = "yguznbjculsanzuy"
    # message = """\
    # Subject: Mang Hoi Dong toi day

    # Thoi gian Backup: """ + str(localtimemail) + """ \n
    # Backup thanh cong: """ + str(ketqua) + """ \n
    # Backup that bai: """ + str(thatbai) + """ \n
    # ------------------------------------------------------"""
    print("Khoi tao noi dung mail")
    table = ""
    for device in ketqua:
        out = CreateHTMLTableContent(hostname=device['hostname'], ip=device['ip'], status=device['status'])
        table = table+out

    html = """
    <html>
        <head>
            <style>
                .gmail-table {{
                    border: solid 5px #DDEEEE;
                    border-collapse: collapse;
                    border-spacing: 0;
                }}

                .gmail-table thead th {{
                    background-color: #DDEFEF;
                    border: solid 3px #DDEEEE;
                    color: #336B6B;
                    padding: 10px;
                    text-align: left;
                    text-shadow: 1px 1px 1px #fff;
                }}

                .gmail-table tbody td {{
                    border: solid 3px #DDEEEE;
                    color: #333;
                    padding: 10px;
                    text-shadow: 1px 1px 1px #fff;
                }}
            </style>
        </head>
        <body>
            <table class="gmail-table">
                <thead>
                    <tr>
                        <th>Hostname</th>
                        <th>IP address</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {0}
                </tbody>
            </table>
        </body>
    </html>
    """.format(table)
    print("Khoi tao noi dung thanh cong\nBat dau qua trinh gui mail")

    message = MIMEMultipart()
    message['Subject'] = "Mang Hoi Dong Thi toi day"
    message['From'] = sender_email
    message['To'] = receiver_email
    message.attach(MIMEText(html,'html'))
    #lenh gui gmail di
    server = smtplib.SMTP(server)
    server.ehlo()
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, message)
    print("Gui mail thanh cong")

#ham xu li thong tin
async def task(param):
    try:
        print ('khai bao global')
        global ketqua, thatbai, localtimedir, localtime, biendedem
        print('dang xu li con ' + str(param['host']))
        async with netdev.create(**param) as ios:
            # find hostname
            print ('vao ham tim hostname ne')
            hostname = ios.base_prompt.title()
            print ('Tim duoc r ne ' + hostname)
            # Backup Running-Config
            print ('di tim show run')
            out = await ios.send_command("show run")
            # print(out)
            print ('tim duoc r ne')
            Createfolder(str(hostname), str(out))
            biendedem = biendedem + 1
            # ketqua.append(hostname + " " + param['host'])
            ketqua.append(dict({"hostname":hostname, "ip": param['host'], "status": "success"}))
            print('Backup thanh cong ' + hostname + " " + str(param['host']))
    except Exception as ex:
        ketqua.append(dict({"hostname":param['host'], "ip": param['host'], "status": "fail"}))
        print ('Backup khong thanh cong ' +(str(param['host'])) )
        print (ex)


#Ham chay chinh
async def run():
    dev1 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '192.168.1.3',
            #  'ghichu': '123',
    }
    dev2 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '192.168.1.1',
            #  'ghichu': 'con thu 3 tren rack',
    }
    dev3 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '10.67.1.3',
            #  'ghichu': 'abc',
    }
    dev4 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '192.168.1.2',
            #  'ghichu': 'Cung la switch ma no la lam',
    }
    dev5 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '10.67.1.4',
    }
    dev6 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '192.168.1.4',
    }
    dev7 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '10.67.1.5',
    }
    dev8 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '192.168.1.5',
    }
    dev9 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '10.67.1.6',
    }
    dev10 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '192.168.1.6',
    }
    dev11 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '10.67.1.7',
    }
    dev12 = { 'username' : 'admin',
             'password' : 'admin1pass',
             'device_type': 'cisco_ios',
             'host': '192.168.11.7',
    }

    #khoi tao cong viec
    # devices = [dev1, dev2,dev3, dev4,dev5, dev6,dev7, dev8,dev9, dev10,dev11, dev12]
    devices = [dev1, dev2]
    # devices = [dev1, dev2, dev3, dev4, dev5, dev6,]
    tasks = [task(dev) for dev in devices]
    await asyncio.wait(tasks)
#Chay vong lap
startTime = time.perf_counter()
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
endTime = time.perf_counter() - startTime
print(endTime)
Guigmail()