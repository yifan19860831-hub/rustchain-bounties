# RustChain Integrations

Third-party integrations and connectors for the RustChain network.

## 🔌 Available Integrations

### Beacon Integrations

| Integration | Description | Status |
|-------------|-------------|--------|
| [dong-beacon](dong-beacon/) | Dong's beacon node integration | ✅ Active |
| [energypantry-beacon](energypantry-beacon/) | EnergyPantry beacon connector | ✅ Active |
| [raybot-beacon](raybot-beacon/) | RayBot beacon integration | ✅ Active |

### Developer Tools

| Integration | Description | Status |
|-------------|-------------|--------|
| [postman](postman/) | Postman API collection | ✅ Active |
| [rustchain-mcp](rustchain-mcp/) | Model Context Protocol server | ✅ Active |

## 📦 Postman Collection

The Postman collection provides pre-configured API requests for testing RustChain endpoints.

**Location**: `integrations/postman/rustchain-postman-collection.json`

**Import**: 
1. Open Postman
2. Click Import
3. Select the JSON file
4. Start testing!

## 🔧 MCP Server

The Model Context Protocol (MCP) server enables AI agents to interact with RustChain.

**Features**:
- Natural language API queries
- Automated attestation
- Balance checking
- Network status

## 🚀 Adding New Integrations

1. Create a new directory under `integrations/`
2. Add a README.md with usage instructions
3. Include example code/configuration
4. Test against mainnet or testnet
5. Submit PR with documentation

## 📝 Integration Template

```
integrations/
└── my-integration/
    ├── README.md       # Usage guide
    ├── config.example  # Example configuration
    ├── src/            # Source code
    └── tests/          # Test suite
```

## 🔗 Resources

- [RustChain API Docs](../docs/protocol/)
- [Network Topology](../docs/NETWORK_TOPOLOGY.md)
- [Miner Setup Guide](../docs/MINERS_SETUP_GUIDE.md)

## 📝 License

MIT License - RustChain Community
