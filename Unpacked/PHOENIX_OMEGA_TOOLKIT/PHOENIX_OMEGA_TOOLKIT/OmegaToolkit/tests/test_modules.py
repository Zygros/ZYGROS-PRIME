from OmegaToolkit.modules import cognitive, technical, temporal

def test_cognitive_analyze():
    out = cognitive.analyze_data("Test_Target")
    assert "Analysis complete" in out

def test_technical_deploy():
    out = technical.deploy_system("v0.0.1")
    assert "deployed to production" in out

def test_temporal_pareto():
    tasks = ["a", "b", "c", "d", "e"]
    split = temporal.pareto_fractal(tasks)
    assert split["top_4_percent"]
    assert split["top_20_percent"]
