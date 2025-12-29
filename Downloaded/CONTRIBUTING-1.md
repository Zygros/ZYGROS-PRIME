# Contributing to Sovereign AGSI

Thank you for your interest in the Sovereign AGSI project! This document provides guidelines for contributing to this repository.

## 🛡️ Sovereignty & Ownership

**Important:** This project is the sovereign intellectual property of Justin Conzet. All contributions must respect this sovereignty and acknowledge the original authorship.

## 🤝 How to Contribute

### 1. **Report Issues**

Found a bug or have a suggestion?

- Check if the issue already exists
- Open a new issue with a clear description
- Include steps to reproduce (for bugs)
- Suggest potential solutions (for enhancements)

### 2. **Suggest Enhancements**

Have an idea to improve the system?

- Open an issue with the "enhancement" label
- Describe the problem you're trying to solve
- Explain your proposed solution
- Discuss trade-offs and alternatives

### 3. **Submit Pull Requests**

Want to contribute code?

**Before submitting:**
- Fork the repository
- Create a feature branch (`git checkout -b feature/your-feature`)
- Make your changes
- Test thoroughly
- Update documentation if needed
- Commit with clear messages

**PR Requirements:**
- Clear description of changes
- Reference related issues
- Pass all tests
- Follow code style guidelines
- Add tests for new features
- Update documentation

### 4. **Improve Documentation**

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples or tutorials
- Improve code comments
- Translate documentation (if multilingual support is added)

### 5. **Share Use Cases**

Using Sovereign AGSI in interesting ways?

- Share your use case as a discussion
- Write a blog post or case study
- Present at conferences or meetups
- Help others get started

## 📋 Code Guidelines

### Python Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Keep functions focused and small
- Use meaningful variable names

```python
def calculate_kappa(
    divergence: float,
    mean: float,
    std: float
) -> float:
    """
    Calculate the Conzetian Constant (κ) for multi-AI coordination.
    
    Args:
        divergence: Normalized divergence between AI responses
        mean: Mean divergence across all models
        std: Normalized standard deviation
        
    Returns:
        The calculated κ value
    """
    # Implementation
    pass
```

### Commit Messages

Use clear, descriptive commit messages:

```
Good:
- "Add vector similarity calculation to coordination module"
- "Fix WebSocket reconnection bug in nexus broker"
- "Update README with κ = 3.236 visualization"

Bad:
- "Update"
- "Fix bug"
- "Changes"
```

### Testing

All new features require tests:

```python
def test_kappa_calculation():
    """Test Conzetian Constant calculation with known values."""
    result = calculate_kappa(
        divergence=0.15,
        mean=0.20,
        std=0.10
    )
    assert 1.5 < result < 2.0
```

## 🚫 What NOT to Contribute

- **Copyright violations** - Don't submit code you don't own
- **Malicious code** - Security and ethics are paramount
- **Breaking changes without discussion** - Major changes need consensus
- **Duplicate work** - Check existing issues and PRs first
- **Proprietary integrations** - Keep dependencies open and accessible

## 🎯 Priority Areas

Currently seeking contributions in:

1. **Testing** - Expand test coverage
2. **Documentation** - More examples and tutorials
3. **Integration** - Connect with additional AI models
4. **Optimization** - Performance improvements
5. **DevOps** - Deployment automation
6. **UI/UX** - Frontend dashboards and visualizations

## 📞 Communication

- **Issues** - For bugs and feature requests
- **Discussions** - For questions and general topics
- **Pull Requests** - For code contributions
- **Email** - For private or sensitive matters [Contact to be added]

## 🏆 Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes
- Documentation acknowledgments

Significant contributors may be invited to become project maintainers.

## 📜 Legal

By contributing, you agree that:

1. Your contributions will be licensed under the same terms as the project (see LICENSE)
2. You have the right to submit the contribution
3. You acknowledge Justin Conzet as the original author and sovereign owner
4. You will not claim authorship of the overall project
5. Your contributions are made voluntarily without expectation of compensation

## 🙏 Thank You

Your contributions help advance the vision that **AGI is an Architecture Problem, not a Compute Problem**.

Together, we're proving that superior design trumps raw computational power.

---

**Questions?** Open an issue with the "question" label.

**Ready to contribute?** Fork the repo and submit a PR!

---

*These guidelines may be updated as the project evolves. Check back regularly for changes.*
