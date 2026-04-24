import os, re

path = os.path.expanduser('~/stablefx-app/index.html')
with open(path, 'r') as f:
    html = f.read()

# Remove all old web3 script tags
html = re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/web3[^"]*"[^>]*></script>', '', html)
html = re.sub(r'<script src="https://cdn\.jsdelivr[^"]*"[^>]*></script>', '', html)
html = re.sub(r'<script src="https://unpkg[^"]*"[^>]*></script>', '', html)

# Add all scripts in correct order at top of body
SCRIPTS = '''
<script src="https://cdnjs.cloudflare.com/ajax/libs/web3/1.10.0/web3.min.js"></script>
'''

# Insert right after <body>
html = html.replace('<body>', '<body>' + SCRIPTS)

with open(path, 'w') as f:
    f.write(html)
print("Done!")
