from OmegaToolkit.modules import entropy

def test_entropy_handle_failure():
    try:
        raise RuntimeError("boom")
    except RuntimeError as e:
        summary = entropy.handle_failure("test_context", e)
        assert "Post-mortem" in summary
