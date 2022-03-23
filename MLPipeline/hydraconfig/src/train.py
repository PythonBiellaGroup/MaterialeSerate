import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig


@hydra.main(config_path="../config/", config_name="train.yaml")
def train(cfg: DictConfig):
    print(cfg)
    dataloader = instantiate(cfg.dataloader)
    model = instantiate(cfg.model)
    result = model.train(dataloader)

    print(result)


if __name__ == '__main__':
    train()
