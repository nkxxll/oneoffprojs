export function getCookies(request: Request, cookie: string): string | null {
  const cookies = request.headers.get("cookie")?.split(";");

  if (!cookies) {
    return null;
  }

  const sessionIdMatch = cookies.find((cookie) =>
    cookie.startsWith(`${cookie}=`),
  );
  if (!sessionIdMatch) {
    return null;
  }

  const cookie_res = sessionIdMatch.split("=")[1];

  if (!cookie_res) {
    console.log("No session ID found");
    return null;
  }
  return cookie_res;
}
