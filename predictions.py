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
from seq2seq.dataset import SourceField, TargetField, Word2Vectors
from seq2seq.evaluator import Predictor, HierarchialPredictor
from seq2seq.util.checkpoint import Checkpoint

def predict_with_checkpoint(checkpoint_path,
                            sequence,
                            hierarchial = False,
                            remote = None,
                            word_vectors = None):
    checkpoint = Checkpoint.load(checkpoint_path)
    seq2seq = checkpoint.model
    input_vocab = checkpoint.input_vocab
    output_vocab = checkpoint.output_vocab

    
    seq2seq.encoder.word_vectors, seq2seq.decoder.word_vectors = None, None
    if word_vectors != None:
        input_vects = Word2Vectors(input_vocab, word_vectors, word_vectors.dim_size)
        output_vects = Word2Vectors(output_vocab, word_vectors, word_vectors.dim_size)
        seq2seq.encoder.word_vectors, seq2seq.decoder.word_vectors = input_vects, output_vects

        
    seq2seq.decoder = TopKDecoder(seq2seq.decoder, 5)


        
    if not hierarchial:
        predictor = Predictor(seq2seq, input_vocab, output_vocab)
        seq = sequence.strip().split()
    else:
        predictor = HierarchialPredictor(seq2seq, input_vocab, output_vocab)
        seq = ['|'.join(x.split()) for x in sequence]


    return ' '.join(predictor.predict(seq))


def remote_predict(checkpoint_path,
                   sequence,
                   hierarchial = False,
                   remote = None):

    precommand = remote['precommand']
    command = remote['command']
    checkpoint_path = checkpoint_path.split("::")[-1]
    if hierarchial:
        sequence = '<n>'.join([x.strip() for x in sequence])

    command = command + "{checkpoint_path} '{sequence}' {hierarchial} 5 2> /dev/null".format(**locals())
    finalcommand = precommand + " \"" + command+ "\" > tmp.out"
    print('Seq', sequence)
    print(finalcommand)
    os.system(finalcommand)
    return open('tmp.out').read()
    #return ""
