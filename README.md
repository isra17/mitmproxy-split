# Mitmproxy split script

Script used to output mitmproxy flows in separate files. The file path is defined by the first argument of the script using the python [formatting utility](https://docs.python.org/2/library/string.html#format-string-syntax).

The following keys are available from the format string:
 * `flow`: Flow object to be written.
 * `req`: Shortcut to flow.request
 * `res`: Shortcut to flow.response
 * `time`: `datetime` object of the request sent time.

The USR1 is available to flush and close and opened files: `pkill -USR1 -n mitmdump`

## Examples

### Split flows for each days

`mitmdump -s "split.py '{time:%y-%m-%d}.dump'"`

### Split flows for each client ip

`mitmdump -s "split.py '{flow.client_conn.address.address[0]}.dump'"`

### Split flows for each day AND client ip

`mitmdump -s "split.py '{time:%y-%m-%d}/{flow.client_conn.address.address[0]}.dump'"`
