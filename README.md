# \[WIP\] truzt

[Builelib](https://github.com/MasatoMiyata/builelib)-compatible Data Model using [Pydantic](https://docs.pydantic.dev/latest/).

## Data Validation

```python
import json

from truzt.webpro_model import WebproModel


def test_webpro_model_json_serialize():
    with open("sample/sample_v3.json") as file:
        wm_dict = json.load(file)
    # WebproModelインスタンスを作成
    wm = WebproModel.model_validate(wm_dict)
    # serialize
    wm_serialized_dict = wm.model_dump(by_alias=True, exclude_unset=True)
    with open("webpro_model.json", "w") as f:
        json.dump(wm_serialized_dict, f, indent=2, ensure_ascii=False)


def test_invalid_input():
    with open("sample/sample_v3.json") as file:
        wm_dict = json.load(file)
        wm_dict["Building"]["Region"] = 9  # <- 地域区分(1-8)に範囲外の値を入力
    try:
        wm = WebproModel.model_validate(wm_dict)
    except ValueError as e:
        print(e)

    # OUTPUT AS FOLLOWS
    # 1 validation error for WebproModel
    # Building.Region
    #   Input should be less than or equal to 8 [type=less_than_equal, input_value=9, input_type=int]


if __name__ == "__main__":
    test_webpro_model_json_serialize()
    test_invalid_input()
```

## [WIP] Convert excel to json

### Roadmap

| model                                 | v2  | v3  | reference sheet                   |
| ------------------------------------- | --- | --- | --------------------------------- |
| `Building`                            | ✅  | ✅  | **0) 基本情報**                   |
| `Rooms`                               | ✅  | ✅  | **1) 室仕様**                     |
| `AirConditioningZone`                 | ✅  | ⬜  | **2-1) 空調ゾーン**               |
| `WallConfigure`                       | ✅  | ⬜  | **2-2) 外壁構成**                 |
| `WindowConfigure`                     | ✅  | ⬜  | **2-3) 窓仕様**                   |
| `EnvelopeSet` / `ShadingConfigure`    | ✅  | ⬜  | **2-4) 外皮**                     |
| `HeatSourceSystem`                    | ⬜  | ⬜  | **2-5) 熱源**                     |
| `SecondaryPumpSystem`                 | ⬜  | ⬜  | **2-6) 2 次ﾎﾟﾝﾌﾟ**                |
| `AirHandlingSystem`                   | ⬜  | ⬜  | **2-7) 空調機**                   |
| **only v3?**                          | ⬜  | ⬜  | **2-8) 熱源水温度**               |
| **only v3?**                          | ⬜  | ⬜  | **2-9) 全熱交換器**               |
| `VentilationRoom`                     | ⬜  | ⬜  | **3-1) 換気室**                   |
| `VentilationUnit`                     | ⬜  | ⬜  | **3-2) 換気送風機**               |
| `VentilationRoom` / `VentilationUnit` | ⬜  | ⬜  | **3-3) 換気空調機**               |
| **only v3?**                          | ⬜  | ⬜  | **3-4) 年間平均負荷率**           |
| `LightingRoom`                        | ⬜  | ⬜  | **4) 照明**                       |
| `HotWaterRoom`                        | ⬜  | ⬜  | **5-1) 給湯室**                   |
| `HotWaterSupplySystem`                | ⬜  | ⬜  | **5-2) 給湯機器**                 |
| `Elevators`                           | ⬜  | ⬜  | **6) 昇降機**                     |
| `PhotovoltaicSystem`                  | ⬜  | ⬜  | **7-1) 太陽光発電**               |
| `CogenerationSystem`                  | ⬜  | ⬜  | **7-3) コージェネレーション設備** |
| _builelib_ **not supported?**         | ⬜  | ⬜  | **8) 非空調外皮**                 |
| `WebproModel`                         | ⬜  | ⬜  | **モデル横断で影響する部分**      |
| **for SP sheet...**                   | ⬜  | ⬜  | **builelib sp sheets...**         |

## Contribution

See [docs/CONTRIBUTING.md](https://github.com/yutaka-shoji/truzt/blob/main/docs/CONTRIBUTING.md)
