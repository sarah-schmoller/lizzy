# Lizzy
## A Python implementation of the Eliza chatbot

A Python implementation of Joseph Weizenbaum's 1966 chatbot, based on his paper in Communications of the ACM. The original paper is included in the repo as weizenbaum1966.pdf.

## Usage

The chatbot can be downloaded via pip using the following command:

```
pip install git+https://github.com/sarah-schmoller/lizzy.git
```

To run, execute the following Python script:

```
from lizzy import chatbot

eliza = chatbot.Lizzy()
eliza.load()
eliza.run()

```