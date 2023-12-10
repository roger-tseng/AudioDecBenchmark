import argparse, os
from codec import load_codec, list_codec
import soundfile as sf
import torch
import torchaudio


def main(args):
    with open(args.filpath, "r") as txt_file:
        filepaths_48k = txt_file.readlines()
    # filepaths_48k = ["../VCTK-Corpus/wav48/p225/p225_001.wav"]
    
    # Remove enclosing speaekr directory from list of strings of paths
    filepaths_16k = map(lambda x: os.path.join(os.path.dirname(os.path.dirname(x)), os.path.basename(x)).replace("wav48", "16k"), filepaths_48k)
    
    for codec_name in list_codec():    
        print(f"Synthesizing dataset with {codec_name}")
        if 'funcodec' in codec_name:
            print(f"Skipping FunCodec-based due to dependency issues...")
            continue

        codec = load_codec(codec_name)
        codec_sr = codec.sampling_rate
        print(f"Sampling rate: {codec_sr}")

        if codec_sr == 16000:
            filepaths = filepaths_16k
        else:
            filepaths = filepaths_48k
            sampler = torchaudio.transforms.Resample(orig_freq=48000, new_freq=codec_sr, dtype=torch.float32)
        
        for path in filepaths:
            path = path.strip()
            data = {}
            data["id"] = path.split("/")[-1].split(".")[0]
            # path = os.path.join(os.path.dirname(os.path.dirname(path)), os.path.basename(path))
            wav, samplerate = sf.read(path)
            if codec_sr != samplerate:
                wav = sampler(torch.from_numpy(wav).float()).numpy()
                samplerate = codec_sr
            
            data["audio"] = {
                "array": wav,
                "sampling_rate": samplerate
                }
            _ = codec.synth(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run resyn.')
    parser.add_argument('--codec', type=str, default="")
    parser.add_argument('--filpath', default="filepaths_48k.txt")
    args = parser.parse_args()
    main(args)