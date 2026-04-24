import os, re

path = os.path.expanduser('~/stablefx-app/index.html')
with open(path, 'r') as f:
    html = f.read()

# Remove ALL old wallet scripts
html = re.sub(r'<script src="https://unpkg\.com/@walletconnect[^"]*"[^>]*></script>', '', html)
html = re.sub(r'<script>\s*async function connectWallet[\s\S]*?</script>', '', html)
html = re.sub(r'<script>\s*// Fallback[\s\S]*?</script>', '', html)
html = re.sub(r'<script>\s*if\(window\.ethereum\)[\s\S]*?</script>', '', html)

# Fix button just in case
html = html.replace('onclick="openWalletModal()"', 'onclick="connectWallet()"')

NEW_WALLET = """
<script src="https://cdn.jsdelivr.net/npm/@web3modal/standalone@2.4.1/dist/index.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@walletconnect/sign-client@2.11.2/dist/index.umd.js"></script>
<script>
const PROJECT_ID='910f7a5fc823c671ef990ea38fe5cf94';

async function connectWallet(){
  const btn=document.getElementById('walletBtn');
  btn.innerHTML='<span class="spinner"></span>';

  try{
    // Try injected wallet first (MetaMask, Trust, Brave)
    if(window.ethereum){
      await window.ethereum.request({method:'eth_requestAccounts'});
      window.web3=new Web3(window.ethereum);
      const accs=await window.web3.eth.getAccounts();
      window.account=accs[0];
      walletReady(accs[0]);
      window.ethereum.on('accountsChanged',a=>{
        if(a.length){window.account=a[0];walletReady(a[0]);}
        else walletGone();
      });
      return;
    }

    // No injected wallet — show install options
    btn.textContent='Connect';
    document.getElementById('modalTitle').textContent='Connect Wallet';
    document.getElementById('modalBody').innerHTML=`
      <div style="display:flex;flex-direction:column;gap:12px">
        <a href="https://metamask.app.link/dapp/${window.location.host}" 
           style="display:flex;align-items:center;gap:14px;background:var(--card2);border:1px solid var(--border);border-radius:14px;padding:16px;text-decoration:none;color:var(--text)">
          <span style="font-size:32px">🦊</span>
          <div><div style="font-family:'Syne',sans-serif;font-weight:700">MetaMask</div>
          <div style="font-size:11px;color:var(--muted)">Open in MetaMask browser</div></div>
        </a>
        <a href="https://link.trustwallet.com/open_url?coin_id=60&url=${window.location.href}"
           style="display:flex;align-items:center;gap:14px;background:var(--card2);border:1px solid var(--border);border-radius:14px;padding:16px;text-decoration:none;color:var(--text)">
          <span style="font-size:32px">🛡️</span>
          <div><div style="font-family:'Syne',sans-serif;font-weight:700">Trust Wallet</div>
          <div style="font-size:11px;color:var(--muted)">Open in Trust Wallet browser</div></div>
        </a>
        <a href="https://go.cb-w.com/dapp?cb_url=${window.location.href}"
           style="display:flex;align-items:center;gap:14px;background:var(--card2);border:1px solid var(--border);border-radius:14px;padding:16px;text-decoration:none;color:var(--text)">
          <span style="font-size:32px">💙</span>
          <div><div style="font-family:'Syne',sans-serif;font-weight:700">Coinbase Wallet</div>
          <div style="font-size:11px;color:var(--muted)">Open in Coinbase Wallet browser</div></div>
        </a>
        <div style="text-align:center;font-size:11px;color:var(--muted);padding:8px 0">
          Or copy the URL and open it inside your wallet's browser
        </div>
        <div style="background:var(--card2);border:1px solid var(--border);border-radius:10px;padding:12px;font-size:11px;color:var(--accent);word-break:break-all;text-align:center">
          ${window.location.href}
        </div>
      </div>`;
    document.getElementById('modalOverlay').classList.add('open');

  }catch(e){
    btn.textContent='Connect';
    showToast('❌ '+e.message,'error');
  }
}

function walletReady(addr){
  const btn=document.getElementById('walletBtn');
  btn.textContent='Connected';
  btn.classList.add('connected');
  const addrEl=document.getElementById('walletAddr');
  if(addrEl)addrEl.innerHTML='<span class="dot"></span> '+addr.slice(0,6)+'...'+addr.slice(-4);
  ['swapBtn','swapBtn2'].forEach(id=>{
    const b=document.getElementById(id);
    if(b)b.textContent='Swap Now ⚡';
  });
  showToast('✅ Wallet connected!','success');
  window.web3.eth.getBalance(addr).then(bal=>{
    const eth=parseFloat(window.web3.utils.fromWei(bal,'ether'));
    const usd=(eth*3200).toFixed(2);
    const pv=document.getElementById('portfolioVal');
    const av=document.getElementById('availableSwap');
    const pc=document.getElementById('portfolioChange');
    const pf=document.getElementById('progressFill');
    if(pv)pv.textContent='$'+parseFloat(usd).toLocaleString('en-US',{minimumFractionDigits:2});
    if(av)av.textContent='$'+parseFloat(usd).toLocaleString();
    if(pc)pc.textContent='+2.34% today';
    if(pf)pf.style.width=Math.min((eth/10)*100,100)+'%';
  }).catch(console.error);
}

function walletGone(){
  window.account=null;
  const btn=document.getElementById('walletBtn');
  if(btn){btn.textContent='Connect';btn.classList.remove('connected');}
  const addrEl=document.getElementById('walletAddr');
  if(addrEl)addrEl.innerHTML='<span>—</span>';
  ['swapBtn','swapBtn2'].forEach(id=>{
    const b=document.getElementById(id);
    if(b)b.textContent='Connect Wallet to Swap';
  });
  showToast('👋 Disconnected','');
}
</script>
"""

html = html.replace('</body>', NEW_WALLET + '</body>')
with open(path, 'w') as f:
    f.write(html)
print("Done!")
