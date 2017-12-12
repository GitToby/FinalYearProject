def crossover_old(self, other_cycler):
    # single point crossover:
    crossover_point = int(self.get_sequence_length() // 2)
    # get half 1 from self
    seq_p1 = self.get_sequence()[0: crossover_point]
    # get half 2 from the other_cycler
    seq_p2 = other_cycler.get_sequence()[crossover_point: other_cycler.get_sequence_length()]
    crossed_sequence = seq_p1 + seq_p2
    return CyclerParams(sequence=crossed_sequence)
