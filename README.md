# La magia NER nascosta
## Progetto di TLN
### Luca Demma
--- 
## Instructions to run the code
1. Clone the repository
2. Install the following python packages:
	- `pandas` 
	- `tqdm` 
	- `conllu`
3. In the root folder of the project create the following directory tree structure (case sensitive), putting the train and test file from https://github.com/Babelscape/wikineural/tree/master/data/wikineural/en and https://github.com/Babelscape/wikineural/tree/master/data/wikineural/en in their respective folders:
```bash
data
├── outputs
│   ├── DECODING
│   │   ├── EN
│   │   └── IT
│   └── LEARNING
│       ├── EN
│       └── IT
├── wikineural_en
│   ├── test.conllu
│   └── train.conllu
└── wikineural_it
    ├── test.conllu
    └── train.conllu

```
4. Start the Training launching: ```learning.py LANG``` replacing LANG with `IT` or `EN` (if no argument is passed it defaults to IT). The results of the training will be saved in `data/outputs/DECODING/LANG/` in CSV format
5. Launch the Decoding with: ```main.py LANG BASELINE``` replacing `LANG` with `IT` or `EN` and `BASELINE` with `baseline` to calculate the NER tags with the baseline method. To don't calculate the baseline don't pass any argument as `BASELINE`. The results will be saved as CSV files in `data/outputs/DECODING/LANG`
6. To get the NER tags of the 3 sentences present in the slides launch ```decode.py```. The result will be printed to console in the CoNLL-U format

# Project Report
[Link to the report of the project](./report/Relazione.pdf)
