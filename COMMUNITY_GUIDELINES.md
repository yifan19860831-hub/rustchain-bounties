# RustChain Community Guidelines

Welcome to the RustChain community! These guidelines ensure our community remains welcoming, productive, and inclusive for all participants.

## 🎯 Our Mission

RustChain is building a decentralized, hardware-attested mining ecosystem using Rust. We value:
- **Technical excellence** - Clean, efficient, well-documented code
- **Transparency** - Open development and clear communication
- **Inclusivity** - Welcoming contributors of all backgrounds and skill levels
- **Security** - Responsible handling of vulnerabilities and user data

## 📋 Code of Conduct

### Expected Behavior

- **Be respectful** - Treat all community members with dignity and respect
- **Be constructive** - Offer helpful feedback and accept criticism gracefully
- **Be inclusive** - Welcome contributors regardless of experience level, background, or identity
- **Be collaborative** - Help others, share knowledge, and work together
- **Be professional** - Keep discussions focused on technical topics

### Unacceptable Behavior

- Harassment, discrimination, or offensive language
- Personal attacks, insults, or trolling
- Spam, self-promotion without contribution, or off-topic advertising
- Posting sensitive information (API keys, private data, security vulnerabilities) publicly
- Disruptive behavior that derails discussions

### Reporting Issues

If you experience or witness unacceptable behavior:
1. **Document the incident** - Save screenshots or links
2. **Contact maintainers** - Reach out to @Scottcjn or project maintainers via DM
3. **Be specific** - Provide context and what resolution you're seeking

All reports will be handled confidentially and promptly.

## 💬 Communication Channels

| Channel | Purpose | Guidelines |
|---------|---------|------------|
| **GitHub Issues** | Bug reports, feature requests, bounties | Search before posting, use templates, be specific |
| **GitHub Discussions** | General questions, ideas, show-and-tell | Keep on-topic, be respectful |
| **Pull Requests** | Code contributions | Follow PR template, respond to reviews |
| **Discord/Forum** | Real-time chat, community support | Use appropriate channels, avoid @everyone |

## 🤝 Contributing

### Getting Started

1. **Read the docs** - Start with [README.md](README.md) and project documentation
2. **Find an issue** - Look for `good first issue`, `help wanted`, or bounty issues
3. **Fork and branch** - Create a feature branch from `main`
4. **Make changes** - Follow code style and add tests
5. **Submit PR** - Use the PR template and link related issues

### Pull Request Guidelines

- **One feature per PR** - Keep changes focused and atomic
- **Write clear descriptions** - Explain what, why, and how
- **Add tests** - Ensure code quality and prevent regressions
- **Follow code style** - Run `cargo fmt` and `cargo clippy` for Rust projects
- **Respond to feedback** - Address review comments promptly

### Code Style

#### Rust Projects
```bash
# Format code
cargo fmt

# Run linter
cargo clippy -- -D warnings

# Run tests
cargo test
```

#### Python Projects
```bash
# Format code
black .

# Run linter
flake8 .

# Run tests
pytest
```

### Documentation

- **Comments** - Explain _why_, not _what_ (code should be self-documenting)
- **README** - Include installation, usage, examples, and troubleshooting
- **API docs** - Document public functions, parameters, and return values
- **Examples** - Provide working code samples for common use cases

## 🏆 Bounty Program

### How It Works

1. **Find a bounty issue** - Look for issues labeled `bounty` with RTC rewards
2. **Comment to claim** - Indicate you're working on it (first-come, first-served)
3. **Submit your work** - Create a PR referencing the issue
4. **Get reviewed** - Maintainers verify completion
5. **Receive reward** - RTC tokens transferred upon acceptance

### Bounty Guidelines

- **Quality over speed** - Well-tested, documented work gets priority
- **Communication** - Update the issue if you're stuck or need help
- **Original work** - No AI-generated code without significant human review
- **One bounty at a time** - Complete current bounties before claiming new ones

### Valid Reasons for Rejection

- Code doesn't compile or tests fail
- Missing documentation or examples
- Doesn't fully meet requirements
- Plagiarized or AI-generated without disclosure
- Security vulnerabilities introduced

## 🔒 Security

### Reporting Vulnerabilities

**DO NOT** report security issues in public GitHub issues.

Instead:
1. **DM the maintainer** - Contact @Scottcjn directly on GitHub
2. **Provide details** - Include reproduction steps and impact assessment
3. **Allow time for fix** - Give maintainers 7-30 days to address before disclosure

### Security Best Practices

- Never commit API keys, passwords, or private keys
- Use environment variables for sensitive configuration
- Review dependencies for known vulnerabilities
- Follow principle of least privilege in code design

## 📞 Getting Help

- **Documentation** - Check existing docs first
- **Search issues** - Your question may already be answered
- **Ask clearly** - Provide context, what you tried, and expected vs actual results
- **Be patient** - Maintainers are volunteers with limited availability

## 🌟 Recognition

We appreciate all contributions:
- **Contributors** - Listed in CONTRIBUTORS.md and release notes
- **Top contributors** - Featured in community highlights
- **Bounty hunters** - RTC rewards and public recognition
- **First-timers** - Special welcome and mentorship

## 📝 Enforcement

Violations of these guidelines may result in:
1. **Warning** - Private message explaining the issue
2. **Temporary suspension** - Time-limited restriction from community
3. **Permanent ban** - For severe or repeated violations

Enforcement is at the discretion of project maintainers.

## 🔄 Updates

These guidelines may be updated as the community grows. Changes will be:
- Announced in GitHub Discussions
- Documented in the commit history
- Applied fairly to all community members

---

## Quick Reference

✅ **DO:**
- Be kind and respectful
- Help newcomers
- Write tests and documentation
- Report bugs clearly
- Respect maintainers' time

❌ **DON'T:**
- Harass or discriminate
- Spam or self-promote excessively
- Post sensitive information publicly
- Submit low-quality or plagiarized work
- Expect immediate responses

---

**Last Updated:** March 2026

**Questions?** Open a GitHub Discussion or contact @Scottcjn.

**License:** This document is available under the same license as RustChain (MIT).
