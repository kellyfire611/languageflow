import os
import re
import shutil
from enum import Enum
from typing import Union, List

from tabulate import tabulate

from languageflow.data import CategorizedCorpus, Sentence, Corpus, Label
from languageflow.datasets import REPO
from languageflow.file_utils import cached_path, CACHE_ROOT
from pathlib import Path
import zipfile

MISS_URL_ERROR = "Caution:\n  With closed license dataset, you must provide URL to download"
SAMPLE_CACHE_ROOT = Path(__file__).parent.absolute() / "data"


class NLPData(Enum):
    AIVIVN2019_SA = "aivivn2019_sa"
    AIVIVN2019_SA_SAMPLE = "aivivn2019_sa_sample"


class DataFetcher:

    @staticmethod
    def download_data(data, url):
        if data not in REPO:
            print(f"No matching distribution found for '{data}'")
            return

        filepath = REPO[data]["filepath"]
        cache_dir = REPO[data]["cache_dir"]
        filepath = Path(CACHE_ROOT) / cache_dir / filepath
        if Path(filepath).exists():
            print(f"Data is already existed: '{data}' in {filepath}")
            return

        if data == "VNESES":
            url = "https://www.dropbox.com/s/m4agkrbjuvnq4el/VNESEcorpus.txt?dl=1"
            cached_path(url, cache_dir=cache_dir)
            shutil.move(Path(CACHE_ROOT) / cache_dir / "VNESEcorpus.txt?dl=1",
                        Path(CACHE_ROOT) / cache_dir / filepath)

        if data == "VNTQ_SMALL":
            url = "https://www.dropbox.com/s/b0z17fa8hm6u1rr/VNTQcorpus-small.txt?dl=1"
            cached_path(url, cache_dir=cache_dir)
            shutil.move(Path(CACHE_ROOT) / cache_dir / "VNTQcorpus-small.txt?dl=1",
                        Path(CACHE_ROOT) / cache_dir / filepath)

        if data == "VNTQ_BIG":
            url = "https://www.dropbox.com/s/t4z90vs3qhpq9wg/VNTQcorpus-big.txt?dl=1"
            cached_path(url, cache_dir=cache_dir)
            shutil.move(Path(CACHE_ROOT) / cache_dir / "VNTQcorpus-big.txt?dl=1",
                        Path(CACHE_ROOT) / cache_dir / filepath)

        if data == "VNTC":
            url = "https://www.dropbox.com/s/4iw3xtnkd74h3pj/VNTC.zip?dl=1"
            cached_path(url, cache_dir=cache_dir)
            filepath = Path(CACHE_ROOT) / cache_dir / "VNTC.zip?dl=1"
            cache_folder = Path(CACHE_ROOT) / cache_dir
            zip = zipfile.ZipFile(filepath)
            zip.extractall(cache_folder)
            os.remove(filepath)

        if data == "VLSP2013-WTK":
            if not url:
                print(f"\n{MISS_URL_ERROR}")
                return
            cached_path(url, cache_dir=cache_dir)
            filepath = Path(CACHE_ROOT) / cache_dir / "VLSP2013-WTK.zip?dl=1"
            cache_folder = Path(CACHE_ROOT) / cache_dir
            zip = zipfile.ZipFile(filepath)
            zip.extractall(cache_folder)
            os.remove(filepath)

        if data == "VLSP2013-POS":
            if not url:
                print(f"\n{MISS_URL_ERROR}")
                return
            cached_path(url, cache_dir=cache_dir)
            filepath = Path(CACHE_ROOT) / cache_dir / "VLSP2013-POS.zip?dl=1"
            cache_folder = Path(CACHE_ROOT) / cache_dir
            zip = zipfile.ZipFile(filepath)
            zip.extractall(cache_folder)
            os.remove(filepath)

        if data == "VTB-CHUNK":
            if not url:
                print(f"\n{MISS_URL_ERROR}")
                return
            cached_path(url, cache_dir=cache_dir)
            filepath = Path(CACHE_ROOT) / cache_dir / "VTB-CHUNK.zip?dl=1"
            cache_folder = Path(CACHE_ROOT) / cache_dir
            zip = zipfile.ZipFile(filepath)
            zip.extractall(cache_folder)
            os.remove(filepath)

        if data == "VLSP2016-NER":
            if not url:
                print(f"\n{MISS_URL_ERROR}")
                return
            cached_path(url, cache_dir=cache_dir)
            filepath = Path(CACHE_ROOT) / cache_dir / "VLSP2016-NER.zip?dl=1"
            cache_folder = Path(CACHE_ROOT) / cache_dir
            zip = zipfile.ZipFile(filepath)
            zip.extractall(cache_folder)
            os.remove(filepath)

        if data == "VLSP2018-NER":
            if not url:
                print(f"\n{MISS_URL_ERROR}")
                return
            cached_path(url, cache_dir=cache_dir)
            filepath = Path(CACHE_ROOT) / cache_dir / "VLSP2018-NER.zip?dl=1"
            cache_folder = Path(CACHE_ROOT) / cache_dir
            zip = zipfile.ZipFile(filepath)
            zip.extractall(cache_folder)
            os.remove(filepath)

        if data == "AIVIVN2019_SA":
            if not url:
                print(f"\n{MISS_URL_ERROR}")
                return
            cached_path(url, cache_dir=cache_dir)
            filepath = Path(CACHE_ROOT) / cache_dir / "AIVIVN2019_SA.zip?dl=1"
            cache_folder = Path(CACHE_ROOT) / cache_dir
            zip = zipfile.ZipFile(filepath)
            zip.extractall(cache_folder)
            os.remove(filepath)

    @staticmethod
    def list(all):
        datasets = []
        for key in REPO:
            name = key
            type = REPO[key]["type"]
            license = REPO[key]["license"]
            year = REPO[key]["year"]
            directory = REPO[key]["cache_dir"]
            if not all:
                if license == "Close":
                    continue
            if license == "Close":
                license = "Close*"
            datasets.append([name, type, license, year, directory])

        print(tabulate(datasets,
                       headers=["Name", "Type", "License", "Year", "Directory"],
                       tablefmt='orgtbl'))

        if all:
            print(f"\n{MISS_URL_ERROR}")

    @staticmethod
    def remove(data):
        if data not in REPO:
            print(f"No matching distribution found for '{data}'")
            return
        dataset = REPO[data]
        cache_dir = Path(CACHE_ROOT) / dataset["cache_dir"]
        if cache_dir.is_dir():
            shutil.rmtree(cache_dir)
        print(f"Dataset {data} is removed.")

    @staticmethod
    def load_corpus(corpus_id: Union[NLPData, str]) -> Corpus:
        if corpus_id == NLPData.AIVIVN2019_SA:
            data_folder = Path(CACHE_ROOT) / "datasets" / "aivivn2019_sa"
            return DataFetcher.load_classification_corpus(data_folder)

        if corpus_id == NLPData.AIVIVN2019_SA_SAMPLE:
            data_folder = SAMPLE_CACHE_ROOT / "aivivn2019_sa_sample"
            return DataFetcher.load_classification_corpus(data_folder)

    @staticmethod
    def load_classification_corpus(data_folder) -> CategorizedCorpus:
        train_file = data_folder / "train.txt"
        dev_file = data_folder / "dev.txt"
        test_file = data_folder / "test.txt"
        sentences_train: List[Sentence] = DataFetcher.read_text_classification_file(train_file)
        sentences_dev: List[Sentence] = DataFetcher.read_text_classification_file(dev_file)
        sentences_test: List[Sentence] = DataFetcher.read_text_classification_file(test_file)
        corpus = CategorizedCorpus(sentences_train, sentences_dev, sentences_test)
        return corpus

    @staticmethod
    def read_text_classification_file(path_to_file) -> List[Sentence]:
        sentences = []
        with open(path_to_file) as f:
            lines = f.read().splitlines()
            for line in lines:
                label_pattern = r"__label__(?P<label>\w+)"
                labels = re.findall(label_pattern, line)
                labels = [Label(label) for label in labels]
                text = re.sub(label_pattern, "", line)
                s = Sentence(text, labels)
                sentences.append(s)
        return sentences
