class FFNNModel():
    def __init__(self, num_layers, hidden_size, out_size):
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.out_size = out_size

    def train(self, dataloader):
        a = str(dataloader)
        res = f'Trained FFNN with hyperparameters LAYERS: {self.num_layers} HIDDEN: {self.hidden_size} ' \
              f'OUT_SIZE: {self.out_size} over DATASET {a}'
        return res