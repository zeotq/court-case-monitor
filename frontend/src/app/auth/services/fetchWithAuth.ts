export const fetchWithAuth = async (
    url: string,
    accessToken: string | null,
    setAccessToken: (token: string | null) => void,
    router: any,
    options: RequestInit = {}
  ) => {
    const headers = new Headers(options.headers || {});
    if (accessToken) {
      headers.set("Authorization", `Bearer ${accessToken}`);
    }
  
    let response = await fetch(url, { ...options, headers });
  
    if (response.status === 401) {
      const refreshResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/refresh`, {
        method: "POST",
        credentials: "include",
      });
  
      if (refreshResponse.ok) {
        const refreshData = await refreshResponse.json();
        setAccessToken(refreshData.access_token);
  
        headers.set("Authorization", `Bearer ${refreshData.access_token}`);
        response = await fetch(url, { ...options, headers });
      } else {
        setAccessToken(null);
        router.push("/auth");
      }
    }
  
    return response;
  };
  