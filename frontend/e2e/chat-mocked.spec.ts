import { test, expect } from "@playwright/test";

/**
 * CI-safe E2E tests that intercept all /api/* calls at the network layer.
 * No backend required — Vite dev server serves the React app, and
 * page.route() returns canned JSON responses.
 */

const HEALTH_OK = {
  status: "ok",
  retriever_loaded: true,
  provider_configured: true,
};

const GENERATE_OK = {
  generated_code: "fun addNumbers(a, b):\n    return a + b\nend fun",
  retrieved_functions: [
    {
      score: 0.95,
      function_name: "addNumbers",
      parameters: ["a", "b"],
      code: "fun addNumbers(a, b):\n    return a + b\nend fun",
    },
  ],
  cached: false,
};

/** Install default route mocks (health OK, generate OK). */
async function mockApi(page: import("@playwright/test").Page) {
  await page.route("**/api/health", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(HEALTH_OK) }),
  );
  await page.route("**/api/generate", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(GENERATE_OK) }),
  );
}

test.describe("AVP RAG Chat (mocked)", () => {
  test("page loads with UI elements", async ({ page }) => {
    await mockApi(page);
    await page.goto("/");
    await expect(page.getByText("AVP RAG Chat")).toBeVisible();
    await expect(page.getByPlaceholder("Ask me to generate AVP code...")).toBeVisible();
    await expect(page.getByRole("button", { name: "Send" })).toBeVisible();
  });

  test("send message and receive response", async ({ page }) => {
    await mockApi(page);
    await page.goto("/");

    await page.getByPlaceholder("Ask me to generate AVP code...").fill("write a function to add two numbers");
    await page.getByRole("button", { name: "Send" }).click();

    const assistant = page.locator("pre").first();
    await expect(assistant).toBeVisible();
    await expect(assistant).toContainText("fun addNumbers");
  });

  test("response contains AVP keywords", async ({ page }) => {
    await mockApi(page);
    await page.goto("/");

    await page.getByPlaceholder("Ask me to generate AVP code...").fill("write a function to add two numbers");
    await page.getByRole("button", { name: "Send" }).click();

    const assistant = page.locator("pre").first();
    await expect(assistant).toBeVisible();
    const text = await assistant.textContent();
    expect(text).toMatch(/fun\b/);
    expect(text).toMatch(/end fun/);
  });

  test("multiple messages appear in chat", async ({ page }) => {
    await mockApi(page);
    await page.goto("/");

    const input = page.getByPlaceholder("Ask me to generate AVP code...");
    await input.fill("write a function to add two numbers");
    await page.getByRole("button", { name: "Send" }).click();
    await page.locator("pre").first().waitFor();

    await input.fill("write a fibonacci function");
    await page.getByRole("button", { name: "Send" }).click();

    await expect(page.locator("pre")).toHaveCount(2);
  });

  test("empty input does not send", async ({ page }) => {
    await mockApi(page);
    await page.goto("/");
    await expect(page.getByRole("button", { name: "Send" })).toBeDisabled();
  });

  test("rate limit error renders", async ({ page }) => {
    await page.route("**/api/health", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(HEALTH_OK) }),
    );
    await page.route("**/api/generate", (route) =>
      route.fulfill({ status: 429, contentType: "text/plain", body: "Rate limit exceeded" }),
    );
    await page.goto("/");

    await page.getByPlaceholder("Ask me to generate AVP code...").fill("trigger rate limit");
    await page.getByRole("button", { name: "Send" }).click();

    await expect(page.getByText("Rate limit exceeded")).toBeVisible();
  });

  test("server error renders", async ({ page }) => {
    await page.route("**/api/health", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(HEALTH_OK) }),
    );
    await page.route("**/api/generate", (route) =>
      route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Internal server error" }),
      }),
    );
    await page.goto("/");

    await page.getByPlaceholder("Ask me to generate AVP code...").fill("trigger error");
    await page.getByRole("button", { name: "Send" }).click();

    await expect(page.getByText("Internal server error")).toBeVisible();
  });

  test("network failure renders", async ({ page }) => {
    await page.route("**/api/health", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(HEALTH_OK) }),
    );
    await page.route("**/api/generate", (route) => route.abort());
    await page.goto("/");

    await page.getByPlaceholder("Ask me to generate AVP code...").fill("trigger network failure");
    await page.getByRole("button", { name: "Send" }).click();

    await expect(page.getByText("Failed to connect to the server.")).toBeVisible();
  });
});
