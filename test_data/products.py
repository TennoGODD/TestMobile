# products.py — тестовая продукция и параметры стенда

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    gtin: str
    name: str


WATER = Product(gtin="07665585002196", name="МАСТ Минеральная водица")

LINE = 67         
AGGR_LEVEL0_ID = 1166609   
AGGR_LEVEL1_ID = 1169809  
