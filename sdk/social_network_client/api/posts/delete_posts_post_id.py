from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_message import ErrorMessage
from ...types import Response


def _get_kwargs(
    post_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/posts/{post_id}".format(
            post_id=quote(str(post_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ErrorMessage | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 404:
        response_404 = ErrorMessage.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ErrorMessage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    post_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ErrorMessage]:
    """Delete post by ID

    Args:
        post_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorMessage]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    post_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ErrorMessage | None:
    """Delete post by ID

    Args:
        post_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorMessage
    """

    return sync_detailed(
        post_id=post_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    post_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | ErrorMessage]:
    """Delete post by ID

    Args:
        post_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ErrorMessage]
    """

    kwargs = _get_kwargs(
        post_id=post_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    post_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Any | ErrorMessage | None:
    """Delete post by ID

    Args:
        post_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ErrorMessage
    """

    return (
        await asyncio_detailed(
            post_id=post_id,
            client=client,
        )
    ).parsed
