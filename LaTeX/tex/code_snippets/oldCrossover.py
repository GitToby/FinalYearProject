def crossover_old(self, other_cycler,in_seed=0):
    seq1 = self.sequence
    seq2 = other_cycler.sequence

    if not in_seed == 0:
        # only seed for when we explicitly give it a seed
        random.seed(in_seed)

    midpoint = int(random.randint(0, len(seq1)) / 2)
    new_seq = seq1[:midpoint] + seq2[midpoint:]
    return CyclerParams(sequence=new_seq)


    
