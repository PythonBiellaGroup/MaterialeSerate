from hydraconfig.src.dataloaders.cifar import CIFARLoader
from hydraconfig.src.models.ffnn import FFNNModel
from hydraconfig.src.models.cnn import CNNModel
from hydraconfig.src.dataloaders.mnist import MNISTLoader


def train():
    # dataloader = CIFARLoader(file_path='data', train_val_test_split=[80, 10, 10])
    dataloader = MNISTLoader(file_path='data')

    # model = FFNNModel(layers=3, hidden_size=512, out_size=10)
    model = CNNModel(num_layers=3, conv_size=3)

    res = model.train(dataloader)

    print(res)


if __name__ == '__main__':
    train()
