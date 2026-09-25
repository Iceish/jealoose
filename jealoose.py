#!/usr/bin/env python3
import argparse, shlex
from pypsrp.wsman import WSMan
from pypsrp.powershell import PowerShell, RunspacePool

def run(host, user, password, kerberos, cmd, mode, endpoint):
    wsman = WSMan(host, username=user, password=password,
                  auth="kerberos" if kerberos else "negotiate",
                  ssl=False, negotiate_service="WSMAN")
    kw = {"configuration_name": endpoint} if endpoint else {}
    with RunspacePool(wsman, **kw) as pool, PowerShell(pool) as ps:
        if mode == "script":
            ps.add_script(cmd)
        else:
            args = shlex.split(cmd)
            ps.add_cmdlet(args[0])
            for a in args[1:]:
                ps.add_parameter(None, a)
        for item in ps.invoke():
            print(item)
        for e in ps.streams.error:
            print("ERR:", e)

p = argparse.ArgumentParser(description="pypsrp JEA runner")
p.add_argument("-t", "--target", required=True, help="target host")
p.add_argument("-u", "--user", required=True, help="username")
p.add_argument("-p", "--password", required=True, help="password")
p.add_argument("-k", "--kerberos", action="store_true", help="use Kerberos auth (needs pyspnego[kerberos])")
m = p.add_mutually_exclusive_group(required=True)
m.add_argument("-c", "--cmdlet", help="single cmdlet + positional args")
m.add_argument("-s", "--script", help="raw PowerShell script")
p.add_argument("-e", "--endpoint", help="JEA configuration name (default endpoint if omitted)")
a = p.parse_args()

run(a.target, a.user, a.password, a.kerberos, a.cmdlet or a.script,
    "cmdlet" if a.cmdlet else "script", a.endpoint)
