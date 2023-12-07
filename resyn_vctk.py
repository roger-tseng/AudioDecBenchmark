import argparse, os
from codec import load_codec, list_codec
import soundfile as sf


def main(args):
    with open(args.filpath, "r") as txt_file:
        filepaths = txt_file.readlines()

    for codec_name in list_codec():    
        print(f"Synthesizing dataset with {codec_name}")
        codec = load_codec(codec_name)
        
        for path in filepaths:
            path = path.strip()
            data = {}
            data["id"] = path.split("/")[-1].split(".")[0]
            # path = os.path.join(os.path.dirname(os.path.dirname(path)), os.path.basename(path))
            wav, samplerate = sf.read(path)
            data["audio"] = {
                "array": wav,
                "sampling_rate": samplerate
                }
            _ = codec.synth(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run resyn.')
    parser.add_argument('--codec', type=str, default="")
    parser.add_argument('--filpath', default="/media/hbwu/12TB/PublicData/VCTK-Corpus/local/file_paths.txt")
    args = parser.parse_args()
    main(args)