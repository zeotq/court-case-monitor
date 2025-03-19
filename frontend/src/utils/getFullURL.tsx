"use client";

import { useEffect, useState } from "react";

const Component = () => {
  const [fullUrl, setFullUrl] = useState("");

  useEffect(() => {
    setFullUrl(window.location.href);
  }, []);

  return fullUrl;
};

export default Component;