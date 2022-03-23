import pytorch_lightning as pl

from ptlight.src.models.cnn import LightningNet
from ptlight.src.datamodule.cifar import CIFAR10DataModule


def test():
    data_module = CIFAR10DataModule()
    model = LightningNet()

    trainer = pl.Trainer(resume_from_checkpoint='PATH_TO_BEST_MODEL')

    trainer.test(model, data_module)


if __name__ == '__main__':
    test()
