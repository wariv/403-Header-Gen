# 403-Header-Gen

This script generates wordlists of common referer based headers for 403 bypass. It ships with common bypass values and allows for custom values as well.

```
usage: gen403.py [-h] [-o OUTFILE] [-s] [-ch CUSTOM_HEADERS] [-cv CUSTOM_VALUES] [-cp CUSTOM_PORTS] [-sd] [-hf] [-pf] [-u] [-us]

options:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Specify an output file
  -s, --split           Separate headers and values into different files.
  -ch CUSTOM_HEADERS, --custom-headers CUSTOM_HEADERS
                        Specify a file with custom headers.
  -cv CUSTOM_VALUES, --custom-values CUSTOM_VALUES
                        Specify a file with custom values.
  -cp CUSTOM_PORTS, --custom-ports CUSTOM_PORTS
                        Specify a file with custom ports.
  -sd, --skip-default   Skip built-in values and only use custom values. Only if a custom list has been provided
  -hf, --http-force     Ensure https:// is prepended to each value.
  -pf, --port-force     Append port numbers to each value.
  -u, --upper           Force uppercase headers
  -us, --underscore     Replace - with _
```
