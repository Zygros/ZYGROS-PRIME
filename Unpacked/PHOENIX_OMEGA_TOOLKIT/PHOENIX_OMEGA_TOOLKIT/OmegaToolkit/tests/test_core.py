from OmegaToolkit.sovereign_toolkit import SovereignToolkit

def test_register_and_execute():
    toolkit = SovereignToolkit()
    toolkit.register("PING", lambda: "PONG")
    assert toolkit.execute("PING") == "PONG"
