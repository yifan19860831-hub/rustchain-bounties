/**
 * RustChain Wallet - Background Service Worker
 * Handles crypto operations, storage, and communication with popup
 */

importScripts('./src/crypto.js', './src/api.js');

// Wallet state
let walletState = {
  unlocked: false,
  currentAddress: null,
  addresses: [],
  nodeUrl: 'https://50.28.86.131',
  lockTimeout: 5 * 60 * 1000 // 5 minutes
};

let lockTimer = null;

// Initialize wallet state from storage
async function initWalletState() {
  try {
    const result = await chrome.storage.local.get(['walletState', 'encryptedKeystores']);
    if (result.walletState) {
      walletState = { ...walletState, ...result.walletState };
    }
  } catch (error) {
    console.error('Error initializing wallet state:', error);
  }
}

// Auto-lock timer
function resetLockTimer() {
  if (lockTimer) {
    clearTimeout(lockTimer);
  }
  
  if (walletState.unlocked) {
    lockTimer = setTimeout(async () => {
      await lockWallet();
    }, walletState.lockTimeout);
  }
}

// Lock wallet
async function lockWallet() {
  walletState.unlocked = false;
  await saveWalletState();
  chrome.runtime.sendMessage({ action: 'walletLocked' }).catch(() => {});
}

// Save wallet state
async function saveWalletState() {
  try {
    await chrome.storage.local.set({ walletState });
  } catch (error) {
    console.error('Error saving wallet state:', error);
  }
}

// Message handler
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  resetLockTimer();
  
  handleMessage(message).then(sendResponse).catch(error => {
    sendResponse({ success: false, error: error.message });
  });
  
  return true; // Keep channel open for async response
});

async function handleMessage(message) {
  switch (message.action) {
    case 'createWallet':
      return await handleCreateWallet(message.password);
    
    case 'importWallet':
      return await handleImportWallet(message.mnemonic, message.password);
    
    case 'unlockWallet':
      return await handleUnlockWallet(message.password);
    
    case 'lockWallet':
      await lockWallet();
      return { success: true };
    
    case 'getBalance':
      return await handleGetBalance();
    
    case 'sendTransfer':
      return await handleSendTransfer(message.to, message.amount, message.memo, message.password);
    
    case 'getTransactionHistory':
      return await handleGetTransactionHistory();
    
    case 'getAddresses':
      return { success: true, addresses: walletState.addresses };
    
    case 'getCurrentAddress':
      return { success: true, address: walletState.currentAddress };
    
    case 'setNodeUrl':
      walletState.nodeUrl = message.url;
      await saveWalletState();
      return { success: true };
    
    case 'getNodeUrl':
      return { success: true, url: walletState.nodeUrl };
    
    case 'isUnlocked':
      return { success: true, unlocked: walletState.unlocked };
    
    default:
      return { success: false, error: 'Unknown action' };
  }
}

async function handleCreateWallet(password) {
  try {
    // Generate mnemonic
    const mnemonic = await RustChainCrypto.generateMnemonic();
    
    // Derive keypair
    const keyPair = await RustChainCrypto.deriveKeyPair(mnemonic);
    
    // Generate address
    const address = await RustChainCrypto.generateAddress(keyPair.publicKey);
    
    // Export private key for storage
    const privateKeyData = await crypto.subtle.exportKey('pkcs8', keyPair.privateKey);
    const publicKeyData = await crypto.subtle.exportKey('raw', keyPair.publicKey);
    
    // Create keystore
    const keystore = {
      mnemonic: mnemonic,
      privateKey: RustChainCrypto.bytesToHex(new Uint8Array(privateKeyData)),
      publicKey: RustChainCrypto.bytesToHex(new Uint8Array(publicKeyData)),
      address: address,
      createdAt: Date.now()
    };
    
    // Encrypt keystore
    const encryptedKeystore = await RustChainCrypto.encryptKeystore(keystore, password);
    
    // Save to storage
    const encryptedKeystores = await getEncryptedKeystores();
    encryptedKeystores[address] = encryptedKeystore;
    await chrome.storage.local.set({ encryptedKeystores });
    
    // Update wallet state
    walletState.addresses.push(address);
    walletState.currentAddress = address;
    walletState.unlocked = true;
    await saveWalletState();
    
    return {
      success: true,
      address: address,
      mnemonic: mnemonic // Show mnemonic once for backup
    };
  } catch (error) {
    console.error('Error creating wallet:', error);
    return { success: false, error: error.message };
  }
}

async function handleImportWallet(mnemonic, password) {
  try {
    // Derive keypair from mnemonic
    const keyPair = await RustChainCrypto.deriveKeyPair(mnemonic);
    
    // Generate address
    const address = await RustChainCrypto.generateAddress(keyPair.publicKey);
    
    // Export keys
    const privateKeyData = await crypto.subtle.exportKey('pkcs8', keyPair.privateKey);
    const publicKeyData = await crypto.subtle.exportKey('raw', keyPair.publicKey);
    
    // Create keystore
    const keystore = {
      mnemonic: mnemonic,
      privateKey: RustChainCrypto.bytesToHex(new Uint8Array(privateKeyData)),
      publicKey: RustChainCrypto.bytesToHex(new Uint8Array(publicKeyData)),
      address: address,
      createdAt: Date.now()
    };
    
    // Encrypt keystore
    const encryptedKeystore = await RustChainCrypto.encryptKeystore(keystore, password);
    
    // Save to storage
    const encryptedKeystores = await getEncryptedKeystores();
    encryptedKeystores[address] = encryptedKeystore;
    await chrome.storage.local.set({ encryptedKeystores });
    
    // Update wallet state
    walletState.addresses.push(address);
    walletState.currentAddress = address;
    walletState.unlocked = true;
    await saveWalletState();
    
    return {
      success: true,
      address: address
    };
  } catch (error) {
    console.error('Error importing wallet:', error);
    return { success: false, error: error.message };
  }
}

async function handleUnlockWallet(password) {
  try {
    if (!walletState.currentAddress) {
      return { success: false, error: 'No wallet found' };
    }
    
    const encryptedKeystores = await getEncryptedKeystores();
    const encryptedKeystore = encryptedKeystores[walletState.currentAddress];
    
    if (!encryptedKeystore) {
      return { success: false, error: 'Wallet not found' };
    }
    
    // Try to decrypt
    await RustChainCrypto.decryptKeystore(encryptedKeystore, password);
    
    walletState.unlocked = true;
    await saveWalletState();
    
    return { success: true };
  } catch (error) {
    console.error('Error unlocking wallet:', error);
    return { success: false, error: 'Invalid password' };
  }
}

async function handleGetBalance() {
  try {
    if (!walletState.currentAddress || !walletState.unlocked) {
      return { success: false, error: 'Wallet locked' };
    }
    
    const api = new RustChainAPI(walletState.nodeUrl);
    const balance = await api.getBalance(walletState.currentAddress);
    
    return { success: true, balance: balance };
  } catch (error) {
    console.error('Error getting balance:', error);
    return { success: false, error: error.message };
  }
}

async function handleSendTransfer(to, amount, memo, password) {
  try {
    if (!walletState.unlocked) {
      return { success: false, error: 'Wallet locked' };
    }
    
    const encryptedKeystores = await getEncryptedKeystores();
    const encryptedKeystore = encryptedKeystores[walletState.currentAddress];
    
    if (!encryptedKeystore) {
      return { success: false, error: 'Wallet not found' };
    }
    
    // Decrypt keystore
    const keystore = await RustChainCrypto.decryptKeystore(encryptedKeystore, password);
    
    // Import private key
    const privateKeyBytes = RustChainCrypto.hexToBytes(keystore.privateKey);
    const keyAlgorithm = { name: 'Ed25519', namedCurve: 'Ed25519' };
    
    const privateKey = await crypto.subtle.importKey(
      'pkcs8',
      privateKeyBytes.buffer,
      keyAlgorithm,
      true,
      ['sign']
    );
    
    // Create transfer data
    const api = new RustChainAPI(walletState.nodeUrl);
    const nonce = await api.getNonce(walletState.currentAddress);
    
    const transferData = {
      from_address: walletState.currentAddress,
      to_address: to,
      amount_rtc: amount,
      memo: memo || '',
      nonce: nonce,
      public_key: keystore.publicKey
    };
    
    // Sign the transfer data
    const message = JSON.stringify({
      from: transferData.from_address,
      to: transferData.to_address,
      amount: transferData.amount_rtc,
      nonce: transferData.nonce
    });
    
    const signature = await RustChainCrypto.signMessage(privateKey, message);
    transferData.signature = signature;
    
    // Send transfer
    const result = await api.sendTransfer(transferData);
    
    return { success: true, result: result };
  } catch (error) {
    console.error('Error sending transfer:', error);
    return { success: false, error: error.message };
  }
}

async function handleGetTransactionHistory() {
  try {
    if (!walletState.currentAddress || !walletState.unlocked) {
      return { success: false, error: 'Wallet locked' };
    }
    
    const api = new RustChainAPI(walletState.nodeUrl);
    const transactions = await api.getTransactionHistory(walletState.currentAddress);
    
    return { success: true, transactions: transactions };
  } catch (error) {
    console.error('Error getting transaction history:', error);
    return { success: false, error: error.message };
  }
}

async function getEncryptedKeystores() {
  try {
    const result = await chrome.storage.local.get(['encryptedKeystores']);
    return result.encryptedKeystores || {};
  } catch (error) {
    console.error('Error getting encrypted keystores:', error);
    return {};
  }
}

// Initialize on startup
initWalletState();
