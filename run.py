import argparse
from src.process.train_process import process_train 
from src.process.inference_process import inference

def execute_preprocess(path, force=False):
    print(f"Exécution de preprocess sur {path}")
    if force:
        print("Option --force activée")
    process_train(path, force)

def execute_inference(path, benchmark=False):
    print(f"Exécution de inference sur {path}")
    if benchmark:
        print("Benchmark activé")

def parse_command_line():
    parser = argparse.ArgumentParser(description='Parser pour ligne de commande.')
    parser.add_argument('-preprocess', metavar='PREPROCESS_PATH', type=str, help='Chemin pour preprocess')
    parser.add_argument('--force', action='store_true', help='Force l\'exécution de preprocess')
    parser.add_argument('-inference', metavar='INFERENCE_PATH', type=str, help='Chemin pour inference')
    parser.add_argument('-benchmark', action='store_true', help='Activer le benchmark (uniquement avec inference)')
    args = parser.parse_args()

    if args.benchmark and not args.inference:
        parser.error("L'option -benchmark nécessite -inference.")

    return args

def main():
    args = parse_command_line()

    if args.preprocess:
        execute_preprocess(args.preprocess, args.force)

    if args.inference:
        execute_inference(args.inference, args.benchmark)

if __name__ == "__main__":
    main()