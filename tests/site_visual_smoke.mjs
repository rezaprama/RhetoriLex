import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const playwrightModule = process.env.PLAYWRIGHT_MODULE_PATH || "playwright";
const { chromium } = require(playwrightModule);

const baseUrl = process.env.SITE_BASE_URL || "http://127.0.0.1:8765";
const catalogPath = process.env.SITE_CATALOG_PATH || path.resolve("data/dist/phrases.json");
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const visualOut = process.env.SITE_VISUAL_OUT || "";
const catalogBody = fs.readFileSync(catalogPath, "utf8");

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function installCatalogRoute(page) {
  await page.route("**/data/phrases.json", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json; charset=utf-8",
      body: catalogBody,
    });
  });
}

async function assertPage(page, route, viewport) {
  await page.setViewportSize(viewport);
  const response = await page.goto(baseUrl + route, { waitUntil: "networkidle" });
  assert(response && response.ok(), "Route failed: " + route);
  const state = await page.evaluate(() => ({
    h1: document.querySelectorAll("h1").length,
    main: document.querySelectorAll("main").length,
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    title: document.title,
    lang: document.documentElement.lang,
  }));
  assert(state.h1 === 1, "Expected one H1: " + route);
  assert(state.main === 1, "Expected one main landmark: " + route);
  assert(state.overflow <= 0, "Horizontal overflow " + state.overflow + "px: " + route);
  assert(state.title.length > 20, "Missing useful title: " + route);
  assert(state.lang === "en" || state.lang === "id", "Missing locale: " + route);
}

async function main() {
  const browser = await chromium.launch({
    headless: true,
    executablePath: chromePath,
  });
  const context = await browser.newContext();
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (error) => errors.push("pageerror: " + error.message));
  page.on("console", (message) => {
    if (message.type() === "error") errors.push("console: " + message.text());
  });
  await installCatalogRoute(page);

  const desktop = { width: 1440, height: 900 };
  const mobile = { width: 390, height: 844 };
  const routes = [
    "/en/",
    "/id/",
    "/en/research-gap/",
    "/id/kesenjangan-riset/",
    "/en/writing-skills/research-framing/",
    "/id/skill-penulisan/perumusan-riset/",
    "/en/phrase-explorer/?q=cautious%20interpretation",
    "/id/penjelajah-frasa/?q=interpretasi%20hati-hati",
  ];

  for (const route of routes) {
    await assertPage(page, route, desktop);
    await assertPage(page, route, mobile);
  }

  await page.setViewportSize(desktop);
  await page.goto(baseUrl + "/en/phrase-explorer/?q=cautious%20interpretation", {
    waitUntil: "networkidle",
  });
  await page.waitForSelector(".phrase-entry .entry-content");
  const firstResult = await page.locator("#results .phrase-entry").first().innerText();
  assert(!firstResult.includes("Claim strength\nCausal"), "Cautious query ranked a causal claim first");
  assert(!firstResult.includes("Risk\nHigh"), "Cautious query ranked a high-risk claim first");
  await page.locator("#results .copy-button").first().click();
  await page.waitForFunction(() => {
    const status = document.querySelector("#copy-status");
    return status && status.textContent.includes("copied");
  });
  await page.locator(".filter-panel summary").click();
  await page.selectOption("#risk-filter", "low");
  await page.waitForFunction(() => {
    const status = document.querySelector("#explorer-status");
    return status && !status.textContent.includes("Loading");
  });

  await page.evaluate(() => {
    localStorage.setItem("rhetorilex.theme", "dark");
  });
  await page.goto(baseUrl + "/en/", { waitUntil: "networkidle" });
  const dark = await page.evaluate(() => ({
    theme: document.documentElement.dataset.theme,
    background: getComputedStyle(document.body).backgroundColor,
  }));
  assert(dark.theme === "dark", "Dark theme preference not applied");
  assert(dark.background === "rgb(16, 22, 30)", "Unexpected dark background: " + dark.background);

  await page.evaluate(() => {
    localStorage.setItem("rhetorilex.theme", "light");
  });
  await page.reload({ waitUntil: "networkidle" });
  const light = await page.evaluate(() => ({
    theme: document.documentElement.dataset.theme,
    background: getComputedStyle(document.body).backgroundColor,
  }));
  assert(light.theme === "light", "Light theme preference not applied");
  assert(light.background === "rgb(245, 243, 237)", "Unexpected light background: " + light.background);

  await page.evaluate(() => {
    localStorage.setItem("rhetorilex.locale", "id");
  });
  await page.goto(baseUrl + "/", { waitUntil: "domcontentloaded" });
  await page.waitForURL("**/id/");
  assert(page.url().endsWith("/id/"), "Persisted Indonesian locale not selected at root");

  if (visualOut) {
    fs.mkdirSync(visualOut, { recursive: true });
    await page.setViewportSize(desktop);
    await page.goto(baseUrl + "/en/", { waitUntil: "networkidle" });
    await page.screenshot({ path: path.join(visualOut, "home-en-desktop.png"), fullPage: true });
    await page.goto(baseUrl + "/en/phrase-explorer/?q=cautious%20interpretation", {
      waitUntil: "networkidle",
    });
    await page.waitForSelector(".phrase-entry .entry-content");
    await page.screenshot({ path: path.join(visualOut, "explorer-en-desktop.png"), fullPage: true });
    await page.setViewportSize(mobile);
    await page.goto(baseUrl + "/id/", { waitUntil: "networkidle" });
    await page.screenshot({ path: path.join(visualOut, "home-id-mobile.png"), fullPage: true });
  }

  assert(errors.length === 0, errors.join("\n"));
  await browser.close();
  process.stdout.write("Headless site smoke passed for desktop, 390px mobile, themes, locale, explorer, and canonical skill routes.\n");
}

main().catch((error) => {
  process.stderr.write(error.stack + "\n");
  process.exitCode = 1;
});
