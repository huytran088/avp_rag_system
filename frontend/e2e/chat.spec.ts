import { test, expect } from "@playwright/test";

test.describe("AVP RAG Chat", () => {
  test("page loads with input and submit button", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("AVP RAG Chat")).toBeVisible();
    await expect(page.getByPlaceholder("Ask me to generate AVP code...")).toBeVisible();
    await expect(page.getByRole("button", { name: "Send" })).toBeVisible();
  });

  test("health check returns ok", async ({ request }) => {
    const res = await request.get("http://localhost:8000/api/health");
    expect(res.ok()).toBeTruthy();
    const body = await res.json();
    expect(body.status).toBe("ok");
    expect(body.retriever_loaded).toBe(true);
  });

  test("send message and receive response", async ({ page }) => {
    await page.goto("/");
    const input = page.getByPlaceholder("Ask me to generate AVP code...");
    await input.fill("write a function to add two numbers");
    await page.getByRole("button", { name: "Send" }).click();

    // Wait for assistant response (generous timeout for LLM)
    const assistant = page.locator("pre").first();
    await expect(assistant).toBeVisible({ timeout: 60_000 });
    await expect(assistant).not.toBeEmpty();
  });

  test("assistant response contains AVP keywords", async ({ page }) => {
    await page.goto("/");
    const input = page.getByPlaceholder("Ask me to generate AVP code...");
    await input.fill("write a function to add two numbers");
    await page.getByRole("button", { name: "Send" }).click();

    const assistant = page.locator("pre").first();
    await expect(assistant).toBeVisible({ timeout: 60_000 });
    const text = await assistant.textContent();
    expect(text).toMatch(/fun\b/);
    expect(text).toMatch(/end fun/);
  });

  test("multiple messages appear in chat", async ({ page }) => {
    await page.goto("/");
    const input = page.getByPlaceholder("Ask me to generate AVP code...");

    await input.fill("write a function to add two numbers");
    await page.getByRole("button", { name: "Send" }).click();
    await page.locator("pre").first().waitFor({ timeout: 60_000 });

    await input.fill("write a fibonacci function");
    await page.getByRole("button", { name: "Send" }).click();

    // Wait for second response
    await expect(page.locator("pre")).toHaveCount(2, { timeout: 60_000 });
  });

  test("empty input does not send", async ({ page }) => {
    await page.goto("/");
    const btn = page.getByRole("button", { name: "Send" });
    await expect(btn).toBeDisabled();
  });

  test("rate limiting shows error gracefully", async ({ page }) => {
    await page.goto("/");
    const input = page.getByPlaceholder("Ask me to generate AVP code...");

    // Fire 11 rapid requests
    for (let i = 0; i < 11; i++) {
      await input.fill(`test request ${i}`);
      await page.getByRole("button", { name: "Send" }).click();
      // Don't wait for response, just fire
      await page.waitForTimeout(100);
    }

    // Should see rate limit error
    await expect(page.getByText(/rate limit/i)).toBeVisible({ timeout: 10_000 });
  });
});
