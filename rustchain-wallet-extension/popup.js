/**
 * RustChain Wallet - Popup Script
 * Handles UI interactions and communication with background script
 */

// State
let currentView = 'unlock';
let mnemonicBackup = '';

// Utility functions
function showView(viewId) {
  document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
  document.getElementById(viewId).classList.add('active');
  currentView = viewId;
}

function showStatus(elementId, message, type = 'info') {
  const el = document.getElementById(elementId);
  if (!el) return;
  
  el.className = `status-message ${type}`;
  el.textContent = message;
  el.style.display = 'block';
  
  if (type !== 'error') {
    setTimeout(() => {
      el.style.display = 'none';
    }, 5000);
  }
}

function formatAddress(address) {
  if (!address) return '';
  return `${address.slice(0, 10)}...${address.slice(-10)}`;
}

function formatTime(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;
  
  if (diff < 60000) return 'Just now';
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
  return date.toLocaleDateString();
}

async function sendMessage(message) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(message, response => {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
      } else if (response && response.success) {
        resolve(response);
      } else {
        reject(new Error(response?.error || 'Unknown error'));
      }
    });
  });
}

// Check wallet status on load
async function checkWalletStatus() {
  try {
    const response = await sendMessage({ action: 'isUnlocked' });
    const addressesResponse = await sendMessage({ action: 'getAddresses' });
    
    if (addressesResponse.addresses && addressesResponse.addresses.length > 0) {
      // Wallet exists
      if (response.unlocked) {
        showWalletView();
      } else {
        showView('unlock-view');
      }
    } else {
      // No wallet, show create screen
      showView('create-view');
    }
  } catch (error) {
    console.error('Error checking wallet status:', error);
    showView('create-view');
  }
}

// Show main wallet view
async function showWalletView() {
  showView('wallet-view');
  
  // Load balance and address
  await loadBalance();
  await loadAddress();
  await loadTransactionHistory();
}

async function loadBalance() {
  try {
    const response = await sendMessage({ action: 'getBalance' });
    if (response.success) {
      document.getElementById('balance-display').textContent = response.balance.toFixed(2);
    }
  } catch (error) {
    console.error('Error loading balance:', error);
    document.getElementById('balance-display').textContent = '0.00';
  }
}

async function loadAddress() {
  try {
    const response = await sendMessage({ action: 'getCurrentAddress' });
    if (response.success && response.address) {
      const display = formatAddress(response.address);
      document.getElementById('address-display').textContent = display;
      document.getElementById('receive-address-display').textContent = response.address;
    }
  } catch (error) {
    console.error('Error loading address:', error);
  }
}

async function loadTransactionHistory() {
  try {
    const response = await sendMessage({ action: 'getTransactionHistory' });
    const listEl = document.getElementById('history-list');
    
    if (response.success && response.transactions && response.transactions.length > 0) {
      listEl.innerHTML = response.transactions.map(tx => `
        <div class="transaction-item">
          <div class="tx-info">
            <div class="tx-amount ${tx.from === 'me' ? 'negative' : 'positive'}">
              ${tx.from === 'me' ? '-' : '+'}${tx.amount.toFixed(2)} RTC
            </div>
            <div class="tx-address">${formatAddress(tx.from === 'me' ? tx.to : tx.from)}</div>
            <div class="tx-time">${formatTime(tx.timestamp)}</div>
          </div>
        </div>
      `).join('');
    } else {
      listEl.innerHTML = '<div style="text-align: center; color: #999; padding: 20px;">No transactions yet</div>';
    }
  } catch (error) {
    console.error('Error loading history:', error);
    document.getElementById('history-list').innerHTML = '<div style="text-align: center; color: #999; padding: 20px;">Unable to load transactions</div>';
  }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  checkWalletStatus();
  
  // Tab switching
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const tabName = tab.dataset.tab;
      
      // Update active tab
      tab.parentElement.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      // Update active view
      const parentView = tab.closest('.view');
      const viewId = parentView.id.replace('-view', '');
      document.querySelectorAll(`#${viewId}-tab .view`).forEach(v => v.classList.remove('active'));
      document.getElementById(`${tabName}-tab`).classList.add('active');
      
      // Refresh data if needed
      if (tabName === 'history') {
        loadTransactionHistory();
      }
    });
  });
  
  // Unlock wallet
  document.getElementById('unlock-btn')?.addEventListener('click', async () => {
    const password = document.getElementById('unlock-password').value;
    if (!password) {
      showStatus('unlock-status', 'Please enter password', 'error');
      return;
    }
    
    try {
      const response = await sendMessage({ action: 'unlockWallet', password });
      if (response.success) {
        showWalletView();
      } else {
        showStatus('unlock-status', response.error || 'Invalid password', 'error');
      }
    } catch (error) {
      showStatus('unlock-status', error.message, 'error');
    }
  });
  
  // Show import view
  document.getElementById('import-btn')?.addEventListener('click', () => {
    showView('create-view');
    document.querySelectorAll('.tab').forEach(t => {
      if (t.dataset.tab === 'import') {
        t.click();
      }
    });
  });
  
  // Create wallet
  document.getElementById('create-wallet-btn')?.addEventListener('click', async () => {
    const password = document.getElementById('create-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    if (!password || password.length < 8) {
      showStatus('create-status', 'Password must be at least 8 characters', 'error');
      return;
    }
    
    if (password !== confirmPassword) {
      showStatus('create-status', 'Passwords do not match', 'error');
      return;
    }
    
    try {
      const response = await sendMessage({ action: 'createWallet', password });
      if (response.success) {
        mnemonicBackup = response.mnemonic;
        showBackupView(mnemonicBackup);
      } else {
        showStatus('create-status', response.error || 'Failed to create wallet', 'error');
      }
    } catch (error) {
      showStatus('create-status', error.message, 'error');
    }
  });
  
  // Import wallet
  document.getElementById('import-wallet-btn')?.addEventListener('click', async () => {
    const mnemonic = document.getElementById('import-mnemonic').value.trim();
    const password = document.getElementById('import-password').value;
    
    if (!mnemonic) {
      showStatus('import-status', 'Please enter seed phrase', 'error');
      return;
    }
    
    if (!password || password.length < 8) {
      showStatus('import-status', 'Password must be at least 8 characters', 'error');
      return;
    }
    
    try {
      const response = await sendMessage({ action: 'importWallet', mnemonic, password });
      if (response.success) {
        showWalletView();
      } else {
        showStatus('import-status', response.error || 'Failed to import wallet', 'error');
      }
    } catch (error) {
      showStatus('import-status', error.message, 'error');
    }
  });
  
  // Backup done
  document.getElementById('backup-done-btn')?.addEventListener('click', () => {
    showWalletView();
  });
  
  // Send RTC
  document.getElementById('send-btn')?.addEventListener('click', async () => {
    const address = document.getElementById('send-address').value.trim();
    const amount = parseFloat(document.getElementById('send-amount').value);
    const memo = document.getElementById('send-memo').value.trim();
    const password = document.getElementById('send-password').value;
    
    if (!address || !address.startsWith('RTC')) {
      showStatus('send-status', 'Invalid recipient address', 'error');
      return;
    }
    
    if (!amount || amount <= 0) {
      showStatus('send-status', 'Invalid amount', 'error');
      return;
    }
    
    if (!password) {
      showStatus('send-status', 'Please enter password', 'error');
      return;
    }
    
    try {
      showStatus('send-status', 'Sending transaction...', 'info');
      const response = await sendMessage({ 
        action: 'sendTransfer', 
        to: address, 
        amount, 
        memo, 
        password 
      });
      
      if (response.success) {
        showStatus('send-status', 'Transaction sent successfully!', 'success');
        // Clear form
        document.getElementById('send-address').value = '';
        document.getElementById('send-amount').value = '';
        document.getElementById('send-memo').value = '';
        document.getElementById('send-password').value = '';
        // Refresh balance
        setTimeout(() => loadBalance(), 2000);
      } else {
        showStatus('send-status', response.error || 'Failed to send', 'error');
      }
    } catch (error) {
      showStatus('send-status', error.message, 'error');
    }
  });
  
  // Copy address
  document.getElementById('copy-address-btn')?.addEventListener('click', async () => {
    const response = await sendMessage({ action: 'getCurrentAddress' });
    if (response.success) {
      await navigator.clipboard.writeText(response.address);
      showStatus('send-status', 'Address copied!', 'success');
    }
  });
  
  document.getElementById('copy-receive-btn')?.addEventListener('click', async () => {
    const address = document.getElementById('receive-address-display').textContent;
    await navigator.clipboard.writeText(address);
    showStatus('send-status', 'Address copied!', 'success');
  });
  
  // Save node URL
  document.getElementById('save-node-btn')?.addEventListener('click', async () => {
    const url = document.getElementById('node-url').value.trim();
    if (!url) {
      showStatus('send-status', 'Invalid node URL', 'error');
      return;
    }
    
    try {
      const response = await sendMessage({ action: 'setNodeUrl', url });
      if (response.success) {
        showStatus('send-status', 'Node URL saved!', 'success');
      }
    } catch (error) {
      showStatus('send-status', error.message, 'error');
    }
  });
  
  // Lock wallet
  document.getElementById('lock-wallet-btn')?.addEventListener('click', async () => {
    await sendMessage({ action: 'lockWallet' });
    showView('unlock-view');
  });
  
  // Export seed
  document.getElementById('export-seed-btn')?.addEventListener('click', async () => {
    alert('For security, please check the background script storage or re-import your wallet to view the seed phrase.');
  });
});

function showBackupView(mnemonic) {
  const words = mnemonic.split(' ');
  const container = document.getElementById('mnemonic-words');
  container.innerHTML = words.map((word, i) => 
    `<div class="mnemonic-word">${i + 1}. ${word}</div>`
  ).join('');
  
  showView('backup-view');
}

// Listen for wallet lock events
chrome.runtime.onMessage.addListener((message) => {
  if (message.action === 'walletLocked' && currentView === 'wallet') {
    showView('unlock-view');
  }
});
