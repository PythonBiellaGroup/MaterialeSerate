from typing import Any, Optional

import pytorch_lightning as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchmetrics
from hydra.utils import instantiate
from pytorch_lightning.utilities.types import STEP_OUTPUT
from torch import optim
from torch.nn import CrossEntropyLoss
from torchmetrics.functional import accuracy


class LightningNet(pl.LightningModule):
    def __init__(self, num_classes=10, loss=None, optimizer=None):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, (5, 5))
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, (5, 5))
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)

        self.valid_acc = torchmetrics.Accuracy()
        self.test_acc = torchmetrics.Accuracy()
        if loss is None:
            loss = CrossEntropyLoss()
        self.loss = instantiate(loss)
        if optimizer is None:
            optimizer = optim.SGD(self.parameters(), lr=0.001, momentum=0.9)
        self.optimizer = instantiate(optimizer, params=self.parameters())

    def forward(self, x, *args, **kwargs) -> Any:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)  # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def custom_histogram_adder(self):
        # iterating through all parameters
        for name, params in self.named_parameters():
            self.logger.experiment.add_histogram(name, params, self.current_epoch)

    def training_step(self, batch, batch_idx, *args, **kwargs) -> STEP_OUTPUT:
        inputs, labels = batch
        outputs = self.forward(inputs)
        loss = self.loss(outputs, labels)
        self.log('train/loss', loss)
        # return loss
        acc = accuracy(outputs, labels)
        pbar = {'train/acc': acc}
        return {'loss': loss, 'progress_bar': pbar}

    # def training_epoch_end(self, outputs: EPOCH_OUTPUT) -> None:
    #     self.custom_histogram_adder()

    def configure_optimizers(self):
        return self.optimizer

    def validation_step(self, batch, batch_idx, *args, **kwargs) -> Optional[STEP_OUTPUT]:
        images, labels = batch
        # calculate outputs by running images through the network
        outputs = self(images)
        loss = self.loss(outputs, labels)
        self.log('val/loss', loss, on_epoch=True, prog_bar=True)
        # the class with the highest energy is what we choose as prediction
        _, predicted = torch.max(outputs.data, 1)
        accuracy = self.valid_acc(predicted, labels)
        self.log('val/acc_epoch', accuracy, on_epoch=True)
        self.log('val/acc_step', accuracy)
        return

    def test_step(self, val_batch, *args, **kwargs) -> Optional[STEP_OUTPUT]:
        images, labels = val_batch
        # calculate outputs by running images through the network
        outputs = self(images)
        # the class with the highest energy is what we choose as prediction
        _, predicted = torch.max(outputs.data, 1)
        accuracy = self.test_acc(predicted, labels)
        self.log('test/acc_step', accuracy)
        return

    def test_step_end(self, *args, **kwargs) -> Optional[STEP_OUTPUT]:
        self.log('test/acc_epoch', self.valid_acc.compute())
        return
