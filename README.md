# Convert RPSL (RFC 2622) to JSON

This tool could be used to parse Routing Policy Specification Language (RPSL)
and dump RPSL objects line-by-line in JSON format. For example, you could use
it to process RIPE database dump files:

    wget https://ftp.ripe.net/ripe/dbase/ripe.db.gz
    cat ripe.db.gz | gunzip | ./rpsl-to-json.py | gzip > ripe.json.gz
