"""HTTP and remote asset utilities for PDF generation pipeline."""

from __future__ import annotations

import hashlib
import os
import tempfile

from typing import Optional

try:
	# Python 3 stdlib
	from urllib.request import Request, urlopen
except Exception:  # pragma: no cover - environments without urllib
	Request = None  # type: ignore
	urlopen = None  # type: ignore


def download_remote_asset(url: str, context: Optional[dict] = None, timeout: int = 20) -> Optional[str]:
	"""
	Download a remote asset into a cache directory and return the local file path.

	Behavior:
	- Uses a cache directory stored in `context['download_cache_dir']` when provided.
	- If no cache dir is provided, creates a temporary one and persists its path in the context.
	- Generates a stable filename based on the SHA1 of the URL plus its extension (if present).
	- Returns None on failure or when urllib is unavailable.
	"""
	try:
		if Request is None or urlopen is None:
			return None

		ctx = context if isinstance(context, dict) else {}
		cache_dir = ctx.get('download_cache_dir')

		if not cache_dir:
			cache_dir = tempfile.mkdtemp(prefix='scl_assets_')
			ctx['download_cache_dir'] = cache_dir

			if isinstance(context, dict):
				context['download_cache_dir'] = cache_dir

		# Build stable filename from URL hash + original extension if any
		url_bytes = url.encode('utf-8')
		h = hashlib.sha1(url_bytes).hexdigest()
		ext = ''
		base = os.path.basename(url)
		if '.' in base:
			ext = '.' + base.split('.')[-1].split('?')[0].split('#')[0]

		fname = f"{h}{ext}"
		fpath = os.path.join(cache_dir, fname)
		if os.path.exists(fpath) and os.path.getsize(fpath) > 0:
			return fpath

		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

		with urlopen(req, timeout=timeout) as resp, open(fpath, 'wb') as out:
			out.write(resp.read())

		return fpath if os.path.exists(fpath) and os.path.getsize(fpath) > 0 else None
	except Exception:
		return None
