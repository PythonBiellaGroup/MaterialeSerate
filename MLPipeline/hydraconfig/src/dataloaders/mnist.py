from dataclasses import dataclass, field


@dataclass
class MNISTLoader:
    file_path: str
    name: str = 'MNIST'

