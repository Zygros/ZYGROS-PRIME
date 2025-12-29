from OmegaToolkit.sovereign_toolkit import SovereignToolkit
from OmegaToolkit.modules import technical

if __name__ == "__main__":
    omega = SovereignToolkit()
    omega.register("DEPLOY", technical.deploy_system)
    print(omega.execute("DEPLOY", version="v2.0.1"))
