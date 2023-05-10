import numpy as np
from echo_logger import *
import evaluate
if __name__ == '__main__':
    metric = evaluate.load("accuracy")


    def compute_acc(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

