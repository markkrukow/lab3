from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.validation_error_detail_item import ValidationErrorDetailItem


T = TypeVar("T", bound="ValidationError")


@_attrs_define
class ValidationError:
    """
    Attributes:
        detail (list[ValidationErrorDetailItem]):
    """

    detail: list[ValidationErrorDetailItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = []
        for detail_item_data in self.detail:
            detail_item = detail_item_data.to_dict()
            detail.append(detail_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detail": detail,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.validation_error_detail_item import ValidationErrorDetailItem

        d = dict(src_dict)
        detail = []
        _detail = d.pop("detail")
        for detail_item_data in _detail:
            detail_item = ValidationErrorDetailItem.from_dict(detail_item_data)

            detail.append(detail_item)

        validation_error = cls(
            detail=detail,
        )

        validation_error.additional_properties = d
        return validation_error

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
