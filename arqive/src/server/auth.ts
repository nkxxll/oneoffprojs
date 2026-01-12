import {
  saveToken,
  getTokenByGithubId,
  saveSession,
  getSession,
  deleteSession,
  type Session,
} from "./db";

const GITHUB_CLIENT_ID = Bun.env.GITHUB_CLIENT_ID!;
const GITHUB_CLIENT_SECRET = Bun.env.GITHUB_CLIENT_SECRET!;
const REDIRECT_URI =
  Bun.env.REDIRECT_URI || "http://127.0.0.1:3000/api/auth/callback";

export async function handleLogin(request: Request): Promise<Response> {
  const state = crypto
    .getRandomValues(new Uint8Array(32))
    .toBase64({ alphabet: "base64url" });

  const url = new URL("https://github.com/login/oauth/authorize");
  url.searchParams.set("client_id", GITHUB_CLIENT_ID);
  url.searchParams.set("redirect_uri", REDIRECT_URI);
  url.searchParams.set("scope", "read:user");
  url.searchParams.set("state", state);

  return Response.redirect(url.toString());
}

export async function handleCallback(request: Request): Promise<Response> {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");

  if (!code || !state) {
    return new Response("Missing code or state", { status: 400 });
  }

  try {
    // Exchange code for token
    const tokenResponse = await fetch(
      "https://github.com/login/oauth/access_token",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          Accept: "application/json",
        },
        body: new URLSearchParams({
          client_id: GITHUB_CLIENT_ID,
          client_secret: GITHUB_CLIENT_SECRET,
          code,
          redirect_uri: REDIRECT_URI,
        }),
      },
    );

    const tokenData = await tokenResponse.json();
    if (tokenData.error) {
      throw new Error(tokenData.error_description || tokenData.error);
    }

    const accessToken = tokenData.access_token;
    const refreshToken = tokenData.refresh_token;
    const expiresIn = tokenData.expires_in;
    const expiresAt = expiresIn
      ? new Date(Date.now() + expiresIn * 1000).toISOString()
      : undefined;

    // Get user info
    const userResponse = await fetch("https://api.github.com/user", {
      headers: {
        Authorization: `token ${accessToken}`,
      },
    });

    const user = await userResponse.json();
    const githubId = user.id;

    saveToken(githubId, {
      access_token: accessToken,
      refresh_token: refreshToken,
      expires_at: expiresAt,
    });

    // Create session and set cookie with session_id
    const sessionId = crypto.randomUUID();
    saveSession(sessionId, githubId);

    const response = Response.redirect("/");
    response.headers.set(
      "Set-Cookie",
      `session_id=${sessionId}; HttpOnly; Path=/; Max-Age=86400; SameSite=None; Secure`,
    );
    return response;
  } catch (error) {
    console.error("OAuth callback error:", error);
    return new Response("Authentication failed", { status: 500 });
  }
}

export async function handleLogout(request: Request): Promise<Response> {
  const cookies = request.headers.get("Cookie") || "";
  const sessionIdMatch = cookies.match(/session_id=([^;]+)/);
  if (sessionIdMatch) {
    deleteSession(sessionIdMatch[1]!);
  }
  const response = Response.redirect("/auth/login");
  response.headers.set(
    "Set-Cookie",
    "session_id=; HttpOnly; Path=/; Max-Age=0",
  ); // Clear cookie
  return response;
}

export async function authMiddleware(
  request: Request,
  next: (requst: Request, session: Session) => Promise<Response>,
): Promise<Response> {
  const cookies = request.headers
    .get("cookie")
    ?.split(";")
    .map((cookie) => cookie.trim());

  if (!cookies) {
    console.log("no cookies found");
    return Response.redirect("/");
  }

  console.log(`Session Cookies ${cookies}`);
  const sessionIdMatch = cookies.find((cookie) => {
    console.log(cookie);
    return cookie.startsWith("session_id=");
  });
  console.log(`session match ${sessionIdMatch}`);

  if (!sessionIdMatch) {
    console.log(`Session Request ${JSON.stringify(request.headers)}`);
    console.log(`Session Cookies ${cookies}`);
    console.log("No session cookie found");
    return Response.redirect("/");
  }

  const session_id = sessionIdMatch.split("=")[1];

  if (!session_id) {
    console.log("No session ID found");
    return Response.redirect("/");
  }

  const session = getSession(session_id);
  if (!session) {
    return Response.redirect("/");
  }

  const githubId = session.github_id;
  const token = getTokenByGithubId(githubId);
  if (!token) {
    return Response.redirect("/");
  }
  return next(request, session);
}

export async function authStatus(request: Request): Promise<Response> {
  const cookies = request.headers.getSetCookie();

  const sessionIdMatch = cookies.find((cookie) =>
    cookie.startsWith("session_id="),
  );

  if (!sessionIdMatch) {
    return Response.json({ status: "no_session" });
  }

  const session = getSession(sessionIdMatch[1]!);
  if (!session) {
    return Response.json({ status: "no_session" });
  }

  const githubId = session.github_id;
  const token = getTokenByGithubId(githubId);
  if (!token) {
    return Response.json({ status: "no_token" });
  }
  return Response.json({ status: "authenticated" });
}
