export const generatePKCE = async () => {
    const codeVerifier = btoa(crypto.getRandomValues(new Uint8Array(32)).toString());
  
    const encoder = new TextEncoder();
    const data = encoder.encode(codeVerifier);
    const digest = await crypto.subtle.digest("SHA-256", data);
    const codeChallenge = btoa(String.fromCharCode(...new Uint8Array(digest)))
      .replace(/=/g, "")
      .replace(/\+/g, "-")
      .replace(/\//g, "_");
  
    return { codeVerifier, codeChallenge };
  };
  