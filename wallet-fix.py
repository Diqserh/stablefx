import os, re

path = os.path.expanduser('~/stablefx-app/index.html')
with open(path, 'r') as f:
    html = f.read()

# Remove ALL old wallet scripts
html = re.sub(r'<script src="https://unpkg\.com/@walletconnect.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<script type="module".*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'// Fallback for browsers[\s\S]*?</script>', '</script>', html)

# Fix button
html = html.replace('onclick="openWalletModal()"', 'onclick="connectWallet()"')

NEW_WALLET = '''
<script src="https://unpkg.com/@walletconnect/web3-provider@1.8.0/dist/umd/index.min.js"></script>
<script>
async function connectWallet(){
  const btn=document.getElementById('walletBtn');
  btn.innerHTML='<span class="spinner"></span>';
  try{
    // Case 1: MetaMask or injected wallet
    if(window.ethereum){
      const accs=await window.ethereum.request({method:'eth_requestAccounts'});
      window.web3=new Web3(window.ethereum);
      window.account=accs[0];
      walletReady(accs[0]);
      return;
    }
    // Case 2: WalletConnect QR
    const wcp=new WalletConnectProvider.default({
      rpc:{
        1:'https://cloudflare-eth.com',
        137:'https://polygon-rpc.com',
        8453:'https://mainnet.base.org'
      },
      qrcode:true,
      qrcodeModalOptions:{mobileLinks:['metamask','trust','rainbow','coinbase']}
    });
    await wcp.enable();
    window.web3=new Web3(wcp);
    const accs=await window.web3.eth.getAccounts();
    window.account=accs[0];
    walletReady(accs[0]);
    wcp.on('accountsChanged',a=>{window.account=a[0];walletReady(a[0]);});
    wcp.on('disconnect',walletGone);
  }catch(e){
    btn.textContent='Connect';
    showToast('❌ '+e.message,'error');
  }
}

function walletReady(addr){
  const btn=document.getElementById('walletBtn');
  btn.textContent='Connected';
  btn.classList.add('connected');
  document.getElementById('walletAddr').innerHTML='<span class="dot"></span> '+addr.slice(0,6)+'...'+addr.slice(-4);
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
  document.getElementById('walletAddr').innerHTML='<span>—</span>';
  ['swapBtn','swapBtn2'].forEach(id=>{
    const b=document.getElementById(id);
    if(b)b.textContent='Connect Wallet to Swap';
  });
  showToast('👋 Disconnected','');
}
</script>
'''

html = html.replace('</body>', NEW_WALLET + '</body>')
with open(path, 'w') as f:
    f.write(html)
print("Done!")
