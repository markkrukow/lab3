from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_message import ErrorMessage
from ...models.post import Post
from ...types import Response


def _get_kwargs(
    post_id: int,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/posts/{post_id}".format(
            post_id=quote(str(post_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorMessage | Post | None:
    if response.status_code == 200:
        response_200 = Post.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = ErrorMessage.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorMessage | Post]:
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
) -> Response[ErrorMessage | Post]:
    """Get post by ID

    Args:
        post_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorMessage | Post]
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
) -> ErrorMessage | Post | None:
    """Get post by ID

    Args:
        post_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorMessage | Post
    """

    return sync_detailed(
        post_id=post_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    post_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[ErrorMessage | Post]:
    """Get post by ID

    Args:
        post_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorMessage | Post]
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
) -> ErrorMessage | Post | None:
    """Get post by ID

    Args:
        post_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorMessage | Post
    """

    return (
        await asyncio_detailed(
            post_id=post_id,
            client=client,
        )
    ).parsed
