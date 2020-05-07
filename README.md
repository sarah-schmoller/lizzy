# Lizzy
## A Python implementation of the Eliza chatbot

A Python implementation of Joseph Weizenbaum's 1966 chatbot, based on his paper in Communications of the ACM. The original paper is included in the repo as weizenbaum1966.pdf.

This package implements the popular DOCTOR script originally presented by Weizenbaum, by which the chatbot takes on the role of a Rogerian therapist. Eliza performs best when the user confines the conversation to simple statements about their own life.

## Usage

The chatbot can be downloaded via pip using the following command:

```
pip install git+https://github.com/sarah-schmoller/lizzy.git
```

To run, start Python in your teminal and execute the following script:
https://github.com/sarah-schmoller/lizzy/blob/main/demo.gif
```
from lizzy import chatbot

eliza = chatbot.Lizzy()
eliza.load()
eliza.run()

```

![](https://github.com/sarah-schmoller/lizzy/blob/main/demo.gif)