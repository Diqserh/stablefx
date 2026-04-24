const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(__dirname));

const KIT_KEY = process.env.KIT_KEY || 'f8660bfb34f5dcc0699cc84f56702569:e9e7345e7bf13e9dec1eb4d00262e92f';

// FX Rates API
app.get('/api/rates', (req, res) => {
  res.json({
    'USDC/EURC': 0.9245,
    'EURC/USDC': 1.0817,
    'USDC/GBPC': 0.7923,
    'GBPC/USDC': 1.2622,
    'USDC/USDT': 1.0001,
    'USDT/USDC': 0.9999,
    'EURC/GBPC': 0.8571,
    'GBPC/EURC': 1.1667
  });
});

// ARC swap quote endpoint
app.post('/api/arc/quote', async (req, res) => {
  try {
    const { tokenIn, tokenOut, amountIn } = req.body;
    const response = await fetch(
      `https://api.arc.network/v1/swap/quote?tokenIn=${tokenIn}&tokenOut=${tokenOut}&amountIn=${amountIn}&chain=Arc_Testnet`,
      { headers: { 'X-Kit-Key': KIT_KEY, 'Content-Type': 'application/json' } }
    );
    const data = await response.json();
    res.json(data);
  } catch(e) {
    res.status(500).json({ error: e.message });
  }
});

// ARC swap execute endpoint
app.post('/api/arc/swap', async (req, res) => {
  try {
    const { tokenIn, tokenOut, amountIn, walletAddress } = req.body;
    const response = await fetch(
      'https://api.arc.network/v1/swap/execute',
      {
        method: 'POST',
        headers: { 'X-Kit-Key': KIT_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: { chain: 'Arc_Testnet', address: walletAddress },
          tokenIn, tokenOut, amountIn,
          config: { kitKey: KIT_KEY }
        })
      }
    );
    const data = await response.json();
    res.json(data);
  } catch(e) {
    res.status(500).json({ error: e.message });
  }
});

// ARC bridge endpoint
app.post('/api/arc/bridge', async (req, res) => {
  try {
    const { fromChain, toChain, amount, walletAddress } = req.body;
    const response = await fetch(
      'https://api.arc.network/v1/bridge/execute',
      {
        method: 'POST',
        headers: { 'X-Kit-Key': KIT_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: { chain: fromChain, address: walletAddress },
          to: { chain: toChain, address: walletAddress },
          amount, token: 'USDC',
          config: { kitKey: KIT_KEY }
        })
      }
    );
    const data = await response.json();
    res.json(data);
  } catch(e) {
    res.status(500).json({ error: e.message });
  }
});

// ARC send endpoint
app.post('/api/arc/send', async (req, res) => {
  try {
    const { to, amount, token, walletAddress } = req.body;
    const response = await fetch(
      'https://api.arc.network/v1/send',
      {
        method: 'POST',
        headers: { 'X-Kit-Key': KIT_KEY, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: { chain: 'Arc_Testnet', address: walletAddress },
          to, amount, token,
          config: { kitKey: KIT_KEY }
        })
      }
    );
    const data = await response.json();
    res.json(data);
  } catch(e) {
    res.status(500).json({ error: e.message });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', kit: 'arc-app-kit', time: new Date() });
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => console.log('StableFX + ARC App Kit on port ' + PORT));
