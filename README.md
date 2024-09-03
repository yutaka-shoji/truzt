# \[WIP\] truzt

[Builelib](https://github.com/MasatoMiyata/builelib)-compatible Data Model using [Pydantic](https://docs.pydantic.dev/latest/).

## Data Validation

## Serialization

## [WIP] Convert excel to json

- Building -> 実装済
- Room -> 実装済

## Usage

```python
import json

from truzt.webpro_model import WebproModel


def test_webpro_model_json_serialize():
    with open("sample/sample_input_v3.json") as file:
        wm_dict = json.load(file)
    # WebproModelインスタンスを作成
    wm = WebproModel.model_validate(wm_dict)
    # serialize
    wm_serialized_dict = wm.model_dump(by_alias=True, exclude_unset=True)
    with open("webpro_model.json", "w") as f:
        json.dump(wm_serialized_dict, f, indent=2, ensure_ascii=False)


def test_invalid_input():
    with open("sample/sample_input_v3.json") as file:
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
