const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const logout = async (setAccessToken: (token: string | null) => void) => {
  try {
    const response = await fetch(`${API_URL}/auth/logout`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || "Ошибка при выходе");
    }

    console.log("Успешный выход из системы");
    setAccessToken(null); // Обнуляем токен после выхода
    return true;
  } catch (error) {
    console.error("Ошибка выхода:", error);
    return false;
  }
};
