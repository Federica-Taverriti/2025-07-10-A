from dataclasses import dataclass

from model.product import Product


@dataclass
class Arco:
    p1: Product
    p2: Product
    peso: int