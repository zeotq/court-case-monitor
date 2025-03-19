export const fetchWithAuth = async (
  url: string,
  auth: { accessToken: string | null; setAccessToken: (token: string | null) => void },
  push: (url: string) => void,
  options: RequestInit = {}
) => {
  const headers = new Headers(options.headers || {});

  if (auth.accessToken) {
    headers.set("Authorization", `Bearer ${auth.accessToken}`);
  }

  let response = await fetch(url, { ...options, headers });

  if (response.status === 401) {
    const refreshResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    });

    if (refreshResponse.ok) {
      const refreshData = await refreshResponse.json();
      auth.setAccessToken(refreshData.access_token);
      headers.set("Authorization", `Bearer ${refreshData.access_token}`);
      response = await fetch(url, { ...options, headers });
    } else {
      const redirectUri = encodeURIComponent(window.location.href);
      auth.setAccessToken(null);
      push(`/auth?redirect_uri=${redirectUri}`);
    }
  }

  return response;
};
