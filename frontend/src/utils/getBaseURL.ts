const getBaseURL = () => {
    if (typeof window !== "undefined") {
      const url = new URL(window.location.href);
      return `${url.protocol}//${url.host}`;
    }
    return "";
  };
  
  export default getBaseURL;
  