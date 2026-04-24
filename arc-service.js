const { AppKit } = require('@circle-fin/app-kit');
const { ViemV2Adapter } = require('@circle-fin/adapter-viem-v2');
const { createWalletClient, custom, http } = require('viem');

const KIT_KEY = 'f8660bfb34f5dcc0699cc84f56702569:e9e7345e7bf13e9dec1eb4d00262e92f';

const ARC_TESTNET = {
  id: 1516,
  name: 'Arc Testnet',
  nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
  rpcUrls: {
    default: { http: ['https://rpc.arc.network'] }
  }
};

function createArcAdapter(walletClient) {
  return new ViemV2Adapter(walletClient, { chain: ARC_TESTNET });
}

function createKit() {
  return new AppKit();
}

module.exports = { createKit, createArcAdapter, ARC_TESTNET, KIT_KEY };
