import argparse
import logging
import os

from music_generator import EmbMusicGenerator


def main():
    logging.basicConfig(level=logging.INFO)
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--path-to-model", type=str, required=True)
    parser.add_argument("--path-to-samples", type=str, required=True)
    parser.add_argument("--path-to-tokenizer", type=str, required=True)
    parser.add_argument("--random-state", type=int, required=True)
    parser.add_argument("--music-elements-amount", type=int, required=True)
    parser.add_argument("--output-folder", type=str, required=True)
    parser.add_argument("--records-amount", type=int, required=True)
    args: argparse.Namespace = parser.parse_args()
    generator: EmbMusicGenerator = EmbMusicGenerator(args.path_to_model, args.path_to_samples, args.path_to_tokenizer,
                                                     args.random_state)
    for i in range(args.records_amount):
        output_path: str = os.path.join(args.output_folder, f"{i}.mid")
        generator.generate(args.music_elements_amount, output_path)
        logging.info(f"Generated {output_path}")


if __name__ == '__main__':
    main()
