# jealoose

Minimal pypsrp runner for restricted (JEA / NoLanguage) WinRM runspaces.

## Usage

    python3 jealoose.py -t HOST -u USER -p PASS -c "Get-Command"
    python3 jealoose.py -t HOST -u USER -p PASS -s "whoami"
    python3 jealoose.py -t HOST -u USER -p PASS -s "whoami" -e MeowMeowEndpoint
    python3 jealoose.py -t host.fqdn -u USER@REALM -p PASS -k -c "whoami"

## Options

    -t  target host (FQDN with -k)
    -u  username
    -p  password
    -k  kerberos (needs pyspnego[kerberos])
    -c  cmdlet mode (NoLanguage-safe)
    -s  script mode
    -e  JEA configuration name (default endpoint if omitted)
