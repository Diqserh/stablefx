import re, os

path = os.path.expanduser('~/stablefx-app/index.html')
with open(path, 'r') as f:
    html = f.read()

# Replace old wallet button onclick
html = html.replace('onclick="openWalletModal()"', 'onclick="connectWallet()"')
html = html.replace('onclick="connectWallet()"', 'onclick="connectWallet()"')

# Add WalletConnect script before </body>
wc_script = '''
<script src="https://unpkg.com/@walletconnect/web3-provider@1.8.0/dist/umd/index.min.js"></script>
<script>
const WC_PROJECT_ID = '910f7a5fc823c671ef990ea38fe5cf94';

async function connectWallet() {
  const btn = document.getElementById('walletBtn');
  btn.innerHTML = '<span class="spinner"></span>';

  try {
    // Try MetaMask / injected wallet first
    if (window.ethereum) {
      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      window.account = accounts[0];
      window.web3 = new Web3(window.ethereum);
      onWalletConnected(window.account);
      return;
    }

    // Fallback to WalletConnect
    const provider = new WalletConnectProvider.default({
      projectId: WC_PROJECT_ID,
      rpc: {
        137: 'https://polygon-rpc.com',
        8453: 'https://mainnet.base.org',
        42161: 'https://arb1.arbitrum.io/rpc',
        1: 'https://cloudflare-eth.com'
      },
      qrcode: true
    });

    await provider.enable();
    window.web3 = new Web3(provider);
    const accounts = await window.web3.eth.getAccounts();
    window.account = accounts[0];
    onWalletConnected(window.account);

    provider.on('accountsChanged', (accs) => {
      window.account = accs[0];
      onWalletConnected(window.account);
    });

    provider.on('disconnect', () => {
      onWalletDisconnected();
    });

  } catch(e) {
    btn.textContent = 'Connect';
    showToast('❌ ' + e.message, 'error');
  }
}

function onWalletConnected(address) {
  const btn = document.getElementById('walletBtn');
  btn.textContent = 'Connected';
  btn.classList.add('connected');

  const addrEl = document.getElementById('walletAddr');
  if (addrEl) {
    addrEl.innerHTML = '<span class="dot"></span> ' +
      address.slice(0,6) + '...' + address.slice(-4);
  }

  ['swapBtn','swapBtn2'].forEach(id => {
    const b = document.getElementById(id);
    if (b) b.textContent = 'Swap Now ⚡';
  });

  showToast('✅ Wallet connected!', 'success');

  if (window.web3) {
    window.web3.eth.getBalance(address).then(bal => {
      const eth = parseFloat(window.web3.utils.fromWei(bal, 'ether'));
      const usd = (eth * 3200).toFixed(2);
      const pv = document.getElementById('portfolioVal');
      const av = document.getElementById('availableSwap');
      const pc = document.getElementById('portfolioChange');
      const pf = document.getElementById('progressFill');
      if (pv) pv.textContent = '$' + parseFloat(usd).toLocaleString('en-US',{minimumFractionDigits:2});
      if (av) av.textContent = '$' + parseFloat(usd).toLocaleString();
      if (pc) pc.textContent = '+2.34% today';
      if (pf) pf.style.width = Math.min((eth/10)*100,100) + '%';
    }).catch(console.error);
  }
}

function onWalletDisconnected() {
  window.account = null;
  const btn = document.getElementById('walletBtn');
  if (btn) { btn.textContent = 'Connect'; btn.classList.remove('connected'); }
  const addrEl = document.getElementById('walletAddr');
  if (addrEl) addrEl.innerHTML = '<span>—</span>';
  ['swapBtn','swapBtn2'].forEach(id => {
    const b = document.getElementById(id);
    if (b) b.textContent = 'Connect Wallet to Swap';
  });
  showToast('👋 Wallet disconnected', '');
}
</script>
'''

# Remove old walletconnect script tag if present
html = re.sub(r'<script type="module" src="walletconnect\.js"></script>', '', html)
# Remove old fallback script blocks
html = re.sub(r'<script>\s*// Fallback for browsers.*?</script>', '', html, flags=re.DOTALL)

# Insert before </body>
html = html.replace('</body>', wc_script + '</body>')

with open(path, 'w') as f:
    f.write(html)
print("Done!")
