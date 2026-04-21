import { createWeb3Modal, defaultWagmiConfig } from 'https://esm.sh/@web3modal/wagmi@5.1.6';
import { mainnet, polygon, base, arbitrum } from 'https://esm.sh/wagmi@2.12.6/chains';
import { reconnect, getAccount, watchAccount } from 'https://esm.sh/@wagmi/core@2.13.6';

const projectId = '910f7a5fc823c671ef990ea38fe5cf94';

const metadata = {
  name: 'StableFX',
  description: 'Onchain Stablecoin FX Trading',
  url: window.location.origin,
  icons: ['https://avatars.githubusercontent.com/u/37784886']
};

const chains = [polygon, base, arbitrum, mainnet];
const config = defaultWagmiConfig({ chains, projectId, metadata });

reconnect(config);

const modal = createWeb3Modal({
  wagmiConfig: config,
  projectId,
  enableAnalytics: false,
  themeMode: 'dark',
  themeVariables: {
    '--w3m-accent': '#7fff00',
    '--w3m-background-color': '#161a1a',
    '--w3m-border-radius-master': '14px',
    '--w3m-font-family': 'DM Mono, monospace'
  }
});

// Override connectWallet globally
window.openWalletModal = function() {
  modal.open();
};

watchAccount(config, {
  onChange(account) {
    if (account.address) {
      window.account = account.address;
      const btn = document.getElementById('walletBtn');
      if (btn) {
        btn.textContent = 'Connected';
        btn.classList.add('connected');
      }
      const addrEl = document.getElementById('walletAddr');
      if (addrEl) {
        addrEl.innerHTML = '<span class="dot"></span> ' +
          account.address.slice(0,6) + '...' + account.address.slice(-4);
      }
      if (window.web3) {
        window.web3.eth.getBalance(account.address).then(bal => {
          const eth = parseFloat(window.web3.utils.fromWei(bal, 'ether'));
          const usd = (eth * 3200).toFixed(2);
          const pv = document.getElementById('portfolioVal');
          const av = document.getElementById('availableSwap');
          const pf = document.getElementById('progressFill');
          if (pv) pv.textContent = '$' + parseFloat(usd).toLocaleString('en-US', {minimumFractionDigits:2});
          if (av) av.textContent = '$' + parseFloat(usd).toLocaleString();
          if (pf) pf.style.width = Math.min((eth/10)*100, 100) + '%';
        });
      }
      ['swapBtn','swapBtn2'].forEach(id => {
        const b = document.getElementById(id);
        if (b) b.textContent = 'Swap Now ⚡';
      });
      if (window.showToast) showToast('✅ Wallet connected!', 'success');
    } else {
      window.account = null;
      const btn = document.getElementById('walletBtn');
      if (btn) { btn.textContent = 'Connect'; btn.classList.remove('connected'); }
      ['swapBtn','swapBtn2'].forEach(id => {
        const b = document.getElementById(id);
        if (b) b.textContent = 'Connect Wallet to Swap';
      });
    }
  }
});
