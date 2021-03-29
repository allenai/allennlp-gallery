This is a simple neural truecaser written with AllenNLP, and based
loosely on ([Susanto et al, 2016](https://aclweb.org/anthology/D16-1225)).
They have an implementation [here](https://gitlab.com/raymondhs/char-rnn-truecase),
but being written in Lua, it's a little hard to use.

We provide [pre-trained models](https://github.com/mayhewsw/pytorch-truecaser/releases/tag/v1.0)
that can be used for truecasing English and German right out of the box. The English model is
trained on the [standard Wikipedia data split](http://www.cs.pomona.edu/~dkauchak/simplification/data.v1/data.v1.split.tar.gz)
from ([Coster and Kauchak, 2011](https://api.semanticscholar.org/CorpusID:9128245)), and achieves an F1 score of **93.01** on
test. This is comparable to the best F1 of ([Susanto et al, 2016](https://aclweb.org/anthology/D16-1225)) of **93.19**.
