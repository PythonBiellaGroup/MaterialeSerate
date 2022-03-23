import pytorch_lightning as pl
from pytorch_lightning import loggers as pl_loggers
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping

from ptlight.src.models.cnn import LightningNet
from ptlight.src.callbacks.logging import TBParametersLoggingCallback
from ptlight.src.datamodule.cifar import CIFAR10DataModule


def train():
    data_module = CIFAR10DataModule()
    model = LightningNet()

    train_checkpoint = ModelCheckpoint(
        filename="{epoch}-{step}-{train_loss:.1f}",
        monitor='train/loss',
        mode='min',
        save_top_k=3
    )

    latest_checkpoint = ModelCheckpoint(
        filename='latest-{epoch}-{step}',
        every_n_train_steps=500,
        save_top_k=1
    )

    early_stop_callback = EarlyStopping(
        monitor="val/loss",
        min_delta=0.00,
        patience=3,
        verbose=True,
        mode="min"
    )

    tb_logger = pl_loggers.TensorBoardLogger("logs/", log_graph=True)
    tb_param_logger = TBParametersLoggingCallback()
    trainer = pl.Trainer(max_epochs=1,
                         callbacks=[latest_checkpoint, train_checkpoint, tb_param_logger, early_stop_callback],
                         gpus=1,
                         logger=tb_logger,
                         fast_dev_run=False,
                         progress_bar_refresh_rate=20, val_check_interval=0.3)

    trainer.fit(model, data_module)
    trainer.test(model, data_module)


if __name__ == '__main__':
    train()
