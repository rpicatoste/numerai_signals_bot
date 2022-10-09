from argparse import ArgumentParser

from src.orchestration.orchestrator import Orchestrator


if __name__ == "__main__":
    parser = ArgumentParser(description='Numerai Signals bot')
    parser.add_argument('data_cfg_path')
    parser.add_argument('--features_cfg_path', default=None)
    args = parser.parse_args()

    print('Running orchestrator test.')
    orch = Orchestrator(db_cfg_path=args.data_cfg_path,
                        features_cfg_path=args.features_cfg_path)
    orch.run_all()
