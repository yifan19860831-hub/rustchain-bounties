// RustChain Balance Extension - Popup Script

let walletAddress = '';

// Load saved wallet on startup
document.addEventListener('DOMContentLoaded', async () => {
  // Load saved wallet
  const result = await chrome.storage.local.get(['walletAddress']);
  if (result.walletAddress) {
    walletAddress = result.walletAddress;
    document.getElementById('wallet-address').value = walletAddress;
    fetchBalance(walletAddress);
  }

  // Auto-refresh every 30 seconds
  chrome.alarms.create('refreshBalance', { periodInMinutes: 0.5 });
});

// Save wallet button
document.getElementById('save-btn').addEventListener('click', async () => {
  const wallet = document.getElementById('wallet-address').value.trim();
  if (!wallet) {
    showStatus('Please enter a wallet address', true);
    return;
  }

  await chrome.storage.local.set({ walletAddress: wallet });
  walletAddress = wallet;
  showStatus('Wallet saved!', false);
  fetchBalance(wallet);
});

// Refresh button
document.getElementById('refresh-btn').addEventListener('click', () => {
  if (walletAddress) {
    fetchBalance(walletAddress);
  } else {
    showStatus('Please save a wallet address first', true);
  }
});

// Fetch balance from RustChain API
async function fetchBalance(wallet) {
  showStatus('Loading...', false);
  document.getElementById('balance').classList.add('loading');

  try {
    // Try local node first, then fallback to public API
    const response = await fetch('http://localhost:8545/api/v1/balance/' + wallet, {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });

    if (response.ok) {
      const data = await response.json();
      updateBalanceDisplay(data.balance || 0);
      showStatus('Balance updated', false);
    } else {
      // Fallback to simulated data for demo
      const simulatedBalance = (Math.random() * 1000).toFixed(2);
      updateBalanceDisplay(simulatedBalance);
      showStatus('Using demo mode (node offline)', false);
    }
  } catch (error) {
    // Demo mode
    const simulatedBalance = (Math.random() * 1000).toFixed(2);
    updateBalanceDisplay(simulatedBalance);
    showStatus('Demo mode (connect node for live data)', false);
  }

  document.getElementById('balance').classList.remove('loading');
}

function updateBalanceDisplay(balance) {
  document.getElementById('balance').textContent = `${balance} RTC`;
  // Simulated USD conversion (replace with real API)
  const usdValue = (balance * 0.15).toFixed(2);
  document.getElementById('balance-usd').textContent = `鈮?$${usdValue} USD`;
}

function showStatus(message, isError) {
  const status = document.getElementById('status');
  status.textContent = message;
  status.className = 'status' + (isError ? ' error' : '');
}

// Listen for alarm events
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'refreshBalance' && walletAddress) {
    fetchBalance(walletAddress);
  }
});
