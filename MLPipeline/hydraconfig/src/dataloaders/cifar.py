from dataclasses import dataclass, field


@dataclass
class CIFARLoader:
    file_path: str
    train_val_test_split: list
    name: str = 'CIFAR'
