#!/usr/bin/env python3
import argparse, shlex
from pypsrp.wsman import WSMan
from pypsrp.powershell import PowerShell, RunspacePool

def run(host, user, password, kerberos, cmd, mode, endpoint, info):
    wsman = WSMan(host, username=user, password=password,
                  auth="kerberos" if kerberos else "negotiate",
                  ssl=False, negotiate_service="WSMAN")
    kw = {"configuration_name": endpoint} if endpoint else {}
    with RunspacePool(wsman, **kw) as pool, PowerShell(pool) as ps:
        if info:
            ps.add_cmdlet("Get-Command")
            if cmd:
                ps.add_parameter(None, cmd)
            ps.invoke()
            for item in ps.output:
                ap = item.adapted_properties
                print(f"== {ap.get('Name')} ({ap.get('CommandType')}) ==")
                print(ap.get("ScriptBlock"))
                print()
            return
        if mode == "script":
            ps.add_script(cmd)
        else:
            for seg in cmd.split("|"):
                args = shlex.split(seg)
                ps.add_cmdlet(args[0])
                for a in args[1:]:
                    ps.add_parameter(None, a)
        for item in ps.invoke():
            print(item)
        for e in ps.streams.error:
            print("ERR:", e)

p = argparse.ArgumentParser(prog="jealoose")
p.add_argument("-t", "--target", required=True)
p.add_argument("-u", "--user", required=True)
p.add_argument("-p", "--password", required=True)
p.add_argument("-k", "--kerberos", action="store_true")
p.add_argument("-i", "--info", action="store_true", help="dump command definitions")
m = p.add_mutually_exclusive_group(required=True)
m.add_argument("-c", "--cmdlet")
m.add_argument("-s", "--script")
p.add_argument("-e", "--endpoint")
a = p.parse_args()

run(a.target, a.user, a.password, a.kerberos, a.cmdlet or a.script,
    "cmdlet" if a.cmdlet else "script", a.endpoint, a.info)
