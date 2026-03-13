pub mod endpoints;
pub mod tls;

use reqwest::blocking::Client;

/// HTTP client for communicating with a RustChain node.
pub struct RustChainClient {
    client: Client,
    base_url: String,
}

impl RustChainClient {
    /// Create a new client for the given node URL.
    /// Accepts self-signed certificates by default.
    pub fn new(base_url: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let client = tls::build_client()?;
        Ok(Self {
            client,
            base_url: base_url.trim_end_matches('/').to_string(),
        })
    }

    /// Get the base URL of the RustChain node.
    ///
    /// Returns the configured node URL without trailing slashes.
    /// This is used for constructing full endpoint URLs.
    ///
    /// # Returns
    ///
    /// A string slice containing the base URL (e.g., "https://node.rustchain.org")
    ///
    /// # Example
    ///
    /// ```
    /// let client = RustChainClient::new("https://node.rustchain.org")?;
    /// assert_eq!(client.base_url(), "https://node.rustchain.org");
    /// ```
    #[allow(dead_code)]
    pub fn base_url(&self) -> &str {
        &self.base_url
    }

    /// Get a reference to the inner reqwest client.
    pub fn inner(&self) -> &Client {
        &self.client
    }

    /// Construct a full URL for a given path.
    pub fn url(&self, path: &str) -> String {
        format!("{}{}", self.base_url, path)
    }
}
