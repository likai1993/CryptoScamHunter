# CryptoScamHunter
This repository contains the code and data related to the Arbitrage bot scam. We reported this scam in our paper "Towards Understanding and Characterizing the Arbitrage Bot Scam In the Wild" accepted by ACM SIGMETRICS 2024.

1. How to collect YouTube videos by keywords. 
`python3 search_videos.py`

2. The ground-truth datasets and trained models are placed in `allennlp`.

3. Scam videos and URLs extracted from video descriptions are in `scam_videos`.

4. Scam addresses extracted from the downloaded bot contracts and expanded scam addresses are in `scam_addresses`. The folder also contains the source code of contract-rewriter and similar-contract-matching.


#### If you use our code or data, please cite our work as follows.

    @inproceedings{li2024towards,  
    title={Towards Understanding and Characterizing the Arbitrage Bot Scam In the Wild},  
    author={Li, Kai and Guan, Shixuan and Lee, Darren},  
    booktitle={ACM SIGMETRICS},  
    year={2024}  
    }  
