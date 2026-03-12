/**
 * RustChain Wallet - API Client
 * Communicates with RustChain node for balance, transfers, and transaction history
 */

class RustChainAPI {
  constructor(nodeUrl = 'https://50.28.86.131') {
    this.baseUrl = nodeUrl;
  }

  /**
   * Get wallet balance
   * GET /wallet/balance?miner_id={wallet}
   */
  async getBalance(address) {
    try {
      const response = await fetch(`${this.baseUrl}/wallet/balance?miner_id=${encodeURIComponent(address)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.balance || 0;
    } catch (error) {
      console.error('Error fetching balance:', error);
      throw error;
    }
  }

  /**
   * Send signed transfer
   * POST /wallet/transfer/signed
   */
  async sendTransfer(transferData) {
    try {
      const response = await fetch(`${this.baseUrl}/wallet/transfer/signed`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(transferData)
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending transfer:', error);
      throw error;
    }
  }

  /**
   * Get transaction history for an address
   */
  async getTransactionHistory(address, limit = 20) {
    try {
      // Note: Adjust endpoint based on actual RustChain API
      const response = await fetch(`${this.baseUrl}/wallet/transactions?address=${encodeURIComponent(address)}&limit=${limit}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.transactions || [];
    } catch (error) {
      console.error('Error fetching transactions:', error);
      // Return mock data for development
      return this.getMockTransactions(address);
    }
  }

  /**
   * Get current nonce for an address
   */
  async getNonce(address) {
    try {
      const response = await fetch(`${this.baseUrl}/wallet/nonce?address=${encodeURIComponent(address)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.nonce || Date.now();
    } catch (error) {
      // Fallback to timestamp-based nonce
      return Date.now();
    }
  }

  /**
   * Mock transaction data for development
   */
  getMockTransactions(address) {
    return [
      {
        hash: '0x' + Array(64).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
        from: address,
        to: 'RTC' + Array(40).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
        amount: 10.5,
        timestamp: Date.now() - 3600000,
        status: 'confirmed',
        memo: 'Test transaction'
      },
      {
        hash: '0x' + Array(64).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
        from: 'RTC' + Array(40).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
        to: address,
        amount: 25.0,
        timestamp: Date.now() - 86400000,
        status: 'confirmed',
        memo: 'Received payment'
      }
    ];
  }

  /**
   * Set node URL
   */
  setNodeUrl(url) {
    this.baseUrl = url;
  }

  /**
   * Get current node URL
   */
  getNodeUrl() {
    return this.baseUrl;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = RustChainAPI;
}
