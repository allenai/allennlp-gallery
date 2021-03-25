Posing reading comprehension as a generation problem provides a great deal of flexibility,
allowing for open-ended questions with few restrictions on possible answers. However,
progress is impeded by existing generation metrics, which rely on token overlap and are
agnostic to the nuances of reading comprehension. To address this, we introduce a benchmark
for training and evaluating generative reading comprehension metrics: MOdeling Correctness
with Human Annotations. MOCHA contains 40K human judgement scores on model outputs from 6
diverse question answering datasets and an additional set of minimal pairs for evaluation.
Using MOCHA, we train an evaluation metric: LERC, a Learned Evaluation metric for Reading
Comprehension, to mimic human judgement scores.
