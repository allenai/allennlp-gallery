Models encapsulating narrative schema knowledge have proven to be useful for a range of event-related tasks, but these
models typically do not engage with temporal relationships between events. We present a a BART-based conditional
generation model capable of capturing event cooccurrence as well as temporality of event sequences. This single model
can address both temporal ordering, sorting a given sequence of events into the order they occurred, and event
infilling, predicting new events which fit into a temporally-ordered sequence of existing ones. Our model is trained as
a denoising autoencoder: we take temporally-ordered event sequences, shuffle them, delete some events, and then
attempting to recover the original event sequence. In this fashion, the model learns to make inferences given incomplete
knowledge about the events in an underlying scenario. On the temporal ordering task, we show that our model is able to
unscramble event sequences from existing datasets without access to explicitly labeled temporal training data,
outperforming both a BERT-based pairwise model and a BERT-based pointer network. On event infilling, human evaluation
shows that our model is able to generate events that fit better temporally into the input events when compared to GPT-2
story completion models.
