import os
import argparse
import logging

import torch
from torch.optim.lr_scheduler import StepLR
import torchtext

import seq2seq
from seq2seq.trainer import SupervisedTrainer
from seq2seq.models import EncoderRNN, DecoderRNN, Seq2seq, HSeq2seq, TopKDecoder
from seq2seq.loss import Perplexity
from seq2seq.optim import Optimizer
from seq2seq.dataset import SourceField, TargetField
from seq2seq.evaluator import Predictor, HierarchialPredictor
from seq2seq.util.checkpoint import Checkpoint

def predict_with_checkpoint(checkpoint_path, sequence, hierarchial = False):
    checkpoint = Checkpoint.load(checkpoint_path)
    seq2seq = checkpoint.model
    input_vocab = checkpoint.input_vocab
    output_vocab = checkpoint.output_vocab

    seq2seq.decoder = TopKDecoder(seq2seq.decoder, 5)

    if not hierarchial:
        predictor = Predictor(seq2seq, input_vocab, output_vocab)
        seq = sequence.strip().split()
    else:
        predictor = HierarchialPredictor(seq2seq, input_vocab, output_vocab)
        seq = ['|'.join(x.split()) for x in sequence]


    return predictor.predict(seq)
