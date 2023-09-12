from typing import Any

from drf_spectacular.utils import OpenApiParameter
from rest_framework.request import Request

from core.app.api_exceptions import NotAcceptable

TopQueryParameter = OpenApiParameter(
    name="top",
    type=int,
    description="Limits the quantity."
)
MinDateQueryParameter = OpenApiParameter(
    name="min_date",
    type=str,
    description="Limits the minimum date."
)
MaxDateQueryParameter = OpenApiParameter(
    name="max_date",
    type=str,
    description="Limits the maximum date."
)
LastDaysQueryParameter = OpenApiParameter(
    name="last_days",
    type=int,
    description="Limits the last day."
)
HeroQueryParameter = OpenApiParameter(
    name="hero",
    type=str,
    description="Group by hero."
)
WinQueryParameter = OpenApiParameter(
    name="win",
    type=bool,
    description="Group games by win/lose."
)


def parse_query_parameter(
        request: Request,
        parameter: OpenApiParameter
) -> Any:
    """Reads query parameter from request, converts as required type.

    * If value can not be converted to a required type, raises an exception.

    :raises NotAcceptable: when unable to convert query parameter."""

    query_parameter = request.query_params.get(parameter.name)

    if not query_parameter:
        return None

    try:
        if parameter.type == bool:
            query_parameter = query_parameter.upper()
            if query_parameter not in ["TRUE", "FALSE"]:
                raise ValueError
            return True if query_parameter == "TRUE" else False
        serialized = parameter.type(query_parameter)
    except ValueError:
        raise NotAcceptable(
            detail="Unable to parse parameter '{}' as {}.".format(
                query_parameter,
                parameter.type.__name__
            )
        )

    return serialized
