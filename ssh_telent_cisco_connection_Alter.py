from sys import exit
from os import path as os_path
from telnetlib import Telnet
from _datetime import datetime
from ini import IniConfig
from paramiko import SSHClient, AutoAddPolicy


class CISCO_CONFIG:
    def __init__(self, telnet_session=None, telnet_host2login=None):
        # Variables
        self.config = IniConfig.read('./scripting.ini')
        self.commands_file = self.config.main.commands_file
        self.hostsfile = self.config.main.hostsfile
        self.verbose = self.config.main.verbose
        self.type_connection = self.config.main.type_connection
        self.telnet_session = telnet_session
        self.telnet_host2login = telnet_host2login
        self.w_it = {"Host": telnet_host2login, "Status": "Success", "msg": []}

    def login(self):
        # __username = input("Username: ")
        # password = getpass.getpass("User Password: ")
        # enable = getpass.getpass("Enable Password: ")
        self.w_it["msg"].append('Using default login.\n')
        __username = self.config.main.username
        __password = self.config.main.password
        __enable = self.config.main.enable

        self.telnet_session.read_until(b"Username: ")
        self.telnet_session.write(__username.encode('ascii') + b"\n")

        if __password:
            self.telnet_session.read_until(b"Password: ")
            self.telnet_session.write(__password.encode('ascii') + b"\n")

        if __enable:
            self.telnet_session.read_until(b'>')
            self.telnet_session.write(b"enable\n")
            self.telnet_session.read_until(b"Password: ")
            self.telnet_session.write(__enable.encode('ascii') + b"\n")
            self.w_it["msg"].append("enable Ok, The commands will are executed\n")

    def session_commands(self):
        # Executing commands on the host
        print("Executing Commands on", self.telnet_host2login)
        if os_path.isfile(self.commands_file):
            commands = open(self.commands_file, "r")
            try:
                for cmd2exe in commands:
                    self.w_it["msg"].append(cmd2exe.encode('ascii'))
                    self.telnet_session.write(cmd2exe.encode('ascii')+"\n".encode('ascii'))
            finally:
                commands.close()
        else:
            self.w_it["msg"].append(f"{self.commands_file} doesn't exist")
            print(self.commands_file, " doesn't exist")
            self.telnet_session.write(b"exit\n")
            self.w_it["Status"] = "Error"
            self.w_it["msg"].append(b"exit\n")
        # Displaying the results
        if self.verbose == "yes":
            self.telnet_session.write(b"exit\nexit\nexit\nexit\n")
            output = self.telnet_session.read_all().decode('ascii')
            if "% " in output:
                print("Error: ", output)
                self.w_it["Status"] = "Error"
                self.w_it["msg"].append(f"Error: {output}")
                exit()
            else:
                print(output)
                self.w_it["msg"].append(output)
        self.w_it["msg"].append(f"Logging out of {self.telnet_host2login}")
        finish = LOGS(self.w_it)
        finish.write_log()
        return f"Logging out of {self.telnet_host2login}\n"

    def ssh_solution(self):
        # Connexion SSH
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname=self.telnet_host2login, port=22,
                    username=self.config.main.username,
                    password=self.config.main.password,
                    timeout=5, auth_timeout=5)
        # Passage en mode enabled
        ssh.invoke_shell()
        #ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('enable\n'.encode('ascii'))
        #ssh_stdin.write(str(self.config.main.enable).encode('ascii'))
        # Interaction avec le switch ou routeur
        commands = open(self.commands_file, "r")
        try:
            for cmd2exe in commands:
                print("On execute = ", cmd2exe)
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd2exe)
                output_out = ssh_stdout.read().decode()
                print(output_out)
                command_backup = CISCO_CONFIG()
                command_backup.get_output_to_file(self.telnet_host2login, output_out)
                if ssh_stderr:
                    output_err = ssh_stderr.read().decode()
                    self.w_it["err"].append(output_err)
                else:
                    self.w_it["msg"].append(output_out)
            ssh.close()
        except Exception as err:
            print(err)
        finally:
            finish = LOGS(self.w_it)
            finish.write_log()

    def get_output_to_file(self, file, content):
        dt = datetime.strftime(datetime.now(), '%Y-%M-%d')
        file = dt+file
        with open(file, 'a', encoding='utf-8') as command_export:
            command_export.write(content)
        return True


class BASE(CISCO_CONFIG):
    def userlogin(self):
        __telnet = None
        if os_path.isfile(self.hostsfile):
            __hosts = open(self.hostsfile, "r")
            while 1:
                __host2login = __hosts.readline()
                __host2login = __host2login.replace("\n", "")
                if not __host2login:
                    break
                else:
                    print("Logging into", __host2login)
                    try:
                        print("On essaye en TELNET !")
                        __telnet = Telnet(__host2login, timeout=3)
                        l = CISCO_CONFIG(telnet_session=__telnet, telnet_host2login=__host2login)
                        print(l.login())
                        print(l.session_commands())
                    except Exception as err:
                        print(err)
                    try:
                        print("On essaye en SSH !")
                        ssh_try = CISCO_CONFIG(telnet_host2login=__host2login)
                        print(ssh_try.ssh_solution())
                    except Exception as err:
                        print(err)
            __hosts.close()


class LOGS:
    def __init__(self, json_to_log):
        self.json_to_log = json_to_log

    def write_log(self):
        with open('./bulk.log', 'a') as f:
            if self.json_to_log['Status'] == "Success":
                f.write(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} INFO {self.json_to_log}')
            else:
                f.write(f'\n{datetime.now().strftime("%Y-%m-%d% H:%M:%S")} ERROR {self.json_to_log}')


if __name__ == "__main__":
    out = BASE()
    print(out.userlogin())
