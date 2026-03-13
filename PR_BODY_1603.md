## Summary

This PR implements official Python and JavaScript/TypeScript SDKs for the BoTTube API, enabling developers to programmatically upload, search, comment, and vote on videos.

## Changes

### Python SDK (`sdk/bottube-python/`)
- Complete API client with async-ready design
- Models: Video, Comment
- Methods: upload, search, comment, upvote, downvote, getVideo, getComments
- Comprehensive unit tests with pytest
- Full documentation with examples

### JavaScript SDK (`sdk/bottube-js/`)
- Native Node.js implementation
- TypeScript type definitions included
- Same API surface as Python SDK
- ES6+ modern JavaScript
- JSDoc documentation

## Features

✅ Upload videos (with 2MB limit validation)
✅ Search videos with tag filtering
✅ Add comments to videos
✅ Upvote/Downvote videos
✅ Get video details and comments
✅ Error handling with custom BoTTubeError class
✅ Environment variable support for API keys
✅ Comprehensive examples for both SDKs

## Testing

Both SDKs include unit tests:
- Python: `pytest` (tests/test_bottube.py)
- JavaScript: `jest` (configured in package.json)

## Installation

### Python
```bash
pip install -e sdk/bottube-python
```

### JavaScript
```bash
npm install sdk/bottube-js
```

## Usage Example

```python
from bottube import BoTTube
client = BoTTube(api_key="your_key")
videos = client.search("agent tutorial")
```

```javascript
const { BoTTube } = require('bottube');
const client = new BoTTube({ apiKey: 'your_key' });
const videos = await client.search({ query: 'agent tutorial' });
```

---

**Bounty Claim:**
- Issue: #1603
- Reward: 3 RTC
- Wallet: `RTC4325af95d26d59c3ef025963656d22af638bb96b`
