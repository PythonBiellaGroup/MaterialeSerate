class CNNModel():
    def __init__(self, conv_size, num_layers):
        self.conv_size = conv_size
        self.num_layers = num_layers

    def train(self, dataloader):
        a = str(dataloader)
        res = f'Trained CNN with hyperparameters CONV:{self.conv_size} - LAYERS: {self.num_layers} over DATASET {a}'
        return res